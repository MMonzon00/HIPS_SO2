import re
from collections import defaultdict
import os
from typing import Dict, List, Tuple
from logging_notification import log_event, notify_admin

# Path to the log file
log_file_path = os.path.abspath('../HIPS_SO2/tests/remote_connection.log')

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

    # Log and notify for users with repetitive failed attempts
    log_user_attempts(user_attempts)
    
    # Log and notify for IPs with multiple failed attempts
    log_ip_attempts(ip_attempts)
    
    return user_attempts, ip_attempts

def log_user_attempts(user_attempts: Dict[str, int]):
    """Log and notify for users with repetitive failed attempts."""
    user_list=[]
    for user, attempts in user_attempts.items():
        if attempts > 5:  # Threshold for repetitive attempts
            message = f"User {user} has {attempts} failed login attempts.\n"
            log_event(message)
            user_list.append(message)
    notify_admin(''.join(user_list))

def log_ip_attempts(ip_attempts: Dict[str, int]):
    """Log and notify for IPs with multiple failed attempts."""
    ip_list=[]
    for ip, attempts in ip_attempts.items():
        if attempts > 5:  # Threshold for multiple user attempts
            message = f"IP {ip} has {attempts} failed login attempts.\n"
            log_event(message)
            ip_list.append(message)
    notify_admin(''.join(ip_list))

analyze_failed_attempts()