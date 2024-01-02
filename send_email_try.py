import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

sender_app_password = os.getenv('GMAIL_APP_PASSWORD')
sender_email = os.getenv('SENDER_EMAIL')
front_end_url = os.getenv('FRONT_END_URL')
print(f"password: {sender_app_password}")
print(f"sender_email: {sender_email}")
print(f"front_end_url: {front_end_url}")
receiver_email="weijiec08@gmail.com"

def send_html_email(subject, html_content, to_email):

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

        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

# HTML content for the email
def login_email_template(receiver_email, user_password, login_url):
    return f"""
<html>
  <head>
    <style>
      body {{font-family: Arial, sans-serif; background-color: #f4f4f4; color: #333; line-height: 1.6;}}
      .container {{width: 80%; margin: 20px auto; padding: 20px; background-color: #fff; border-radius: 10px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);}}
      h2 {{color: #0056b3;}}
      p {{margin-bottom: 10px;}}
      .footer {{font-size: 0.8em; text-align: center; color: #666;}}
      .button {{
            display: inline-block; 
            padding: 10px 15px; 
            margin-top: 15px; 
            background-color: #0056b3; 
            color: #fff; /* Text color set to white */
            border-radius: 5px; 
            text-decoration: none;
        }}
    </style>
  </head>
  <body>
    <div class="container">
      <h2>Welcome to Our Service!</h2>
      <p>You have been successfully registered. Here are your login details:</p>
      <p><strong>Username:</strong> {receiver_email}</p>
      <p><strong>Password:</strong> {user_password}</p>
      <a href="{login_url}" style="display: inline-block; padding: 10px 15px; margin-top: 15px; background-color: #0056b3; color: #ffffff; border-radius: 5px; text-decoration: none;">Login Now</a>
      <p class="footer">If you have any questions, please contact our support team.</p>
    </div>
  </body>
</html>
"""

# Usage example
send_html_email("Welcome! Your Account Details", login_email_template(receiver_email, 'password@1234', f'{front_end_url}/#/login'), receiver_email)