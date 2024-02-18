from rest_framework import generics, permissions, status
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from ecommerce.models.products import Product
from ecommerce.serializers.products import ProductSerializer
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

class ProductViewApi(generics.ListAPIView):
    """
    This the Class-based View for managing Products
    """
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated]
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
        formData = request.data
        name = formData.get('name')
        description = formData.get('description')
        price = formData.get('price')
        stock = formData.get('stock')

        product = Product(
            name=name,
            description=description,
            price=price,
            stock=stock
        )
        product.save()

        return Response({
            'message': "Product has been added successfully",
            'product': ProductSerializer(product).data,
        }, status=status.HTTP_201_CREATED)

    def put(self, request, pk=None):
        formData = request.data
        pk = formData.get('id')
        
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({
                "message": "Product does not exist."
                },)

        product.name = formData.get('name', product.name)
        product.description = formData.get('description', product.description)
        product.price = formData.get('price', product.price)
        product.stock = formData.get('stock', product.stock)

        product.save()

        return Response({
            'message': "Product has been updated",
            'product': ProductSerializer(product).data,
        }, status=status.HTTP_200_OK)

    def delete(self, request):
        try:
            product = request.query_params.get('id')
            product = Product.objects.get(pk=product)
            product.delete()

            return Response({
                'message': 'Product deleted successfully',
            }, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            content = {'error': 'Error deleting the Product'}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
