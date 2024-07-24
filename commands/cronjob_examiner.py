import sys
import subprocess
from logging_notification import log_event, notify_admin

def list_user_crontab(username):
    """List all cronjobs for a specific user."""
    try:
        # Use subprocess to run 'crontab -l' for the specified user
        result = subprocess.run(['crontab', '-l', '-u', username], capture_output=True, text=True, check=True)
        log_message = f"Cronjobs for user '{username}':\n{result.stdout}"
        log_event(log_message)  # Log the cronjobs for the user
        notify_admin(log_message)  # Notify the admin about the cronjobs
        return result.stdout
    except subprocess.CalledProcessError as e:
        error_message = f"Error listing crontab for user '{username}': {e}"
        print(error_message)  # Print the error for immediate feedback
        log_event(error_message)  # Log the error
        return None

def list_system_cron():
    """List all cronjobs configured system-wide."""
    try:
        # Use subprocess to list files in /etc/cron.d/ and their contents
        result = subprocess.run(['ls', '/etc/cron.d/'], capture_output=True, text=True, check=True)
        cron_files = result.stdout.splitlines()

        cron_jobs = []
        for cron_file in cron_files:
            file_path = f'/etc/cron.d/{cron_file}'
            with open(file_path, 'r') as f:
                cron_job = f.read()
                cron_jobs.append(cron_job)

        log_message = "System-wide cronjobs:\n" + "\n".join(cron_jobs)
        log_event(log_message)  # Log the system-wide cronjobs
        notify_admin(log_message)  # Notify the admin about the system-wide cronjobs
        return cron_jobs
    except subprocess.CalledProcessError as e:
        error_message = f"Error listing system-wide cronjobs: {e}"
        print(error_message)  # Print the error for immediate feedback
        log_event(error_message)  # Log the error
        return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage_message = "Usage: python3 cronjob_examiner.py <username>"
        print(usage_message)  # Print usage message
        log_event(usage_message)  # Log the usage message
        notify_admin(usage_message)  # Notify the admin about the incorrect usage
        sys.exit(1)
    
    username = sys.argv[1]
    
    # List cronjobs for the specified user
    user_cronjobs = list_user_crontab(username)
    
    # List system-wide cronjobs
    system_cronjobs = list_system_cron()
