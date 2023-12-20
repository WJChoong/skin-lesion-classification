# skin_detection/views.py

from django.shortcuts import render
import numpy as np
from ..forms.form import ImageUploadForm
from ..models.model import ImageModel
import os
import csv
from django.conf import settings
from django.http import HttpResponse, JsonResponse
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from keras.preprocessing.image import load_img, img_to_array

model = load_model('./skin_lesion_system/ml_model/vgg16.h5')

@csrf_exempt
def check_lesion(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        fs = FileSystemStorage(location='media/unlabelled')
        filename = fs.save(image.name, image)
        uploaded_file_url = fs.url(filename)
        
        # Placeholder logic to generate a sentence
        # You should replace this with actual processing logic
         # Preprocess the uploaded image
        img_full_path = os.path.join(settings.MEDIA_ROOT, 'unlabelled', filename)
        print(f" -------------- {img_full_path} -------------")
        img = image.load_img(img_full_path, target_size=(224, 224))  # Adjust target size to match model's expected input
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)  # Model expects a batch of images
        img_array /= 255.0  # Scale pixel values to [0, 1]

        # # Predict the class of the image
        # prediction = model.predict(img_array)
        # predicted_class = np.argmax(prediction, axis=-1)  # Adjust if your model outputs different results

        # # You can map the predicted class index to an actual label
        # label_map = {0: 'Class A', 1: 'Class B', 2: 'Class C'}  # Replace with your actual labels
        # predicted_label = label_map[predicted_class[0]]
        
        
        sentence = "Thank you for uploading the image."
        
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
