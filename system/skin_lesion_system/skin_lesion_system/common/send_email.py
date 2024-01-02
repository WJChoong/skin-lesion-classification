import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()
# load_dotenv(dotenv_path)

sender_app_password = os.getenv('GMAIL_APP_PASSWORD')
sender_email = os.getenv('SENDER_EMAIL')
print(f"password: {sender_app_password}")
print(f"sender_email: {sender_email}")

def send_email(subject, html_content, to_email):

    # Create a MIMEMultipart object to represent the email
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = to_email

    # Create a MIMEText object for the HTML content
    part = MIMEText(html_content, 'html')
    msg.attach(part)

    # Try to send the email
    try:
        # Connect to Gmail's SMTP server
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, sender_app_password)
        server.send_message(msg)
        server.quit()

        return True
    except Exception as e:
        return False