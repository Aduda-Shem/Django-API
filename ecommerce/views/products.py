from ecommerce.models.products import Product, Stock
from rest_framework import generics, status
from ecommerce.serializers.products import ProductSerializer
from django.core.paginator import Paginator, EmptyPage
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from oauth2_provider.contrib.rest_framework import TokenHasScope

class ProductViewApi(generics.GenericAPIView):
    """
    Class Based View for managing products
    """
    permission_classes = [IsAuthenticated, TokenHasScope]
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

        serialized_data = self.serializer_class(products_page, many=True).data
        return Response({
            "message": "Products Fetched Successfully!",
            "products": serialized_data,
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
        quantity = request.data.get('quantity')

        product = Product(
            name=name,
            description=description,
            price=price,
            quantity=quantity
        )
        product.save()

        # Create stock
        Stock.objects.create(product=product, quantity=quantity)

        return Response({
            "message": "Product Created Successfully!",
            "product": self.serializer_class(product).data
        }, status=status.HTTP_201_CREATED)

    def put(self, request, pk=None):
        pk = request.data.get('id')
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({
                "message": "Product does not exist."
            }, status=status.HTTP_404_NOT_FOUND)

        product.name = request.data.get('name', product.name)
        product.description = request.data.get('description', product.description)
        product.price = request.data.get('price', product.price)
        product.quantity = request.data.get('quantity', product.quantity)

        product.save()

        # Update stock
        stock, _ = Stock.objects.get_or_create(product=product)
        stock.quantity = product.quantity
        stock.save()

        return Response({
            "message": "Product Updated Successfully!",
            "product": self.serializer_class(product).data
        }, status=status.HTTP_200_OK)

    def delete(self, request):
        product_id = request.data.get('product_id')
        if not product_id:
            return Response({
                "message": "Please provide the product ID."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(pk=product_id)
            product_name = product.name
            product.delete()

            # Remove stock
            Stock.objects.filter(product=product).delete()

            return Response({
                'message': f'Product {product_name} deleted successfully',
            }, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({
                'error': 'Product not found'}, 
                status=status.HTTP_404_NOT_FOUND)
