from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def get_users(request):
    return True

def create_user(request):
    return True

def delete_user(request):
    return True

def update_user(request):
    return True