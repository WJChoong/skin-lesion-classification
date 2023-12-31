from django.http import JsonResponse

def failMessage(message):
    return JsonResponse({'status': 'error', 'message': message}, status=400)

def successMessage(message, data=None):
    return JsonResponse({'status': 'success', 'message': message, 'data': data}, status=201)