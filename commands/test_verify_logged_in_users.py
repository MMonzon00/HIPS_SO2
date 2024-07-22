import unittest
from unittest.mock import patch
from commands.verify_connections import verify_logged_in_users
import subprocess

class TestVerifyLoggedInUsers(unittest.TestCase):
    
    @patch('verify_connections.subprocess.run')
    def test_multiple_users_logged_in(self, mock_subprocess):
        # Simulate output of 'who' command with multiple users logged in
        mock_subprocess.return_value.stdout = "user1 pts/0 2022-02-10 10:00 (:0)\nuser2 pts/1 2022-02-10 09:30 (:1)"
        verify_logged_in_users()
        # Assert that the correct output is printed
        self.assertTrue(mock_subprocess.called)
        self.assertEqual(mock_subprocess.call_count, 1)
    
    @patch('verify_connections.subprocess.run')
    def test_no_users_logged_in(self, mock_subprocess):
        # Simulate output of 'who' command with no users logged in
        mock_subprocess.return_value.stdout = ""
        verify_logged_in_users()
        # Assert that the correct output is printed
        self.assertTrue(mock_subprocess.called)
        self.assertEqual(mock_subprocess.call_count, 1)
    
    @patch('verify_connections.subprocess.run')
    def test_single_user_logged_in(self, mock_subprocess):
        # Simulate output of 'who' command with a single user logged in
        mock_subprocess.return_value.stdout = "user1 pts/0 2022-02-10 10:00 (:0)"
        verify_logged_in_users()
        # Assert that the correct output is printed
        self.assertTrue(mock_subprocess.called)
        self.assertEqual(mock_subprocess.call_count, 1)
    
    @patch('verify_connections.subprocess.run')
    def test_handle_errors(self, mock_subprocess):
        # Simulate an error condition when executing the 'who' command
        mock_subprocess.side_effect = subprocess.CalledProcessError(returncode=1, cmd="who")
        verify_logged_in_users()
        # Assert that the error is handled gracefully
        self.assertTrue(mock_subprocess.called)
        self.assertEqual(mock_subprocess.call_count, 1)

if __name__ == '__main__':
    unittest.main()
