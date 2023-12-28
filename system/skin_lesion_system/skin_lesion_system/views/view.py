# skin_detection/views.py

import base64
import uuid
from django.shortcuts import render
import numpy as np
# from ..forms.form import ImageUploadForm
# from ..models.model import ImageModel
import os
import csv
from django.conf import settings
from django.http import HttpResponse, JsonResponse
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
#from keras.preprocessing.image import load_img, img_to_array

model = load_model('./skin_lesion_system/ml_model/vgg16.h5')

@csrf_exempt
def check_lesion(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        print(image.name)
        fs = FileSystemStorage(location='media/unlabelled')
        filename = fs.save(image.name, image)
        uploaded_file_url = fs.url(filename)
        
        # Placeholder logic to generate a sentence
        # You should replace this with actual processing logic
         # Preprocess the uploaded image
        img_full_path = os.path.join(settings.MEDIA_ROOT, 'unlabelled', filename)
        print(f" -------------- {img_full_path} -------------")
        img = load_img(img_full_path, target_size=(224, 224, 3))  # Adjust target size to match model's expected input
        img_array = img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)  # Model expects a batch of images
        img_array /= 255.0  # Scale pixel values to [0, 1]

        # Predict the class of the image
        prediction = model.predict(img_array)
        predicted_class = np.argmax(prediction, axis=-1)  # Adjust if your model outputs different results

        # # You can map the predicted class index to an actual label
        label_map = {0: 'Class A', 1: 'Class B', 2: 'Class C'}  # Replace with your actual labels
        predicted_label = label_map[predicted_class[0]]
        
        sentence = "It is a "+predicted_label+" images"
        
        return JsonResponse({
            'message': sentence,
            'image_url': uploaded_file_url
        }, status=200)
        
        # return JsonResponse({
        #     'message': sentence,
        #     'image_url': uploaded_file_url
        # })
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    
# def get_images(request):
#     image_folder = os.path.join(settings.MEDIA_ROOT, 'unlabelled')
#     image_files = [f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
#     image_urls = [os.path.join(settings.MEDIA_URL, f) for f in image_files]
#     print(f'images_url: --- {image_urls}---')
#     return JsonResponse({'images': image_urls})

def get_images(request):
    image_folder = os.path.join(settings.MEDIA_ROOT, 'unlabelled')
    image_files = [f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]

    # Generate random IDs for each image
    image_ids = [str(uuid.uuid4()) for _ in image_files]
    
    image_data = []
    
    for file_name, image_id in zip(image_files, image_ids):
        with open(os.path.join(image_folder, file_name), "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            image_data.append({'id': image_id, 'image': f"data:image/jpeg;base64,{encoded_string}"})

    return JsonResponse({'images': image_data})