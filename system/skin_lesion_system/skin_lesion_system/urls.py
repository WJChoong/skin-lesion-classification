"""
URL configuration for skin_lesion_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import image as image_views
from .views import auth as auth_views
from .views import user as user_views
from .views import category as category_views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('images/get/', image_views.getImages, name='get_images'),
    path('images/upload/', image_views.check_lesion, name='upload_image'),
    path('images/delete/', image_views.deleteImages, name='delete_images'),
    
    path('auth/login/', auth_views.login, name='login'),
    path('auth/reset/', auth_views.resetPassword, name='reset_passwords'),
    path('auth/change/', auth_views.changePassword, name='change_passwords'),
    
    path('user/get/all/', user_views.getAllUsers, name='get_users'),
    path('user/get/user/', user_views.getUserDetails, name='get_users'),
    path('user/create/', user_views.createUser, name='create_user'),
    path('user/update/', user_views.updateUser, name='update_user'),
    path('user/delete/', user_views.deleteUser, name='delete_user'),
    
    path('category/images/', category_views.categoryImage, name='category_data'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

