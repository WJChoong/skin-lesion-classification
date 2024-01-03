import json
from django.db import connection
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..common.message import failMessage, successMessage
from .auth import generateId

@csrf_exempt
def categoryImage(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            user_id = data.get('user_id')
            image_id = data.get('image_id')
            category = data.get('category')
            print(f"Image_id: {image_id}")
        except json.JSONDecodeError:
            return failMessage('Invalid JSON data.')

        print("here")
        if user_id and image_id:
            # Check if the user exists
            with connection.cursor() as cursor:
                # Check if the user exists
                cursor.execute("SELECT id FROM user WHERE id = %s AND status = 1", [user_id])
                user_exists = cursor.fetchone()
                print(f"Retrieved User ID from DB: {user_exists}")  # Print user_id from database for debugging

            with connection.cursor() as cursor:
                # Check if the image exists
                cursor.execute("SELECT id FROM image WHERE id = %s AND status = 1", [image_id])
                image_exists = cursor.fetchone()
                print(f"Retrieved Image ID from DB: {image_exists}")  # Print image_id from database for debugging

            if not user_exists or not image_exists:
                return failMessage('User or Image does not exist.')
            
            # Generate a unique ID for the category entry
            category_id = generateId()

            # Insert data into the category table
            with connection.cursor() as cursor:
                sql_query = "INSERT INTO category (id, user_id, image_id, category, status) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql_query, [category_id, user_id, image_id, category, 1]) 
                cursor.close()

            return successMessage('Category image linked successfully.')
        else:
            return failMessage('User ID and Image ID are required.')
    else:
        return failMessage('Invalid request method.')
