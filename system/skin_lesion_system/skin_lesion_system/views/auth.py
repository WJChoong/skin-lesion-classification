from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..models.model import User
import json
from django.db import connection
import hashlib
import base64
import random
import string
import uuid
import os
from ..common.message import failMessage, successMessage
from ..common.send_email import send_email
from ..common.email_templates.reset_password_email import reset_password_email_template
from dotenv import load_dotenv

load_dotenv()
front_end_url = os.getenv('FRONT_END_URL')
salt = os.getenv('SALT')
print(f"salt: {salt}")

def generateId():
    return uuid.uuid4()

def hash_password(password, salt):
    salt_bytes = salt.encode('utf-8')

    hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt_bytes, 100000)

    return base64.b64encode(hashed_password).decode('utf-8')

def verify_password(stored_hash, salt, password_to_check):
    # Hash the password to check
    new_hash = hash_password(password_to_check, salt)
    return new_hash == stored_hash

def generatePassword(length=12, safe_characters=None):
    if safe_characters is None:
        safe_characters = string.ascii_letters + string.digits + "!@$%"

    required_characters = [
        random.choice(string.ascii_lowercase),
        random.choice(string.ascii_uppercase),
        random.choice(string.digits),
        random.choice("!@$%")
    ]

    remaining_length = length - len(required_characters)
    random_characters = [random.choice(safe_characters) for _ in range(remaining_length)]

    password_characters = required_characters + random_characters
    random.shuffle(password_characters)

    password = ''.join(password_characters)

    return password

##############################################################################################
############################     API FUNCTION       ##########################################
##############################################################################################

@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            email = data.get('email')
            password = data.get('password')
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data.'}, status=400)

        if email and password:
            with connection.cursor() as cursor:
                sql_query = "SELECT id FROM user WHERE email = %s AND status = 1"
                cursor.execute(sql_query, [email])
                custom_data = cursor.fetchone()
                cursor.close()

            if custom_data:
                user_id = custom_data[0]
                print(f"custom_field_value: {user_id}")
                with connection.cursor() as cursor:
                    sql_query = "SELECT password, level FROM auth WHERE user_id = %s AND status = 1"
                    cursor.execute(sql_query, [user_id])
                    custom_data = cursor.fetchone()
                    cursor.close()
                    
                    if custom_data:
                        db_password = custom_data[0]
                        level = custom_data[1]
                        print(f"password: {password}")
                        print(f"db_password: {db_password}")
                        
                        is_correct = verify_password(db_password, salt, password)

                        if is_correct:
                            return successMessage('Login successful.', { "level": level, "user_id": user_id})
                        else:
                            return failMessage('Email and password do not match.')
                    else:
                        return failMessage('Invalid User.')
            else:
                return failMessage('Invalid User.')
        else:
            return failMessage('Email and password are required.')
    else:
        return failMessage('Invalid request method.')
    
@csrf_exempt
def resetPassword(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            email = data.get('email')
        except json.JSONDecodeError:
            return failMessage('Invalid JSON data.')

        if email:
            with connection.cursor() as cursor:
                # Check if the user exists
                sql_query = "SELECT id FROM user WHERE email = %s AND status = 1"
                cursor.execute(sql_query, [email])
                user_data = cursor.fetchone()
                cursor.close()

                if user_data:
                    user_id = user_data[0]
                    # Generate a new password
                    new_password = generatePassword()
                    print(f"New Password: {new_password}")
                    hashed_password = hash_password(new_password, salt)
                    print(f"Hashed Password: {hashed_password}")
                    
                    # Update the password in the database
                    with connection.cursor() as cursor:
                        sql_query = "UPDATE auth SET password = %s WHERE user_id = %s AND status = 1"
                        cursor.execute(sql_query, [hashed_password, user_id])
                        cursor.close()

                    # Send the new password via email
                    email_message = send_email("Password Reset", reset_password_email_template(email, new_password, f'{front_end_url}/#/login'), email)

                    if email_message:
                        return successMessage('Password reset successfully. Please check your email.')
                    else:
                        return failMessage('Failed to send reset password email.')
                else:
                    return failMessage('User not found.')
        else:
            return failMessage('Email is required.')
    else:
        return failMessage('Invalid request method.')
    
@csrf_exempt
def changePassword(request):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body.decode('utf-8'))
            user_id = data.get('user_id')
            old_password = data.get('old_password')
            new_password = data.get('new_password')
        except json.JSONDecodeError:
            return failMessage('Invalid JSON data.')

        print(f"user_id: {user_id}")
        print(f"old_password: {old_password}")
        print(f"new_password: {new_password}")
        if user_id and old_password and new_password:
            with connection.cursor() as cursor:
                sql_query = "SELECT id FROM user WHERE id = %s AND status = 1 "
                cursor.execute(sql_query, [user_id])
                user_data = cursor.fetchone()

            if user_data:
                with connection.cursor() as cursor:
                    sql_query = "SELECT password FROM auth WHERE user_id = %s AND status = 1 "
                    cursor.execute(sql_query, [user_id])
                    password_data = cursor.fetchone()

                    if password_data:
                        db_password = password_data[0]
                        is_correct = verify_password(db_password, salt, old_password)
                        print(f"is_correct: {is_correct}")
                        if is_correct:
                            print(f"user_id: {user_id}")
                            hashed_new_password = hash_password(new_password, salt)
                            print(f"hashed_new_password: {hashed_new_password}")
                            sql_query = "UPDATE auth SET password = %s WHERE user_id = %s AND status = 1"
                            cursor.execute(sql_query, [hashed_new_password, user_id])
                            return successMessage('Password changed successfully.')
                        else:
                            print("ghello guys")
                            return failMessage('Old password is incorrect.')
                    else:
                        return failMessage('Invalid User.')
            else:
                return failMessage('Invalid User.')
        else:
            return failMessage('Email, old password, and new password are required.')
    else:
        return failMessage('Invalid request method.')