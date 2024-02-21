from ecommerce.models.users import Customer
from ecommerce.serializers.users import CustomerSerializer
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from oauth2_provider.contrib.rest_framework import TokenHasScope

class CustomerAPIView(generics.GenericAPIView):
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['openid']

    def get(self, request):
        customers = Customer.objects.all()
        serializer = self.serializer_class(customers, many=True)
        return Response({
            'message': "Customers retrieved successfully",
            'customers': serializer.data,
        }, status=status.HTTP_200_OK)

    def post(self, request):
        first_name = request.data.get('first_name')
        phone_number = request.data.get('phone_number')
        date_created = request.data.get('date_created')

        customer = Customer.objects.create(
            first_name=first_name,
            phone_number=phone_number,
            date_created=date_created
        )

        serializer = self.serializer_class(customer)

        return Response({
            'message': "Customer created successfully",
            'customer': serializer.data,
        }, status=status.HTTP_201_CREATED)

    def put(self, request):
        customer_id = request.data.get('id')
        if not customer_id:
            return Response({
                'message': "Please provide the customer ID",
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return Response({
                'message': "Customer not found",
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(customer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': "Customer updated successfully",
                'customer': serializer.data,
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        customer_id = request.query_params.get('id')
        if not customer_id:
            return Response({
                'message': "Please provide the customer ID",
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            customer = Customer.objects.get(id=customer_id)
            customer.delete()
            return Response({
                'message': "Customer deleted successfully",
            }, status=status.HTTP_204_NO_CONTENT)
        except Customer.DoesNotExist:
            return Response({
                'message': "Customer not found",
            }, status=status.HTTP_404_NOT_FOUND)
