from django.test import TestCase
from ecommerce.models.orders import Order
from ecommerce.models.users import Customer
from rest_framework.test import APIClient
from rest_framework import status
from ecommerce.models.products import Product, Stock
from tests.factories import CustomerFactory, OrderFactory, ProductFactory

class ProductViewApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_products(self):
        # products created with -->  Factory Boy
        ProductFactory.create_batch(2)

        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['products']), 2)

    def test_create_product(self):
        product_data = ProductFactory.build()
        response = self.client.post('/api/products/', product_data.__dict__, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # product associated wth stock
        self.assertTrue(Product.objects.filter(name=product_data.name).exists())
        self.assertTrue(Stock.objects.filter(product__name=product_data.name).exists())

    def test_update_product(self):
        product = ProductFactory()
        new_price = 25.99
        updated_data = {
            'name': product.name,
            'description': product.description,
            'price': new_price,
            'quantity': product.quantity
        }
        response = self.client.put('/api/products/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # product update checl
        updated_product = Product.objects.get(pk=product.pk)
        self.assertEqual(updated_product.price, new_price)

    def test_delete_product(self):
        product = ProductFactory()
        response = self.client.delete('/api/products/', {'product_id': product.pk})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # product deleted check
        self.assertFalse(Product.objects.filter(pk=product.pk).exists())
        self.assertFalse(Stock.objects.filter(product=product).exists())

# Customer test view
class CustomerViewApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_customers(self):
        # Customer created with --> Factory Boy
        CustomerFactory.create_batch(2)

        response = self.client.get('/api/customers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['customers']), 2) 

    def test_create_customer(self):
        customer_data = CustomerFactory.build()
        response = self.client.post('/api/customers/', customer_data.__dict__, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # customer created check
        self.assertTrue(Customer.objects.filter(full_name=customer_data.full_name).exists())

    def test_update_customer(self):
        customer = CustomerFactory()
        new_phone_number = '+9876543210'
        updated_data = {
            'full_name': customer.full_name,
            'code': customer.code,
            'phone_number': new_phone_number
        }
        response = self.client.put('/api/customers/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Customer update check
        updated_customer = Customer.objects.get(pk=customer.pk)
        self.assertEqual(updated_customer.phone_number, new_phone_number)

    def test_delete_customer(self):
        customer = CustomerFactory()
        response = self.client.delete('/api/customers/', {'customer_id': customer.pk})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Customer deletion check
        self.assertFalse(Customer.objects.filter(pk=customer.pk).exists())

# order test view
class OrderViewApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_orders(self):
        # Creating orders with --> Factory Boy
        customer = CustomerFactory()
        product = ProductFactory()
        order = OrderFactory.create(customer=customer, products=[product])

        response = self.client.get('/api/orders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['orders']), 1)

    def test_create_order(self):
        # associated customer && product check
        customer = CustomerFactory()
        product = ProductFactory()

        order_data = {
            'customer': customer.pk,
            'status': 'pending',
            'order_items': [
                {
                    'id': product.pk,
                    'quantity': 2
                }
            ]
        }

        response = self.client.post('/api/orders/', order_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Order Creation check
        self.assertTrue(Order.objects.filter(pk=response.data['order']['id']).exists())

    def test_delete_order(self):
        # Order exists check
        order = OrderFactory()

        response = self.client.delete(f'/api/orders/', {'order_id': order.pk})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Order deletion check
        self.assertFalse(Order.objects.filter(pk=order.pk).exists())