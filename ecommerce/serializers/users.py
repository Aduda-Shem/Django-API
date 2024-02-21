from ecommerce.models.users import Customer
from rest_framework import serializers

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['full_name', 'code', 'phone_number', 'date_created']