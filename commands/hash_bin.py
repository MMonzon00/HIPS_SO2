import os
import hashlib
from datetime import datetime
from logging_notification import log_event, notify_admin

def read_file(file_path):
    """Read the content of the file."""
    try:
        with open(file_path, 'rb') as f:
            return f.read()
    except FileNotFoundError:
        error_message = f"Error: {file_path} not found."
        log_event(error_message)
        return None

def generate_hash(file_content):
    """Generate SHA-256 hash of the file content."""
    sha256 = hashlib.sha256()
    sha256.update(file_content)
    return sha256.hexdigest()

def store_hash(file_path, hash_value, hash_file, status):
    """Store the hash with a timestamp and status in the hash file."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(hash_file, 'a') as f:
        f.write(f"{timestamp} {status} {file_path}: {hash_value}\n")

def get_last_hash(file_path, hash_file):
    """Retrieve the last hash value for the specified file from the hash log."""
    last_hash = None
    try:
        with open(hash_file, 'r') as f:
            for line in f:
                if file_path in line:
                    last_hash = line.strip().split()[-1]
    except FileNotFoundError:
        error_message = f"Error: {hash_file} not found."
        log_event(error_message)
    return last_hash

def trigger_alarm(file_path):
    """Generate an alarm for the modified file."""
    alarm_message = f"ALERT: File {file_path} has been modified!"
    log_event(alarm_message)
    notify_admin('Modified File',alarm_message)

def verify_and_hash_file(file_path, hash_file):
    """Verify the file, generate its hash, compare with the last hash, and store the new hash."""
    file_content = read_file(file_path)
    if file_content is None:
        return
    
    current_hash = generate_hash(file_content)
    last_hash = get_last_hash(file_path, hash_file)

    if last_hash is None:
        log_message = f"No previous hash found for {file_path}. Storing the current hash."
        log_event(log_message)
        status = "NEW"
    elif current_hash != last_hash:
        log_message = f"File {file_path} has been modified."
        log_event(log_message)
        status = "MODIFIED"
        trigger_alarm(file_path)
    else:
        log_message = f"File {file_path} has not been modified."
        log_event(log_message)
        status = "NOT MODIFIED"

    store_hash(file_path, current_hash, hash_file, status)
    return f"{file_path} hash stored with status: {status}"

def read_logged_hashes(log_file):
    """Read the logged hashes from the log file."""
    logged_hashes = {}
    try:
        with open(log_file, 'r') as log:
            for line in log:
                parts = line.strip().split()
                if len(parts) >= 5 and parts[2] == "SUCCESS":
                    file_path = parts[3].strip(':')
                    file_hash = parts[4]
                    logged_hashes[file_path] = file_hash
    except FileNotFoundError:
        pass  # Log file does not exist yet
    return logged_hashes

def hash_bin():
    directory = '/bin'
    log_file = '/var/log/bin_hash.log'
    
    # Read the previously logged hashes
    logged_hashes = read_logged_hashes(log_file)
    
    current_hashes = {}
    modified_files = []
    
    for root, dirs, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            try:
                with open(file_path, 'rb') as f:
                    file_content = f.read()
                    file_hash = generate_hash(file_content)
                    status = "SUCCESS"
                    current_hashes[file_path] = file_hash
            except Exception as e:
                file_hash = str(e)
                status = "FAILURE"
                log_event(f"Failed to read or hash file {file_path}: {file_hash}")

            # Check if the file hash has changed
            try:
                if status == "SUCCESS" and logged_hashes[file_path] != file_hash:
                    modified_files.append(file_path)
            except KeyError:
                log_event(f'New file detected: {file_path}')
                modified_files.append(file_path)
    
    # Update the log file only if modifications are detected
    if modified_files:
        with open(log_file, 'a') as log:
            for file_path in modified_files:
                file_hash = current_hashes[file_path]
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                log.write(f"{timestamp} SUCCESS {file_path}: {file_hash}\n")
        notify_admin('Bin modified',f"Modified files detected: {', '.join(modified_files)}")
    
    return modified_files

def verify_integrity_files():
    return_list = []
    modified_files = hash_bin()
    if modified_files:
        return_list.append("Modified files:")
        return_list.extend(modified_files)
    else:
        return_list.append("No modifications detected in the /bin directory.")

    file_path = ["/etc/passwd", "/etc/shadow"]
    hash_file = "/var/log/file_hashes.log"  # File to store the hashes

    passwd_return = verify_and_hash_file(file_path[0], hash_file)
    shadow_return = verify_and_hash_file(file_path[1], hash_file)

    return_list.extend([passwd_return, shadow_return])

    return return_list
