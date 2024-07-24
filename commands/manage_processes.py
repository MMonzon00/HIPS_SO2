import subprocess
from logging_notification import log_event, notify_admin

def list_high_memory_processes(threshold):
    """List processes consuming more than the given memory threshold."""
    try:
        # Use ps command to list processes with memory usage
        result = subprocess.run(['ps', '-eo', 'pid,%mem,cmd', '--sort=-%mem'], capture_output=True, text=True, check=True)
        lines = result.stdout.splitlines()
        
        high_memory_processes = []
        for line in lines[1:]:  # Skip header line
            parts = line.strip().split(maxsplit=2)
            pid = parts[0]
            mem_percent = float(parts[1])
            command = parts[2]
            if mem_percent > threshold:
                high_memory_processes.append((pid, mem_percent, command))
                log_event(f"High memory usage detected: PID {pid}, Memory Usage: {mem_percent}%, Command: {command}")
        
        if high_memory_processes:
            notify_admin(f"High memory usage processes detected: {', '.join([f'PID {p[0]} ({p[1]}%)' for p in high_memory_processes])}")
        
        return high_memory_processes
    except subprocess.CalledProcessError as e:
        error_message = f"Error retrieving process list: {e}"
        log_event(error_message)
        return []

def kill_process(pid):
    """Kill a process with the given PID."""
    try:
        subprocess.run(['kill', '-9', pid], check=True)
        success_message = f"Killed process with PID {pid}"
        log_event(success_message)
    except subprocess.CalledProcessError as e:
        error_message = f"Error killing process {pid}: {e}"
        print(error_message)
        log_event(error_message)