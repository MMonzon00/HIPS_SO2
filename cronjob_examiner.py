import sys
import subprocess

def list_user_crontab(username):
    """List all cronjobs for a specific user."""
    try:
        # Use subprocess to run 'crontab -l' for the specified user
        result = subprocess.run(['crontab', '-l', '-u', username], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None

def list_system_cron():
    """List all cronjobs configured system-wide."""
    try:
        # Use subprocess to list files in /etc/cron.d/ and their contents
        result = subprocess.run(['ls', '/etc/cron.d/'], capture_output=True, text=True, check=True)
        cron_files = result.stdout.splitlines()
        
        # Read contents of each file in /etc/cron.d/
        cron_jobs = []
        for cron_file in cron_files:
            file_path = f'/etc/cron.d/{cron_file}'
            with open(file_path, 'r') as f:
                cron_jobs.append(f.read())
        
        return cron_jobs
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 cronjob_examiner.py <username>")
        sys.exit(1)
    
    username = sys.argv[1]
    
    # List cronjobs for the specified user
    user_cronjobs = list_user_crontab(username)
    if user_cronjobs:
        print(f"Cronjobs for user '{username}':")
        print(user_cronjobs)
    
    print("-" * 40)
    
    # List system-wide cronjobs
    system_cronjobs = list_system_cron()
    if system_cronjobs:
        print("System-wide cronjobs:")
        for job in system_cronjobs:
            print(job)
