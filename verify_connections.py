import unittest
from unittest.mock import patch
import subprocess

def verify_logged_in_users():
    """Verify the users currently logged in and their origins."""
    try:
        # Run the 'who' command to get the list of logged-in users
        result = subprocess.run(['who'], capture_output=True, text=True, check=True)

        # Extract and print the username and origin for each logged-in user
        print("Logged-in users:")
        for line in result.stdout.splitlines():
            print(line)

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

def main():
    verify_logged_in_users()



if __name__ == "__main__":
    main()
