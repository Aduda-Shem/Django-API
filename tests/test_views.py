from django.test import TestCase
from ecommerce.models.users import Customer
from rest_framework.test import APIClient
from rest_framework import status
from ecommerce.models.products import Product, Stock
from tests.factories import CustomerFactory, ProductFactory

class ProductViewApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_products(self):
        # Creatingd some products using Factory Boy
        ProductFactory.create_batch(2)

        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['products']), 2)

    def test_create_product(self):
        product_data = {
            'name': 'New Product',
            'description': 'New Product Description',
            'price': 20.99,
            'quantity': 3
        }
        response = self.client.post('/api/products/', product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if the product and associated stock are created
        self.assertTrue(Product.objects.filter(name='New Product').exists())
        self.assertTrue(Stock.objects.filter(product__name='New Product').exists())

    def test_update_product(self):
        product = ProductFactory()
        new_price = 25.99
        updated_data = {
            'name': product.name,
            'description': product.description,
            'price': new_price,
            'quantity': product.quantity
        }
        response = self.client.put(f'/api/products/{product.pk}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # is product is updated?
        updated_product = Product.objects.get(pk=product.pk)
        self.assertEqual(updated_product.price, new_price)

    def test_delete_product(self):
        product = ProductFactory()
        response = self.client.delete(f'/api/products/{product.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # isproduct deleted
        self.assertFalse(Product.objects.filter(pk=product.pk).exists())
        self.assertFalse(Stock.objects.filter(product=product).exists())


# Cuatomer test view
class CustomerViewApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_customers(self):
        # Customer generation using fact0ry boy
        CustomerFactory.create_batch(2)

        response = self.client.get('/api/customers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['customers']), 2) 

    def test_create_customer(self):
        customer_data = {
            'full_name': 'John Doe',
            'code': '12345',
            'phone_number': '+1234567890'
        }
        response = self.client.post('/api/customers/', customer_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check is customer created
        self.assertTrue(Customer.objects.filter(full_name='John Doe').exists())

    def test_update_customer(self):
        customer = CustomerFactory()
        new_phone_number = '+9876543210'
        updated_data = {
            'full_name': customer.full_name,
            'code': customer.code,
            'phone_number': new_phone_number
        }
        response = self.client.put(f'/api/customers/{customer.pk}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check is customer updated
        updated_customer = Customer.objects.get(pk=customer.pk)
        self.assertEqual(updated_customer.phone_number, new_phone_number)

    def test_delete_customer(self):
        customer = CustomerFactory()
        response = self.client.delete(f'/api/customers/{customer.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check is customer deleted
        self.assertFalse(Customer.objects.filter(pk=customer.pk).exists())