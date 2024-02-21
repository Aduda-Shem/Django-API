from rest_framework import generics, permissions, status
from oauth2_provider.contrib.rest_framework import TokenHasScope
from ecommerce.models.products import Product
from ecommerce.serializers.products import ProductSerializer
from django.core.paginator import Paginator, EmptyPage
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class ProductViewApi(generics.GenericAPIView):
    """
    This is the Class-based View for managing Products
    """
    # permission_classes = [IsAuthenticated, TokenHasScope]
    required_scopes = ['openid']
    serializer_class = ProductSerializer

    def get_queryset(self):
        q = self.request.query_params.get("q")
        if q:
            return Product.objects.filter(name__icontains=q).order_by('id')
        else:
            return Product.objects.all().order_by('id')

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Pagination
        page_number = request.query_params.get('page', 1)
        rows = request.query_params.get('rows', 10)

        paginator = Paginator(queryset, rows)

        try:
            products_page = paginator.page(page_number)
        except EmptyPage:
            return Response({
                "message": "Invalid page number"
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'message': "Products have been fetched successfully",
            'products': ProductSerializer(products_page, many=True).data,
            "pagination": {
                "currentPage": page_number,
                "total": paginator.count,
                "pageSize": rows
            }
        }, status=status.HTTP_200_OK)

    def post(self, request):
        name = request.data.get('name')
        description = request.data.get('description')
        price = request.data.get('price')
        stock = request.data.get('stock')

        product = Product.objects.create(
            name=name,
            description=description,
            price=price,
            stock=stock
        )

        serializer = self.serializer_class(product)

        return Response({
            'message': "Product has been added successfully",
            'product': serializer.data,
        }, status=status.HTTP_201_CREATED)

    def put(self, request, pk=None):
        pk = request.data.get('id')
        
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({
                "message": "Product does not exist."
            }, status=status.HTTP_404_NOT_FOUND)

        name = request.data.get('name')
        description = request.data.get('description')
        price = request.data.get('price')
        stock = request.data.get('stock')

        if name:
            product.name = name
        if description:
            product.description = description
        if price:
            product.price = price
        if stock:
            product.stock = stock

        product.save()

        serializer = self.serializer_class(product)

        return Response({
            'message': "Product has been updated",
            'product': serializer.data,
        }, status=status.HTTP_200_OK)

    def delete(self, request):
        product_id = request.query_params.get('id')
        if not product_id:
            return Response({
                "message": "Please provide the product ID."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(pk=product_id)
            product.delete()
            return Response({
                'message': 'Product deleted successfully',
            }, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
