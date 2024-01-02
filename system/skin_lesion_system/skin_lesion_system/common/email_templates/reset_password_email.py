def reset_password_email_template(email, new_password, login_url):
    # HTML content with added CSS for styling
    return f"""
    <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    color: #333;
                    line-height: 1.6;
                }}
                .container {{
                    max-width: 600px;
                    margin: 20px auto;
                    padding: 20px;
                    background: #fff;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                h2 {{
                    color: #0056b3;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 20px;
                    font-size: 0.8em;
                    color: #666;
                }}
                .button {{
                    display: inline-block;
                    margin-top: 20px;
                    padding: 10px 20px;
                    background-color: #0056b3;
                    color: #fff;
                    text-decoration: none;
                    border-radius: 5px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Password Reset Notification</h2>
                <p>Hello,</p>
                <p>Your password has been successfully reset. Below are your new login credentials:</p>
                <table>
                    <tr><td><strong>Email:</strong></td><td>{email}</td></tr>
                    <tr><td><strong>New Password:</strong></td><td>{new_password}</td></tr>
                </table>
                <p>Please use this new password to log in to your account. For security reasons, we strongly recommend you change your password after logging in.</p>
                <a href="{login_url}" style="display: inline-block; padding: 10px 15px; margin-top: 15px; background-color: #0056b3; color: #ffffff; border-radius: 5px; text-decoration: none;">Login to Your Account</a>
                <p class="footer">If you did not request a password reset, please contact our support team immediately.</p>
            </div>
            <div class="footer">
                Best regards,<br>
                Your Support Team
            </div>
        </body>
    </html>
    """