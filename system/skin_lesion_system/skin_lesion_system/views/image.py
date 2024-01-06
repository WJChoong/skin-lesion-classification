# skin_detection/views.py

import base64
import json
import uuid
from django.shortcuts import render
import numpy as np
import os
import csv
from django.conf import settings
from django.http import HttpResponse, JsonResponse
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
#from keras.preprocessing.image import load_img, img_to_array
from datetime import datetime
from .auth import generateId
from ..common.message import successMessage, failMessage

model = load_model('./skin_lesion_system/ml_model/vgg16.h5')     

def preprocess_image(image_path):
    # Load and resize the image
    img = load_img(image_path, target_size=(224, 224, 3))
    img_array = img_to_array(img)

    # Normalize the image (adjust this according to how you trained your model)
    img_array = img_array / 255.0

    # Add a batch dimension
    img_array = np.expand_dims(img_array, axis=0)

    return img_array   

@csrf_exempt
def checkLesion(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        # Extract the file extension from the original image name
        original_extension = os.path.splitext(image.name)[1]
        # Get the current timestamp
        current_timestamp = datetime.now()
        new_filename = f"{current_timestamp.strftime('%Y%m%d%H%M%S')}{original_extension}"
        print("New filename:", new_filename)
        fs = FileSystemStorage(location='media/unlabelled')
        filename = fs.save(new_filename, image)
        imageId = generateId()
        
        try:
            with connection.cursor() as cursor:
                sql_query = "INSERT INTO image (id, name, status) VALUES (%s, %s, %s)"
                cursor.execute(sql_query, [imageId, filename, 1])
                cursor.close()
        except Exception as e:
            print(f"Database error: {e}")
            return failMessage('Database error', 500)
        
        # Preprocess the uploaded image
        img_full_path = os.path.join(settings.MEDIA_ROOT, 'unlabelled', filename)
        img = preprocess_image(img_full_path)

        # Predict the class of the image
        prediction = model.predict(img)
        predicted_class = np.argmax(prediction, axis=-1)  # Adjust if your model outputs different results

        # # You can map the predicted class index to an actual label
        label_map = {0: 'Melanoma', 1: 'Melanocytic Nevus', 2: 'Bascal Cell Carcinoma', 3: 'Benign Keratosis', 4: 'Unkown'} 
        predicted_label = label_map[predicted_class[0]]
        
        return successMessage("It is a "+ predicted_label +" images")
    else:
        return failMessage('Invalid request', 500)

@csrf_exempt
def getImages(request):
    image_data = []
    try:
        with connection.cursor() as cursor:
            # Query to select the image ID and name from the database
            sql_query = """
            SELECT image.id, image.name 
            FROM image 
            LEFT JOIN category ON image.id = category.image_id
            WHERE image.status = 1 AND category.id IS NULL
            """
            cursor.execute(sql_query)
            images = cursor.fetchall()

            for image_id, image_name in images:
                image_path = os.path.join(settings.MEDIA_ROOT, 'unlabelled', image_name)
                
                # Ensure the file exists before trying to open it
                if os.path.exists(image_path):
                    with open(image_path, "rb") as image_file:
                        # Encode the image file as base64
                        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                        # Append the image data to the list
                        image_data.append({'id': image_id, 'image': f"data:image/jpeg;base64,{encoded_string}"})
                else:
                    print(f"File not found: {image_path}")

    except Exception as e:
        return failMessage('Database error', 500)
    
    return successMessage("Successfully get all images", image_data)

@csrf_exempt
def deleteImage(request):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body.decode('utf-8'))
            image_id = data.get('id')
        except json.JSONDecodeError:
            return failMessage('Invalid JSON data.')

        if image_id:
            # Check if the image exists
            with connection.cursor() as cursor:
                sql_query = "SELECT id FROM image WHERE id = %s AND status = 1"
                cursor.execute(sql_query, [image_id])
                existing_image = cursor.fetchone()

            if existing_image:
                # Soft delete the image
                with connection.cursor() as cursor:
                    current_time = datetime.now()
                    sql_query = """
                    UPDATE image
                    SET deleted_at = %s, status = 0
                    WHERE id = %s AND status = 1
                    """
                    cursor.execute(sql_query, [current_time, image_id])

                return successMessage('Image deleted successfully.')
            else:
                return failMessage('Image not found.')
        else:
            return failMessage('Image ID is required.')
    else:
        return failMessage('Invalid request method.')