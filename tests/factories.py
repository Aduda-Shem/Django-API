from factory.django import DjangoModelFactory
from factory import Faker, SubFactory, post_generation
from django.utils import timezone
from ecommerce.models import Customer, Product, Order, Stock

# Customer Factory
class CustomerFactory(DjangoModelFactory):
    class Meta:
        model = Customer
    
    full_name = Faker('name')
    code = Faker('uuid4')
    phone_number = Faker('phone_number')
    date_created = timezone.now()

# Product Factory
class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product
    
    name = Faker('word')
    description = Faker('sentence')
    price = Faker('pydecimal', left_digits=3, right_digits=2)
    quantity = Faker('random_int')

# Stock Factory
class StockFactory(DjangoModelFactory):
    class Meta:
        model = Stock
    
    product = SubFactory(ProductFactory)
    quantity = Faker('random_int')
    reason_for_change = Faker('sentence')
    created_at = timezone.now()

# Order Factory
class OrderFactory(DjangoModelFactory):
    class Meta:
        model = Order
    
    customer = SubFactory(CustomerFactory)
    created_at = timezone.now()
    status = Faker('random_element', elements=['Pending', 'Approved', 'Delivered'])
    total_amount = Faker('pydecimal', left_digits=4, right_digits=2)
    
    @post_generation
    def products(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            self.products.add(*extracted)
