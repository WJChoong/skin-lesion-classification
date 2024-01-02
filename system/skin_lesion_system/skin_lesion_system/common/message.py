from django.http import JsonResponse

def failMessage(message, status=400):
    return JsonResponse({'status': 'error', 'message': message}, status=status)

def successMessage(message, data=None):
    return JsonResponse({'status': 'success', 'message': message, 'data': data}, status=201)