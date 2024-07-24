import os
import shutil
import logging
from logging_notification import log_event, notify_admin


# Logging configuration
logging.basicConfig(filename='/var/log/check_tmp.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def log_event(event):
    logging.info(event)

def check_tmp_directory():
    suspicious_files = []

    # List all files in /tmp directory
    tmp_files = os.listdir('/tmp')

    # Check each file in /tmp
    for filename in tmp_files:
        file_path = os.path.join('/tmp', filename)

        # Check if it's a regular file and ends with .sh (example for scripts)
        if os.path.isfile(file_path) and filename.endswith('.sh'):
            suspicious_files.append(file_path)

    return suspicious_files

def quarantine_files(files):
    quarantine_folder = '/tmp/quarantine'

    # Create quarantine folder if it doesn't exist
    if not os.path.exists(quarantine_folder):
        os.makedirs(quarantine_folder)

    # Move suspicious files to quarantine
    for file_path in files:
        try:
            shutil.move(file_path, os.path.join(quarantine_folder, os.path.basename(file_path)))
            log_message = f"Moved {file_path} to {quarantine_folder}"
            print(log_message)  # Print the action for immediate feedback
            log_event(log_message)  # Log the action
            notify_admin(log_message)  # Notify the admin about the action
        except Exception as e:
            error_message = f"Failed to move {file_path}: {str(e)}"
            print(error_message)  # Print the error for immediate feedback
            log_event(error_message)  # Log the error
            notify_admin(error_message)  # Notify the admin about the error

# Main function to execute the checks
def main():
    suspicious_files = check_tmp_directory()

    if suspicious_files:
        log_message = "Suspicious files found in /tmp:"
        log_event(log_message)
        notify_admin(log_message)

        for file_path in suspicious_files:
            log_event(f"Suspicious file detected: {file_path}")
            notify_admin(f"Suspicious file detected: {file_path}")

        # Quarantine the suspicious files
        quarantine_files(suspicious_files)
    else:
        log_message = "No suspicious files found in /tmp"
        log_event(log_message)
        notify_admin(log_message)
