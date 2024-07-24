import re
from collections import defaultdict
import os
from logging_notification import log_event, notify_admin

def analyze_access_log():
    page_errors = defaultdict(int)
    log_file_path = os.path.abspath('../HIPS_SO2/tests/accessLog.log')
    try:
        with open(log_file_path, 'r') as file:
            for line in file:
                if '404' in line:  # Assuming 404 errors indicate access issues
                    ip_match = re.search(r'(\d+\.\d+\.\d+\.\d+)', line)
                    if ip_match:
                        ip = ip_match.group(1)
                        page_errors[ip] += 1

        result = "HTTP Access Errors:\n"
        for ip, count in page_errors.items():
            if count > 5:
                result += f"IP {ip} has {count} page errors. Blocking IP...\n"
                log_event(result)
                # Add logic to block IP
                # os.system(f"sudo iptables -A INPUT -s {ip} -j DROP")

    except Exception as e:
        error_message = f"Error analyzing access log: {e}"
        log_event(error_message)  # Log the error
    notify_admin(result)
    return result