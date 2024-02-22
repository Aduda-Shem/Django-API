from django.core.paginator import Paginator, EmptyPage
from ecommerce.models.users import Customer
from ecommerce.serializers.users import CustomerSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

class CustomerViewApi(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = CustomerSerializer

    def get_queryset(self):
        q = self.request.query_params.get("q")
        if q:
            return Customer.objects.filter(full_name__icontains=q).order_by('id')
        else:
            return Customer.objects.all().order_by('id')

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Pagination
        page_number = request.query_params.get('page', 1)
        rows = request.query_params.get('rows', 10)

        paginator = Paginator(queryset, rows)

        try:
            customers_page = paginator.page(page_number)
        except EmptyPage:
            return Response({
                "message": "Invalid page number"
            }, status=status.HTTP_400_BAD_REQUEST)

        serialized_data = self.serializer_class(customers_page, many=True).data
        return Response(
            serialized_data, 
            status=status.HTTP_200_OK
            )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, 
                status=status.HTTP_201_CREATED
                )
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
            )

    def put(self, request, pk=None):
        pk = request.data.get('id')
        try:
            customer = Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            return Response({
                "message": "Customer does not exist."
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, 
                status=status.HTTP_200_OK
                )
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request):
        customer_id = request.data.get('customer_id')
        if not customer_id:
            return Response({
                "message": "Please provide the customer ID."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            customer = Customer.objects.get(pk=customer_id)
            customer_name = customer.full_name
            customer.delete()

            return Response({
                'message': f'Customer {customer_name} deleted successfully',
            }, status=status.HTTP_200_OK)
        except Customer.DoesNotExist:
            return Response({
                'error': 'Customer not found'}, 
                status=status.HTTP_404_NOT_FOUND)
