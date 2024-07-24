import smtplib
from email.mime.text import MIMEText
import os
import logging
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(filename='/var/log/hips.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def log_event(event):
    logging.info(event)
    
def notify_admin(message):
    sender_email = os.getenv("EMAIL_USER")
    receiver_email = os.getenv("EMAIL_RECEIVER")
    smtp_server = "smtp.gmail.com"
    smtp_port = 465
    smtp_user = os.getenv("EMAIL_USER")
    smtp_password = os.getenv("EMAIL_PASSWORD")
    
    msg = MIMEText(message)
    msg['Subject'] = 'HIPS Alert'
    msg['From'] = sender_email
    msg['To'] = receiver_email
    
    try:
        # Use SMTP_SSL for port 465
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(smtp_user, smtp_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        log_event(f"Failed to send email: {e}")