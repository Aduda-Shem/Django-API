from ecommerce.models.orders import Order
from ecommerce.models.users import Customer
from rest_framework import serializers

class CustomerOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'full_name']

class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerOrderSerializer()

    class Meta:
        model = Order
        fields = ['uuid', 'customer', 'created_at', 'status', 'total_amount', 'products']
