from django.test import TestCase
from ecommerce.serializers.orders import OrderSerializer
from ecommerce.serializers.products import ProductSerializer
from ecommerce.serializers.users import CustomerSerializer
from tests.factories import CustomerFactory, OrderFactory, ProductFactory

# test_case --> CustomerOrderSerializerTest
class CustomerOrderSerializerTest(TestCase):
    def test_customer_order_serializer(self):
        customer = CustomerFactory()
        serializer = CustomerSerializer(customer)
        self.assertEqual(serializer.data['full_name'], customer.full_name)

# test_case --> OrderSerializerTest
class OrderSerializerTest(TestCase):
    def test_order_serializer(self):
        order = OrderFactory()
        serializer = OrderSerializer(order)
        self.assertEqual(serializer.data['uuid'], str(order.uuid))
        self.assertEqual(serializer.data['customer']['full_name'], order.customer.full_name)

# test_case --> ProductSerializerTest
class ProductSerializerTest(TestCase):
    def test_product_serializer(self):
        product = ProductFactory()
        serializer = ProductSerializer(product)
        self.assertEqual(serializer.data['name'], product.name)
