from decimal import Decimal
import threading
from ecommerce.models.products import Product
from ecommerce.serializers.orders import OrderSerializer
from ecommerce.utils.send_sms import send_sms
from rest_framework import generics, status
from rest_framework.response import Response
from ecommerce.models import Order
from django.core.paginator import Paginator, EmptyPage
from rest_framework.permissions import IsAuthenticated
from oauth2_provider.contrib.rest_framework import TokenHasScope

class OrderViewApi(generics.GenericAPIView):
    """
    Class Based View for managing orders
    """
    permission_classes = [IsAuthenticated, TokenHasScope]
    required_scopes = ['openid']    

    def get_queryset(self):
        return Order.objects.all()

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

        serialized_data = OrderSerializer(orders_page, many=True).data
        return Response({
            "message": "Orders Fetched Successfully!",
            "orders": serialized_data,
            "last_page": paginator.num_pages,
            "pagination": {
                "currentPage": page_number,
                "total": paginator.count,
                "pageSize": rows
            }
        }, status=status.HTTP_200_OK)


    def post(self, request):
        customer_id = request.data.get('customer')
        statuse = request.data.get('status')
        order_items = request.data.get('order_items', [])

        products_data = []
        for item in order_items:
            product_id = item.get('id')
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response({'error': f'Product with ID {product_id} does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

            product_data = {
                'id': product.id,
                'name': product.name,
                'price': str(product.price),
                'quantity': item.get('quantity')
            }
            products_data.append(product_data)

        order = Order.objects.create(
            customer_id=customer_id,
            status=statuse,
            products=products_data
        )

        # Send SMS in a separate thread
        customer_phone_number = order.customer.phone_number
        message = f"Dear {order.customer.full_name}, your order has been placed successfully. Thank you for shopping with us!"
        sms_thread = threading.Thread(target=send_sms, args=(customer_phone_number, message))
        sms_thread.start()

        order_data = OrderSerializer(order).data

        return Response({'message': 'Order created successfully', 'order': order_data}, status=status.HTTP_201_CREATED)
    
    def delete(self, request):
        order_id = request.data.get('order_id')
        if not order_id:
            return Response({
                "message": "Please provide the order ID."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            return Response({
                "message": "Order does not exist."
            }, status=status.HTTP_404_NOT_FOUND)

        order.delete()
        return Response({
            'message': 'Order deleted successfully'}, 
            status=status.HTTP_204_NO_CONTENT)
