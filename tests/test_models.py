# from decimal import Decimal
# from django.test import TestCase
# from django.contrib.auth.models import User
# from ecommerce.models import CustomerProfile, Product, ShoppingCart, CartItem, Order, OrderItem
# from factory.django import DjangoModelFactory
# from factory import SubFactory, Faker

# # Import Factory Boy factory classes

# class UserFactory(DjangoModelFactory):
#     class Meta:
#         model = User
    
#     username = Faker('user_name')
#     email = Faker('email')
#     first_name = Faker('first_name')
#     last_name = Faker('last_name')

# class CustomerProfileFactory(DjangoModelFactory):
#     class Meta:
#         model = CustomerProfile
    
#     user = SubFactory(UserFactory)
#     full_name = Faker('name')
#     Id_number = Faker('ssn')
#     email = Faker('email')
#     phone_number = Faker('phone_number')

# class ProductFactory(DjangoModelFactory):
#     class Meta:
#         model = Product
    
#     name = Faker('word')
#     description = Faker('sentence')
#     price = Faker('pydecimal', left_digits=3, right_digits=2)
#     stock = Faker('random_int')

# class ShoppingCartFactory(DjangoModelFactory):
#     class Meta:
#         model = ShoppingCart
    
#     user = SubFactory(UserFactory)

# class CartItemFactory(DjangoModelFactory):
#     class Meta:
#         model = CartItem
    
#     product = SubFactory(ProductFactory)
#     shopping_cart = SubFactory(ShoppingCartFactory)
#     quantity = Faker('random_int')

# class OrderFactory(DjangoModelFactory):
#     class Meta:
#         model = Order
    
#     user = SubFactory(UserFactory)
#     total_amount = Faker('pydecimal', left_digits=4, right_digits=2)
#     status = Faker('random_element', elements=['Pending', 'Approved', 'Delivered'])

# class OrderItemFactory(DjangoModelFactory):
#     class Meta:
#         model = OrderItem
    
#     order = SubFactory(OrderFactory)
#     product = SubFactory(ProductFactory)
#     quantity = Faker('random_int')

# class CustomerModelTest(TestCase):
#     def test_customer_creation(self):
#         customer = CustomerProfileFactory()
#         self.assertEqual(customer.user.username, customer.user.username)
#         self.assertEqual(customer.full_name, customer.full_name)
#         self.assertEqual(customer.Id_number, customer.Id_number)
#         self.assertEqual(customer.email, customer.email)
#         self.assertEqual(customer.phone_number, customer.phone_number)

# class ProductModelTest(TestCase):
#     def test_product_creation(self):
#         product = ProductFactory()
#         self.assertEqual(product.name, product.name)
#         self.assertEqual(product.description, product.description)
#         self.assertEqual(product.price, product.price)
#         self.assertEqual(product.stock, product.stock)

#     def test_product_str_method(self):
#         product = ProductFactory()
#         self.assertEqual(str(product), product.name)

# class ShoppingCartModelTest(TestCase):
#     def test_shopping_cart_creation(self):
#         shopping_cart = ShoppingCartFactory()
#         self.assertEqual(str(shopping_cart), f"Shopping Cart for {shopping_cart.user.username}")

# class CartItemModelTest(TestCase):
#     def test_cart_item_creation(self):
#         cart_item = CartItemFactory()
#         self.assertEqual(cart_item.product.name, cart_item.product.name)
#         self.assertEqual(cart_item.shopping_cart.user.username, cart_item.shopping_cart.user.username)
#         self.assertEqual(cart_item.quantity, cart_item.quantity)

# # Test for Orders
# class OrderModelTest(TestCase):
#     def test_order_creation(self):
#         order = OrderFactory()
#         self.assertEqual(str(order), f"Order #{order.id} for {order.user.username} - {order.get_status_display()}")

# # Test for Order Items
# class OrderItemModelTest(TestCase):
#     def test_order_item_creation(self):
#         order_item = OrderItemFactory()
#         self.assertEqual(order_item.product.name, order_item.product.name)
#         self.assertEqual(order_item.order.user.username, order_item.order.user.username)
#         self.assertEqual(order_item.quantity, order_item.quantity)
