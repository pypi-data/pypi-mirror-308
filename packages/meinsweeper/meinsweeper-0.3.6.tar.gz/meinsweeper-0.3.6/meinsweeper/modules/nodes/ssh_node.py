import socket
from pathlib import Path
import asyncio
import asyncssh
import threading
import os
import traceback
from time import time
import psutil
from datetime import datetime

from meinsweeper.modules.helpers.debug_logging import init_node_logger
from meinsweeper.modules.helpers.utils import timeout_iterator, debug_print
from meinsweeper.modules.helpers.retry import RetryStrategy
from .abstract import ComputeNode

# Use environment variables with default values
MINIMUM_VRAM = int(os.environ.get('MINIMUM_VRAM', 10)) * 1024  # Convert GB to MB
USAGE_CRITERION = float(os.environ.get('USAGE_CRITERION', 0.1))

class SSHNode(ComputeNode):
    _instances = {}
    _connections = {}
    _lock = threading.Lock()

    def __new__(cls, node_name, log_q, address, username, password=None, key_path=None, timeout=5):
        with cls._lock:
            if node_name not in cls._instances:
                instance = super().__new__(cls)
                cls._instances[node_name] = instance
                instance.initialized = False
            return cls._instances[node_name]

    def __init__(self, node_name, log_q, address, username, password=None, key_path=None, timeout=5):
        if not hasattr(self, 'initialized') or not self.initialized:
            assert password or key_path, "Either password or key_path must be provided."
            self.log_q = log_q
            self.name = node_name
            self.connection_info = {
                'address': address,
                'username': username,
                'password': password,
                'key_path': key_path,
                'timeout': timeout
            }
            self.RUN_TIMEOUT = timeout
            self.node_logger = init_node_logger(self.name)
            self.log_lock = threading.Lock()
            self.initialized = True
            debug_print(f"SSHNode initialized with name: {self.name}, address: {address}")
            self.warning_timestamps = {}
            self.WARNING_INTERVAL = 5
            self.last_heartbeat = time()
            self.HEARTBEAT_TIMEOUT = 300  # 5 minutes
            self.process = None

    def log_info(self, label, message):
        with self.log_lock:
            self.node_logger.info(f"{self.name} | {label} | {message}")

    def log_error(self, label, message):
        with self.log_lock:
            self.node_logger.error(f"{self.name} | {label} | {message}")

    def log_warning(self, label, message):
        with self.log_lock:
            # Create a key for this specific warning
            warning_key = f"{label}_{message}"
            current_time = time()
            
            # Check if we should log this warning
            last_time = self.warning_timestamps.get(warning_key, 0)
            if current_time - last_time >= self.WARNING_INTERVAL:
                self.node_logger.warning(f"{self.name} | {label} | {message}")
                self.warning_timestamps[warning_key] = current_time

    def log_debug(self, label, message):
        with self.log_lock:
            self.node_logger.debug(f"{self.name} | {label} | {message}")

    async def open_connection(self):
        address = self.connection_info['address']
        conn_key = f"{address}_{os.getpid()}"
        
        with self._lock:
            if conn_key in self._connections:
                self.conn, self.scp_conn = self._connections[conn_key]
                try:
                    # Test if connection is still alive
                    await self.conn.run('echo test')
                    debug_print(f"Reusing existing connection to {address}")
                    self.free_gpus = await self.check_gpu_free()
                    return bool(self.free_gpus)
                except:
                    # Connection dead, remove it
                    del self._connections[conn_key]

        debug_print(f"Attempting SSH connection to {address} for node {self.name}")
        try:
            self.log_info("INIT", f"Connecting SSH to {address}")
            self.conn = await asyncio.wait_for(
                asyncssh.connect(
                    address,
                    username=self.connection_info['username'],
                    known_hosts=None,
                    login_timeout=self.connection_info['timeout'],
                    encoding='utf-8',
                    client_keys=[self.connection_info['key_path']] if self.connection_info['key_path'] else None,
                    term_type='bash'
                ),
                timeout=self.connection_info['timeout']
            )
            
            self.log_info("INIT", f"Connecting SCP to {address}")
            self.scp_conn = await asyncio.wait_for(
                asyncssh.connect(
                    address,
                    username=self.connection_info['username'],
                    known_hosts=None,
                    login_timeout=self.connection_info['timeout'],
                    encoding='utf-8',
                    client_keys=[self.connection_info['key_path']] if self.connection_info['key_path'] else None
                ),
                timeout=self.connection_info['timeout']
            )

            # Store connections
            with self._lock:
                self._connections[conn_key] = (self.conn, self.scp_conn)

        except asyncio.TimeoutError:
            self.log_warning("INIT", f"Connection timeout to {address}")
            return False
        except Exception as e:
            debug_print(f"Connection failed to {address}: {str(e)}")
            return False

        self.free_gpus = await self.check_gpu_free()
        return bool(self.free_gpus)

    
    async def check_gpu_free(self):
        address = self.connection_info['address']
        self.log_info("GPU_CHECK", f"Starting GPU check on {address}")
        
        retry_strategy = RetryStrategy(
            max_retries=3,
            initial_delay=1.0,
            max_delay=30.0,
            backoff_factor=2.0,
            logger=self.node_logger
        )

        try:
            # Copy script with unique name
            self.log_info("GPU_CHECK", f"Attempting to copy check script to {address}")
            success, remote_script, error = await retry_strategy.execute(
                self._copy_gpu_check_script
            )
            if not success:
                self.log_error("GPU_CHECK", f"Failed to copy GPU check script to {address}: {error}")
                return []

            # Run the node-specific script
            self.log_info("GPU_CHECK", f"Attempting to run check script on {address}")
            success, result, error = await retry_strategy.execute(
                lambda: self._run_gpu_check(remote_script)
            )
            if not success:
                self.log_error("GPU_CHECK", f"Failed to run GPU check on {address}: {error}")
                return []

            # Clean up the script after use
            try:
                await self.conn.run(f'rm -f {remote_script}')
            except Exception as e:
                self.log_warning("GPU_CHECK", f"Failed to clean up check script {remote_script}: {e}")

            self.log_info("GPU_CHECK", f"Successfully ran GPU check on {address}, parsing output")
            gpus = self._parse_gpu_check_output(result)
            self.log_info("GPU_CHECK", f"Found GPUs on {address}: {gpus}")
            return gpus

        except Exception as e:
            self.log_error("GPU_CHECK", f"Unexpected error during GPU check on {address}: {str(e)}\n{traceback.format_exc()}")
            return []

    async def _copy_gpu_check_script(self):
        """Helper to copy the GPU check script with node-specific name"""
        try:
            script_path = Path(__file__).parent.parent / 'check_gpu.py'
            # Create node-specific script name
            remote_script = f'/tmp/check_gpu_{self.name}_{os.getpid()}.py'
            self.log_debug("GPU_CHECK", f"Copying {script_path} to remote {remote_script}")
            await asyncssh.scp(script_path, (self.scp_conn, remote_script))
            self.log_debug("GPU_CHECK", "Successfully copied check script")
            return remote_script
        except Exception as e:
            self.log_error("GPU_CHECK", f"Error copying GPU check script: {str(e)}\n{traceback.format_exc()}")
            raise

    async def _run_gpu_check(self, script_path):
        """Helper to run the GPU check script"""
        try:
            self.log_debug("GPU_CHECK", f"Running {script_path}")
            result = await asyncio.wait_for(
                self.conn.run(f'python {script_path}'),
                timeout=self.RUN_TIMEOUT
            )
            self.log_debug("GPU_CHECK", f"check_gpu.py output: {result.stdout.strip()}")
            return result.stdout.strip()
        except asyncio.TimeoutError:
            self.log_error("GPU_CHECK", f"Timeout running GPU check after {self.RUN_TIMEOUT}s")
            raise
        except Exception as e:
            self.log_error("GPU_CHECK", f"Error running GPU check: {str(e)}\n{traceback.format_exc()}")
            raise

    def _parse_gpu_check_output(self, gpu_info: str) -> list[str]:
        """Helper to parse GPU check output"""
        if 'No Module named' in gpu_info:
            self.log_warning("GPU_CHECK", f"Missing pynvml module on {self.connection_info['address']} - cannot check GPU")
            return []

        free_gpus = []
        for line in gpu_info.split('\n'):
            if '[[GPU INFO]]' in line:
                # Extract GPU indices from the format "[[GPU INFO]] [0,1,2] Free"
                line = line.replace('[[GPU INFO]]', '')
                gpu_list = line.split('[')[1].split(']')[0]
                if gpu_list:  # Only process if there are GPUs listed
                    if ',' in gpu_list:
                        free_gpus = gpu_list.split(',')
                    else:
                        free_gpus = [gpu_list]
                    self.log_debug("GPU_CHECK", f"Found free GPUs: {free_gpus}")

        if not free_gpus:
            self.log_warning("GPU_CHECK", f"No free GPUs found on {self.connection_info['address']} - got {gpu_info}")

        return free_gpus

    async def run(self, command, label):
        if not self.free_gpus:
            self.log_warning(label, f"No free GPUs available on {self.connection_info['address']}")
            return False

        gpu_to_use = self.free_gpus.pop(0)
        self.log_info(label, f"Selected GPU {gpu_to_use} for job on {self.connection_info['address']}")

        env = f"CUDA_VISIBLE_DEVICES={gpu_to_use}"
        full_command = f"{env} {command}"

        self.log_info(label, f"Running command on {self.connection_info['address']} GPU {gpu_to_use}")
        await self.log_q.put((({'status': 'running'}, 'running'), self.connection_info['address'], label))

        max_retries = 2
        retry_count = 0

        while retry_count < max_retries:
            try:
                self.log_debug(label, f"Creating process for command: {full_command}")
                async with self.conn.create_process(full_command) as proc:
                    self.process = proc
                    monitor_task = asyncio.create_task(self._monitor_process(proc, label))
                    
                    try:
                        while True:
                            try:
                                line = await asyncio.wait_for(proc.stdout.readline(), timeout=self.RUN_TIMEOUT)
                                self.last_heartbeat = time()  # Update heartbeat
                                
                                if not line:
                                    break
                                
                                line = line.strip()
                                if line:
                                    # Monitor memory usage
                                    try:
                                        mem_info = await self._get_memory_usage(proc)
                                        if mem_info:
                                            self.log_debug(label, f"Memory usage: {mem_info}")
                                    except Exception as e:
                                        self.log_warning(label, f"Failed to get memory usage: {e}")
                                    
                                    self.log_info(label, f"stdout: {line}")
                                    parsed_line = self.parse_log_line(line)
                                    if parsed_line == "FAILED":
                                        self.log_warning(label, f"Failed (caught via parsed line)")
                                        await self.log_q.put(({"status": "failed"}, self.connection_info["address"], label))
                                        return False
                                    await self.log_q.put((parsed_line, self.connection_info["address"], label))

                            except asyncio.TimeoutError:
                                time_since_heartbeat = time() - self.last_heartbeat
                                if time_since_heartbeat > self.HEARTBEAT_TIMEOUT:
                                    self.log_error(label, f"No heartbeat for {time_since_heartbeat}s, terminating")
                                    await self._terminate_process(proc)
                                    raise
                                self.log_warning(label, f"Timeout while reading stdout")
                                raise

                        stderr = await proc.stderr.read()
                        if stderr:
                            self.log_error(label, f"stderr output: {stderr}")
                            await self.log_q.put(({"status": "failed", "stderr": stderr}, self.connection_info["address"], label))
                            return False

                        exit_status = await proc.wait()
                        monitor_task.cancel()
                        
                        if exit_status != 0:
                            self.log_error(label, f"Process exited with non-zero status: {exit_status}")
                            await self.log_q.put(({"status": "failed", "exit_status": exit_status}, self.connection_info["address"], label))
                            return False

                        break

                    except asyncio.TimeoutError:
                        await self._terminate_process(proc)
                        timeout_msg = f"Job killed - exceeded timeout of {self.RUN_TIMEOUT} seconds"
                        self.log_error(label, timeout_msg)
                        await self.log_q.put((
                            {
                                "status": "failed", 
                                "error": "timeout",
                                "message": timeout_msg
                            }, 
                            self.connection_info["address"], 
                            label
                        ))
                        return False

            except Exception as err:
                self.log_error(label, f'Unexpected error: {err}\nTraceback:\n{traceback.format_exc()}')
                await self.log_q.put(({"status": "failed", "error": str(err), "traceback": traceback.format_exc()}, self.connection_info["address"], label))
                return False

        self.free_gpus.append(gpu_to_use)
        self.log_info(label, f"Job completed successfully")
        await self.log_q.put(({"status": "completed"}, self.connection_info["address"], label))
        return True

    async def _monitor_process(self, proc, label):
        """Monitor process resources and health"""
        try:
            while True:
                try:
                    # Check process existence and resource usage
                    if proc.returncode is not None:
                        self.log_warning(label, f"Process terminated with return code {proc.returncode}")
                        break
                    
                    # Log process stats periodically
                    mem_info = await self._get_memory_usage(proc)
                    if mem_info:
                        self.log_debug(label, f"Process stats: {mem_info}")
                    
                    await asyncio.sleep(60)  # Check every minute
                    
                except Exception as e:
                    self.log_error(label, f"Error monitoring process: {e}")
                    break
                    
        except asyncio.CancelledError:
            pass

    async def _get_memory_usage(self, proc):
        """Get memory usage of the remote process"""
        try:
            result = await self.conn.run(f'ps -p {proc.pid} -o pid,ppid,rss,vsize,pcpu,pmem,comm,state')
            return result.stdout
        except:
            return None

    async def _terminate_process(self, proc):
        """Safely terminate a process"""
        try:
            if proc and proc.returncode is None:
                self.log_warning(proc.get_extra_info('peername')[0], "Terminating process")
                proc.terminate()
                try:
                    await asyncio.wait_for(proc.wait(), timeout=5)
                except asyncio.TimeoutError:
                    proc.kill()  # Force kill if graceful termination fails
        except Exception as e:
            self.log_error(proc.get_extra_info('peername')[0], f"Error terminating process: {e}")

    @staticmethod
    def parse_log_line(line):
        out = None
        if '[[LOG_ACCURACY TRAIN]]' in line:
            out = {}
            line = line.split('[[LOG_ACCURACY TRAIN]]')[1]
            line = line.split(';')
            for section in line:
                if 'Elapsed' in section:
                    continue
                elif "Losses" in section:
                    loss_terms = section.split('Losses:')[1].split(',')
                    for loss_term in loss_terms:
                        loss_name, loss_value = map(lambda x: x.strip(), loss_term.split(':'))
                        out[f'loss_total'] = float(loss_value)
                elif 'Step' in section:
                    out['completed'] = int(section.split('Step:')[1])
        elif '[[LOG_ACCURACY TEST]]' in line:
            line = line.split(':')[1]
            out = {'test_acc': float(line.strip())}
        elif 'error' in line or 'RuntimeError' in line or 'failed' in line or 'Killed' in line:
            out = 'FAILED'
        return out

    def __str__(self) -> str:
        return f'SSH Node {self.name} ({self.connection_info["address"]}) with user {self.connection_info["username"]}'

    @classmethod
    def clear_instances(cls):
        """Clear all stored instances and connections"""
        with cls._lock:
            debug_print(f"Clearing SSHNode instances. Current instances: {list(cls._instances.keys())}")
            # Close all connections
            for conn, scp_conn in cls._connections.values():
                conn.close()
                scp_conn.close()
            cls._connections.clear()
            cls._instances.clear()
            debug_print("SSHNode instances cleared")