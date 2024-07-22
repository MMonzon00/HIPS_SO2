import re
from collections import defaultdict
import os
from typing import Dict, List, Tuple

# Path to the log file
log_file_path = os.path.abspath('../xd/tests/remote_connection.log')

def analyze_failed_attempts() -> Tuple[Dict[str, int], Dict[str, int]]:
    """Analyze failed login attempts from the log file."""
    failed_attempts = defaultdict(list)
    user_attempts = defaultdict(int)
    ip_attempts = defaultdict(int)

    # Read and parse the log file
    with open(log_file_path, 'r') as file:
        for line in file:
            match = re.search(r'Failed password for invalid user (\w+) from (\d+\.\d+\.\d+\.\d+)', line)
            if match:
                user = match.group(1)
                ip = match.group(2)
                failed_attempts[user].append(ip)
                user_attempts[user] += 1
                ip_attempts[ip] += 1

    return user_attempts, ip_attempts
