from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..models.model import User
import json
from django.db import connection
import hashlib
import base64

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

salt = 'ThisIsMyFYP'

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