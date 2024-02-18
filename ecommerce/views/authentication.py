from ecommerce.models.users import CustomerProfile
from ecommerce.serializers.authentication import CustomerProfileSerializer, UserLoginSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from knox.models import AuthToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

class LoginView(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')

        if not email:
            return Response({'message': 'E-mail is Required'}, status=status.HTTP_400_BAD_REQUEST)

        if not password:
            return Response({'message': 'Password is Required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"message":"User does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        if not check_password(password=password, encoded=user.password):
            return Response({"message": "Invalid credentials!, please try again."}, status=status.HTTP_400_BAD_REQUEST)

        profile = CustomerProfile.objects.filter(user=user).first()


        return Response({
            'message': 'Login successful',
            'user': self.serializer_class(user).data,
            'profile': CustomerProfileSerializer(profile).data,
            'token': AuthToken.objects.create(user=user)[1],
        }, status=status.HTTP_200_OK)