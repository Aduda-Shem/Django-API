from django.http import JsonResponse
# Functions to print the Authorization code 
def oauth_openid_callback(request):
    code = request.GET.get('code')

    if not code:
        return JsonResponse({"status": "error", "message": "Authorization Code absent."}, status=400)

    return JsonResponse({"status": "success", "message": "Authorization Code received successfully!", "code": code})
