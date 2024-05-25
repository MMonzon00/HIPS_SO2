# HIPS-SO2
Implementacion de HIPS(Host Intrusion Prevention System)

## Function: Binary File Verification

### Description:
The `verify_and_hash_file(file_path, hash_file)` function verifies the integrity of a specific binary file, calculates its SHA-256 hash, and compares it with the previously stored hash in a log file. Additionally, it records the new hash along with a timestamp and a status indicating whether the file has been modified or not.

### Parameters:
- `file_path`: The path of the binary file to be verified.
- `hash_file`: The path of the log file where hashes and their status are stored.

### Usage:
The script can be executed from the terminal by providing the path of the file to be verified as an argument. For example:

```bash
python3 verify_integrity.py /path/to/file
