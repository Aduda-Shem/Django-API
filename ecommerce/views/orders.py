import threading
from ecommerce.models.orders import CartItem, Order, OrderItem, ShoppingCart
from ecommerce.models.products import Product
from ecommerce.models.users import User
from ecommerce.serializers.orders import CartItemSerializer, OrderItemSerializer, OrderSerializer, ShoppingCartSerializer
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage

import os
import requests
from django.conf import settings
from rest_framework import status
from environ import Env

env = Env()

class ShoppingCartView(generics.GenericAPIView):
    """
    This is a Class-based View for managing the shopping cart
    """
    serializer_class = ShoppingCartSerializer

    def get(self, request):
        user = request.user
        try:
            shopping_cart = ShoppingCart.objects.get(user=user)
        except ShoppingCart.DoesNotExist:
            return Response({
                "message": "Shopping cart does not exist."
                }, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(shopping_cart)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        shopping_cart, created = ShoppingCart.objects.get_or_create(user=user)
        serializer = self.serializer_class(shopping_cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


"""
Function to send message in a seperate thread when order is sent
"""
def send_sms(phone_number, message):
    url = settings.AFRICASTALKING_URL
    username = settings.AFRICASTALKING_USERNAME
    api_key = settings.AFRICASTALKING_API_KEY
    sender_id = settings.AFRICASTALKING_SENDER_ID

    headers = {
        'ApiKey': api_key,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }
    data = {
        'username': username,
        'from': sender_id,
        'message': message,
        'to': phone_number
    }

    try:
        response = requests.post(url=url, headers=headers, data=data)
        response_data = response.json()
        if response.status_code == 201:
            return response_data
        else:
            return None
    except Exception as e:
        return None

class OrderView(generics.GenericAPIView):
    """
    This is a Class-based View for managing orders
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        q = self.request.query_params.get("q")
        status_filter = self.request.query_params.get("status")
        queryset = Order.objects.filter(user=self.request.user)
        
        if q:
            queryset = queryset.filter(name__icontains=q)
        
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset.order_by('id')

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Pagination
        page_number = request.query_params.get('page', 1)
        rows = request.query_params.get('rows', 10)

        paginator = Paginator(queryset, rows)

        try:
            orders_page = paginator.page(page_number)
        except EmptyPage:
            return Response({
                "message": "Invalid page number"
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(orders_page, many=True)
        return Response({
            'message': "Orders have been fetched successfully",
            'orders': serializer.data,
            "pagination": {
                "currentPage": page_number,
                "total": paginator.count,
                "pageSize": rows
            }
        }, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        formData = request.data
        total_amount = formData.get('total_amount')
        status = formData.get('status')

        try:
            customer_profile = User.objects.get(user=user)
            phone_number = customer_profile.phone_number
        except User.DoesNotExist:
            phone_number = None

        order = Order.objects.create(
            user=user,
            total_amount=total_amount,
            status=status
        )

        order_items = OrderItem.objects.filter(order=order)

        message = f"Your order has been created:\n\n"
        message += f"Total Amount: {total_amount}\n"
        message += f"Status: {status}\n\n"
        message += "Order Items:\n"
        for item in order_items:
            message += f"- {item.product.name} x {item.quantity}\n"

        serializer = self.serializer_class(order)


        if phone_number:
            sms_thread = threading.Thread(target=self.send_sms, args=(phone_number, message))
            sms_thread.start()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CartItemView(generics.GenericAPIView):
    """
    This is a Class-based View for managing cart items
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CartItemSerializer

    def post(self, request):
        formData = request.data
        product_id = formData.get('product')
        shopping_cart_id = formData.get('shopping_cart')
        quantity = formData.get('quantity')

        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({"message": "Product does not exist."}, status=status.HTTP_404_NOT_FOUND)

        try:
            shopping_cart = ShoppingCart.objects.get(pk=shopping_cart_id)
        except ShoppingCart.DoesNotExist:
            return Response({"message": "Shopping cart does not exist."}, status=status.HTTP_404_NOT_FOUND)

        cart_item = CartItem.objects.create(
            product=product,
            shopping_cart=shopping_cart,
            quantity=quantity
        )
        serializer = self.serializer_class(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, pk=None):
        try:
            cart_item = CartItem.objects.get(pk=pk)
        except CartItem.DoesNotExist:
            return Response({"message": "Cart item does not exist."}, status=status.HTTP_404_NOT_FOUND)

        formData = request.data
        product_id = formData.get('product')
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({
                "message": "Product does not exist."}, 
                                )
        cart_item.product = product

        quantity = request.data.get('quantity')
        if quantity:
            cart_item.quantity = quantity

        cart_item.save()

        serializer = self.serializer_class(cart_item)
        return Response(serializer.data)

    def delete(self, request, pk=None):
        try:
            cart_item = CartItem.objects.get(pk=pk)
        except CartItem.DoesNotExist:
            return Response({"message": "Cart item does not exist."}, status=status.HTTP_404_NOT_FOUND)

        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderItemView(generics.GenericAPIView):
    """
    This is a Class-based View for managing order items
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderItemSerializer

    def post(self, request):
        formData = request.data
        order_id = formData.get('order')
        product_id = formData.get('product')
        quantity = formData.get('quantity')

        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            return Response({"message": "Order does not exist."}, status=status.HTTP_404_NOT_FOUND)

        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({"message": "Product does not exist."}, status=status.HTTP_404_NOT_FOUND)

        order_item = OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity
        )
        serializer = self.serializer_class(order_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, pk=None):
        try:
            order_item = OrderItem.objects.get(pk=pk)
        except OrderItem.DoesNotExist:
            return Response({"message": "Order item does not exist."}, status=status.HTTP_404_NOT_FOUND)

        quantity = request.data.get('quantity')
        if quantity:
            order_item.quantity = quantity

        order_item.save()

        serializer = self.serializer_class(order_item)
        return Response(serializer.data)

    def delete(self, request):
        try:
            order_item = request.query_params.get('id')
            order_item = OrderItem.objects.get(pk=order_item)
            order_item.delete()

            return Response({
                'message': 'OrderItem deleted successfully',
            }, status=status.HTTP_200_OK)
        except OrderItem.DoesNotExist:
            return Response({'error': 'OrderItem not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            content = {'error': 'Error deleting the OrderItem'}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

