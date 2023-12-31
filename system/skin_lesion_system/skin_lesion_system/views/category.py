from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def categoryImage(request):
    return True
