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
from ..common.message import failMessage, successMessage

salt = 'ThisIsMyFYP'

def generateId():
    return uuid.uuid4()

def hash_password(password, salt):
    # Ensure the salt is in byte format
    salt_bytes = salt.encode('utf-8')

    # PBKDF2 with 100,000 iterations and SHA-256 as the hash function
    hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt_bytes, 100000)

    # Return the hashed password in a readable format
    return base64.b64encode(hashed_password).decode('utf-8')

def verify_password(stored_hash, salt, password_to_check):
    # Hash the password to check
    new_hash = hash_password(password_to_check, salt)

    return new_hash == stored_hash

def generatePassword(length=12, safe_characters=None):
    if safe_characters is None:
        # Define a default set of safe characters (excluding sensitive ones)
        safe_characters = string.ascii_letters + string.digits + "!@$%"

    # Make sure we have at least one character from each category
    required_characters = [
        random.choice(string.ascii_lowercase),
        random.choice(string.ascii_uppercase),
        random.choice(string.digits),
        random.choice("!@$%")
    ]

    # Generate the rest of the password
    remaining_length = length - len(required_characters)
    random_characters = [random.choice(safe_characters) for _ in range(remaining_length)]

    # Combine required and random characters, then shuffle them
    password_characters = required_characters + random_characters
    random.shuffle(password_characters)

    # Convert the list of characters into a string
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
            # Now you can execute a raw SQL query to retrieve additional data
            with connection.cursor() as cursor:
                sql_query = "SELECT id FROM user WHERE email = %s"
                cursor.execute(sql_query, [email])
                custom_data = cursor.fetchone()
                cursor.close()

            if custom_data:
                user_id = custom_data[0]
                print(f"custom_field_value: {user_id}")
                with connection.cursor() as cursor:
                    sql_query = "SELECT password FROM auth WHERE user_id = %s"
                    cursor.execute(sql_query, [user_id])
                    custom_data = cursor.fetchone()
                    cursor.close()
                    
                    if custom_data:
                        db_password = custom_data[0]
                        print(f"password: {password}")
                        print(f"db_password: {db_password}")
                        hashed_password = hash_password(password, salt)
                        print(f"hashed_password: {hashed_password}")
                        
                        is_correct = verify_password(hashed_password, salt, password)

                        if is_correct:
                            return JsonResponse({'status': 'success', 'message': 'Login successful.'}, status=200)
                        else:
                            return JsonResponse({'status': 'error', 'message': 'Email and password do not match.'}, status=400)
                    else:
                        return JsonResponse({'status': 'error', 'message': 'Invalid User.'}, status=400)
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid User.'}, status=400)
        else:
            return JsonResponse({'status': 'error', 'message': 'Email and password are required.'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)
    
def resetPassword(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            email = data.get('email')
            password = data.get('password')
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data.'}, status=400)

        if email and password:
            # Now you can execute a raw SQL query to retrieve additional data
            with connection.cursor() as cursor:
                sql_query = "SELECT id FROM user WHERE email = %s"
                cursor.execute(sql_query, [email])
                custom_data = cursor.fetchone()
                cursor.close()

        #     if custom_data:
        #         user_id = custom_data[0]
        #         print(f"custom_field_value: {user_id}")
        #         with connection.cursor() as cursor:
        #             sql_query = "SELECT password FROM auth WHERE user_id = %s"
        #             cursor.execute(sql_query, [user_id])
        #             custom_data = cursor.fetchone()
        #             cursor.close()
                    
        #             if custom_data:
        #                 db_password = custom_data[0]
        #                 print(f"password: {password}")
        #                 print(f"db_password: {db_password}")
        #                 hashed_password = hash_password(password, salt)
        #                 print(f"hashed_password: {hashed_password}")
                        
        #                 is_correct = verify_password(hashed_password, salt, password)

        #                 if is_correct:
        #                     return JsonResponse({'status': 'success', 'message': 'Login successful.'}, status=200)
        #                 else:
        #                     return JsonResponse({'status': 'error', 'message': 'Email and password do not match.'}, status=400)
        #             else:
        #                 return JsonResponse({'status': 'error', 'message': 'Invalid User.'}, status=400)
        #     else:
        #         return JsonResponse({'status': 'error', 'message': 'Invalid User.'}, status=400)
        else:
            return JsonResponse({'status': 'error', 'message': 'Email and password are required.'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)
    
@csrf_exempt
def changePassword(request):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body.decode('utf-8'))
            email = data.get('email')
            old_password = data.get('old_password')
            new_password = data.get('new_password')
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data.'}, status=400)

        if email and old_password and new_password:
            with connection.cursor() as cursor:
                sql_query = "SELECT id FROM user WHERE email = %s"
                cursor.execute(sql_query, [email])
                user_data = cursor.fetchone()

            if user_data:
                user_id = user_data[0]
                with connection.cursor() as cursor:
                    sql_query = "SELECT password FROM auth WHERE user_id = %s"
                    cursor.execute(sql_query, [user_id])
                    password_data = cursor.fetchone()

                    if password_data:
                        db_password = password_data[0]
                        if verify_password(db_password, salt, old_password):
                            hashed_new_password = hash_password(new_password, salt)
                            sql_query = "UPDATE auth SET password = %s WHERE user_id = %s"
                            cursor.execute(sql_query, [hashed_new_password, user_id])
                            return successMessage('Password changed successfully.')
                        else:
                            return failMessage('Old password is incorrect.')
                    else:
                        return failMessage('Invalid User.')
            else:
                return failMessage('Invalid User.')
        else:
            return failMessage('Email, old password, and new password are required.')
    else:
        return failMessage('Invalid request method.')