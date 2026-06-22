"""
Execution environment for running shell tasks securely inside the sandbox.
Handles stream-level OOM protections, encoding issues, and cross-platform process isolation.
"""

import os
import signal
import subprocess
import platform
import time
import threading
from dataclasses import dataclass
from typing import Optional, List


@dataclass
class ExecutionResult:
    """Contains the execution state of a sandbox command execution."""
    stdout: str
    stderr: str
    exit_code: int
    timed_out: bool


class BashExecutionTool:
    """
    Executes shell commands with strict timeout limits, process group termination,
    OOM protections, and output log truncation.
    """
    def __init__(
        self, 
        default_timeout: float = 10.0, 
        max_output_chars: int = 10000, 
        max_buffer_bytes: int = 5 * 1024 * 1024  # Strict 5MB stream limit to prevent OOM
    ):
        self.default_timeout = default_timeout
        self.max_output_chars = max_output_chars
        self.max_buffer_bytes = max_buffer_bytes
        self.is_posix = platform.system() != "Windows"

    def _truncate_output(self, text: str) -> str:
        """Tails the output to keep tracebacks or exit summaries visible."""
        if len(text) <= self.max_output_chars:
            return text
        
        truncated_count = len(text) - self.max_output_chars
        marker = f"\n\n[... Truncated {truncated_count} characters of output to prevent context overflow ...]\n\n"
        return marker + text[-self.max_output_chars:]

    def _terminate_process_tree(self, process: subprocess.Popen) -> None:
        """Kills the parent process and any nested subprocesses spawned."""
        if self.is_posix:
            try:
                pgid = os.getpgid(process.pid)
                os.killpg(pgid, signal.SIGKILL)
            except OSError:
                pass
        else:
            # Use taskkill on Windows to clean the entire child tree recursively (/T)
            try:
                subprocess.run(
                    ["taskkill", "/F", "/T", "/PID", str(process.pid)],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    check=False
                )
            except Exception:
                process.kill()

    def execute(self, command: str, timeout: Optional[float] = None) -> ExecutionResult:
        """
        Executes a command inside the sandbox. Reads output in binary mode via threads
        to avoid UnicodeDecodeErrors on non-text output.
        """
        exec_timeout = timeout if timeout is not None else self.default_timeout
        
        # Binary mode (omitting text=True) prevents decode crashes on raw outputs
        kwargs = {
            "shell": True,
            "stdout": subprocess.PIPE,
            "stderr": subprocess.PIPE,
        }
        
        if self.is_posix:
            kwargs["preexec_fn"] = os.setsid
            kwargs["executable"] = "/bin/bash"
        else:
            kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP  # type: ignore

        try:
            process = subprocess.Popen(command, **kwargs)
        except Exception as e:
            return ExecutionResult(
                stdout="",
                stderr=f"Failed to start process: {str(e)}",
                exit_code=-1,
                timed_out=False
            )

        stdout_chunks: List[bytes] = []
        stderr_chunks: List[bytes] = []
        
        # Bounded read loops to prevent OOM
        def read_stream(stream, chunks: List[bytes], max_bytes: int):
            bytes_read = 0
            try:
                while bytes_read < max_bytes:
                    chunk = stream.read(4096)
                    if not chunk:
                        break
                    chunks.append(chunk)
                    bytes_read += len(chunk)
            except Exception:
                pass

        t_out = threading.Thread(target=read_stream, args=(process.stdout, stdout_chunks, self.max_buffer_bytes))
        t_err = threading.Thread(target=read_stream, args=(process.stderr, stderr_chunks, self.max_buffer_bytes))
        
        t_out.daemon = True
        t_err.daemon = True
        t_out.start()
        t_err.start()

        start_time = time.time()
        timed_out = False
        
        while process.poll() is None:
            if time.time() - start_time > exec_timeout:
                timed_out = True
                self._terminate_process_tree(process)
                break
            time.sleep(0.05)

        # Confirm process has cleared
        try:
            process.wait(timeout=1.0)
        except subprocess.TimeoutExpired:
            self._terminate_process_tree(process)
            
        # Join stream-capturing threads
        t_out.join(timeout=0.5)
        t_err.join(timeout=0.5)

        # Close streams safely
        if process.stdout:
            process.stdout.close()
        if process.stderr:
            process.stderr.close()

        # Decodes strings using replacement characters to avoid decoder crashes on binary outputs
        stdout_str = b"".join(stdout_chunks).decode("utf-8", errors="replace")
        stderr_str = b"".join(stderr_chunks).decode("utf-8", errors="replace")

        return ExecutionResult(
            stdout=self._truncate_output(stdout_str),
            stderr=self._truncate_output(stderr_str),
            exit_code=process.returncode if not timed_out else -1,
            timed_out=timed_out
        )
