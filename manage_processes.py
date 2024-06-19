import subprocess
import time

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
        
        return high_memory_processes
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return []

def kill_process(pid):
    """Kill a process with the given PID."""
    try:
        subprocess.run(['kill', '-9', pid], check=True)
        print(f"Killed process with PID {pid}")
    except subprocess.CalledProcessError as e:
        print(f"Error killing process {pid}: {e}")


# Define threshold for high memory usage (adjust as needed)
memory_threshold = 10.0  # Threshold in percent

# List processes consuming high memory
high_memory_processes = list_high_memory_processes(memory_threshold)

if high_memory_processes:
    print("Processes consuming high memory:")
    for pid, mem_percent, command in high_memory_processes:
        print(f"PID: {pid}, Memory %: {mem_percent:.2f}, Command: {command}")
        # Example: Kill processes consuming high memory for more than 5 minutes
        if mem_percent > 50.0:
            print(f"Killing process with PID {pid} consuming {mem_percent:.2f}% memory...")
            kill_process(pid)
if memory_threshold == 10:
    print("No process consuming memory higher than threshold!")