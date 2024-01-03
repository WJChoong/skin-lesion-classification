from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db import connection
import json
import os
from .auth import generatePassword, hash_password, generateId
from ..common.message import failMessage, successMessage
from ..common.send_email import send_email
from ..common.email_templates.login_email import login_email_template
from dotenv import load_dotenv

load_dotenv()
front_end_url = os.getenv('FRONT_END_URL')
salt = os.getenv('SALT')
print(f"front_end_url: {front_end_url}")
print(f"salt2: {salt}")

@csrf_exempt
def getAllUsers(request):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            sql_query = """
                SELECT u.id, u.email, u.name, u.country
                FROM user u
                LEFT JOIN auth a ON u.id = a.user_id
                WHERE u.status = 1
                AND (a.level IS NULL OR a.level != 1)
            """
            cursor.execute(sql_query)
            users_data = cursor.fetchall()
            cursor.close()

        users_list = []
        print(f'users_data: {users_data}')
        for user_data in users_data:
            id, email, name, country = user_data
            users_list.append({'id': id, 'name': name, 'email': email, 'country': country})
        return successMessage('Successfully get all users', users_list)
    else:
        return failMessage('Invalid request method.')

@csrf_exempt
def getUserDetails(request):
    if request.method == 'GET':
        try:
            id = request.GET.get('id')
        except json.JSONDecodeError:
            print("Invalid JSON")
            return failMessage('Invalid JSON data.')
        
        print(f"id: {id}")
        if id: 
            with connection.cursor() as cursor:
                sql_query = "SELECT id, name, email, country FROM user WHERE id = %s"
                cursor.execute(sql_query, [id])
                custom_data = cursor.fetchone()
                cursor.close()

            if custom_data:
                id, name, email, country = custom_data
                user_data = {
                    'id': id,
                    'name': name,
                    'email': email,
                    'country': country
                }
                return successMessage('Successfully get data', user_data)
            else:
                return failMessage('Invalid User')
        return failMessage('User data is not found')
    else:
        return failMessage('Invalid request method.')

@csrf_exempt
def createUser(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            name = data.get('name')
            email = data.get('email')
            country = data.get('country')
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data.'}, status=400)

        if name and email and country:
            # Check if the email already exists
            with connection.cursor() as cursor:
                sql_query = "SELECT id FROM user WHERE email = %s AND status = 1"
                cursor.execute(sql_query, [email])
                existing_user = cursor.fetchone()
                cursor.close()

            if existing_user:
                return JsonResponse({'status': 'error', 'message': 'Email already exists.'}, status=400)
            else:
                authId = generateId()
                userId = generateId()
                password = generatePassword()
                print(f"-------------------------- password: {password} ----------------------")
                hashed_password = hash_password(password, salt)
            
                with connection.cursor() as cursor:
                    sql_query = "INSERT INTO user (id, name, email, country, status) VALUES (%s, %s, %s, %s, %s)"
                    cursor.execute(sql_query, [userId, name, email, country, 1])
                    cursor.close()
                with connection.cursor() as cursor:
                    sql_query = "INSERT INTO auth (id, user_id, password, level, status) VALUES (%s, %s, %s, %s, %s)"
                    cursor.execute(sql_query, [authId, userId, hashed_password, 2, 1])
                    cursor.close()
                
                email_message = send_email("Welcome! Your Account Details", login_email_template(email, password, f'{front_end_url}/#/login'), email)
                
                if email_message:
                    return successMessage('User created successfully.')
                else:
                    return failMessage('Fail to send email')
        else:
            return failMessage('Name, email, and country are required.')
    else:
        return failMessage('Invalid request method.')

@csrf_exempt
def updateUser(request):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body.decode('utf-8'))
            user_id = data.get('id')
            name = data.get('name')
            email = data.get('email')
            country = data.get('country')
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data.'}, status=400)

        if user_id and (name or email or country):
            # Check if the user exists
            with connection.cursor() as cursor:
                sql_query = "SELECT id FROM user WHERE id = %s AND status = 1"
                cursor.execute(sql_query, [user_id])
                existing_user = cursor.fetchone()
                cursor.close()

            if existing_user:
                # Update user data
                update_fields = []
                values = []

                if name:
                    update_fields.append("name = %s")
                    values.append(name)
                if email:
                    update_fields.append("email = %s")
                    values.append(email)
                if country:
                    update_fields.append("country = %s")
                    values.append(country)

                values.append(user_id)
                with connection.cursor() as cursor:
                    sql_query = f"UPDATE user SET {', '.join(update_fields)} WHERE id = %s"
                    cursor.execute(sql_query, values)
                    cursor.close()

                return successMessage('User updated successfully.')
            else:
                return failMessage('User not found.')
        else:
            return failMessage('User ID and at least one field to update are required.')
    else:
        return failMessage('Invalid request method.')

@csrf_exempt
def deleteUser(request):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body.decode('utf-8'))
            user_id = data.get('id')
        except json.JSONDecodeError:
            return failMessage('Invalid JSON data.')

        if user_id:
            # Check if the user exists
            with connection.cursor() as cursor:
                sql_query = "SELECT id FROM user WHERE id = %s AND status = 1"
                cursor.execute(sql_query, [user_id])
                existing_user = cursor.fetchone()

            if existing_user:
                # Update the user instead of deleting
                with connection.cursor() as cursor:
                    current_time = datetime.now()
                    sql_query = """
                    UPDATE user
                    SET deleted_at = %s, status = 0
                    WHERE id = %s AND status = 1
                    """
                    cursor.execute(sql_query, [current_time, user_id])

                return successMessage('User deleted successfully.')
            else:
                return failMessage('User not found.')
        else:
            return failMessage('User ID is required.')
    else:
        return failMessage('Invalid request method.')