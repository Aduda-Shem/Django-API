from django.test import TestCase
from ecommerce.models import Customer, Product, Order
from tests.factories import CustomerFactory, OrderFactory, ProductFactory

# Tests
class CustomerModelTest(TestCase):
    def test_customer_creation(self):
        customer = CustomerFactory()
        self.assertIsInstance(customer, Customer)
        self.assertIsNotNone(customer.pk)

class ProductModelTest(TestCase):
    def test_product_creation(self):
        product = ProductFactory()
        self.assertIsInstance(product, Product)
        self.assertIsNotNone(product.pk)

class OrderModelTest(TestCase):
    def test_order_creation(self):
        products = [ProductFactory() for _ in range(3)]
        
        order = OrderFactory(products=products)
        self.assertIsInstance(order, Order)
        self.assertIsNotNone(order.pk)
