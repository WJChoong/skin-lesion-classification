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
      <a href="http://localhost:8080/#/login" style="display: inline-block; padding: 10px 15px; margin-top: 15px; background-color: #0056b3; color: #ffffff; border-radius: 5px; text-decoration: none;">Login Now</a>
      <p class="footer">If you have any questions, please contact our support team.</p>
    </div>
  </body>
</html>
"""