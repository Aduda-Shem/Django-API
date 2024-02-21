from rest_framework.response import Response
from rest_framework import status

def oauth_openid_callback(request):
    code = request.GET.get('code')
    print("CODE: ", code)

    if code is None:
        return Response({"status": status.HTTP_400_BAD_REQUEST, 
                         "message": "Authorization Code absent."}, 
                         status=status.HTTP_400_BAD_REQUEST)
    params = {
        "code": code
    }
    return Response({"status": status.HTTP_200_OK, 
                     "message": "Authorization Code Generated Successfully!", 
                     "results": params})
