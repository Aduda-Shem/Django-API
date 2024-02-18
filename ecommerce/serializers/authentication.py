from ecommerce.models.users import CustomerProfile
from rest_framework import serializers
from django.contrib.auth.models import User

class UserLoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password'] 

class CustomerProfileSerializer(serializers.ModelSerializer):
    user = UserLoginSerializer()

    class Meta:
        model = CustomerProfile
        fields = ['user', 'full_name', 'Id_number', 'email', 'phone_number']
