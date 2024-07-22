import os

def read_last_n_lines(log_path: str, n: int) -> str:
    """
    Reads the last n lines of a log file.

    Args:
    log_path (str): Path to the log file.
    n (int): Number of lines to read from the end of the file.

    Returns:
    str: The last n lines of the log file.
    """
    if not os.path.exists(log_path):
        raise FileNotFoundError(f"The log file at {log_path} does not exist.")
    
    with open(log_path, 'r') as file:
        try:
            # Read all lines from the file
            lines = file.readlines()
            # Return the last n lines
            return ''.join(lines[-n:])
        except Exception as e:
            raise RuntimeError(f"An error occurred while reading the log file: {e}")
