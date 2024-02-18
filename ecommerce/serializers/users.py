from ecommerce.models.users import CustomerProfile
from rest_framework import serializers
from django.contrib.auth.models import User

class CustomerRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomerProfile
        fields = ['id', 'full_name', 'Id_number', 'email', 'phone_number', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User.objects.create_user(username=validated_data['email'], email=validated_data['email'], password=password)
        customer = CustomerProfile.objects.create(user=user, **validated_data)
        return customer
