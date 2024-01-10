import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

sender_app_password = os.getenv('GMAIL_APP_PASSWORD')
sender_email = os.getenv('SENDER_EMAIL')
print(f"password: {sender_app_password}")
print(f"sender_email: {sender_email}")

def send_email(subject, html_content, to_email):

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = to_email

    part = MIMEText(html_content, 'html')
    msg.attach(part)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, sender_app_password)
        server.send_message(msg)
        server.quit()

        return True
    except Exception as e:
        return False