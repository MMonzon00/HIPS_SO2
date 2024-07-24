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

        # Log the analysis results
        log_message = "Page errors by IP:\n"
        for ip, count in page_errors.items():
            log_message += f"IP {ip} had {count} 404 errors.\n"
        
        log_event(log_message)  # Log the detailed analysis
        notify_admin(log_message)  # Notify the administrator about the errors

    except Exception as e:
        error_message = f"Error analyzing access log: {e}"
        log_event(error_message)  # Log the error

    return page_errors
