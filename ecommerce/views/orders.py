from ecommerce.models.orders import OrderItem, Order
from ecommerce.serializers.orders import OrderItemSerializer, OrderSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from oauth2_provider.contrib.rest_framework import TokenHasScope
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage


class OrderViewApi(generics.GenericAPIView):
    """
    This is the Class-based View for managing Orders
    """
    permission_classes = [IsAuthenticated, TokenHasScope]
    required_scopes = ['openid']
    order_item_serializer_class = OrderItemSerializer

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

        return Response({
            'message': "Orders have been fetched successfully",
            'orders': OrderSerializer(orders_page, many=True).data,
            "pagination": {
                "currentPage": page_number,
                "total": paginator.count,
                "pageSize": rows
            }
        }, status=status.HTTP_200_OK)

    def post(self, request):
        order_data = request.data.get('order')
        order_items_data = request.data.get('order_items')

        # Create Order
        order = Order()
        for key, value in order_data.items():
            setattr(order, key, value)
        order.save()

        # Create Order Items
        for order_item_data in order_items_data:
            order_item = OrderItem(order=order)
            for key, value in order_item_data.items():
                setattr(order_item, key, value)
            order_item.save()

        return Response({
            'message': "Order has been created successfully",
            'order': order.id,
        }, status=status.HTTP_201_CREATED)

    def delete(self, request):
        order_id = request.query_params.get('id')
        if not order_id:
            return Response({
                "message": "Please provide the order ID."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            order = Order.objects.get(pk=order_id)
            order.delete()
            return Response({
                'message': 'Order deleted successfully',
            }, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
