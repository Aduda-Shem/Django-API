from django.shortcuts import render
from rest_framework.authtoken.models import Token

def profile_view(request):
    user = request.user

    return render(request, 'account/profile.html', {'user': user, 'token': ""})
