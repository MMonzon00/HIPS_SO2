import hashlib
from datetime import datetime

def read_file(file_path):
    """Read the content of the file."""
    try:
        with open(file_path, 'rb') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
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
        print(f"Error: {hash_file} not found.")
    return last_hash

def trigger_alarm(file_path):
    """Generate an alarm for the modified file."""
    print(f"ALERT: File {file_path} has been modified!")

def verify_and_hash_file(file_path, hash_file):
    """Verify the file, generate its hash, compare with the last hash, and store the new hash."""
    file_content = read_file(file_path)
    if file_content is None:
        return
    
    current_hash = generate_hash(file_content)
    last_hash = get_last_hash(file_path, hash_file)

    if last_hash is None:
        print(f"No previous hash found for {file_path}. Storing the current hash.")
        status = "NEW"
    elif current_hash != last_hash:
        print(f"File {file_path} has been modified.")
        status = "MODIFIED"
        trigger_alarm(file_path)
    else:
        print(f"File {file_path} has not been modified.")
        status = "NOT MODIFIED"

    store_hash(file_path, current_hash, hash_file, status)

def main():
    passwd_file = "/etc/passwd"
    shadow_file = "/etc/shadow"
    hash_file = "/var/log/file_hashes.log"  # File to store the hashes

    verify_and_hash_file(passwd_file, hash_file)
    verify_and_hash_file(shadow_file, hash_file)

if __name__ == "__main__":
    main()
