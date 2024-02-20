# from django.contrib.auth.models import User
# from django.test import TestCase, RequestFactory
# from rest_framework import status
# from rest_framework.test import force_authenticate
# from oauth2_provider.models import AccessToken
# from ecommerce.models.products import Product
# from ecommerce.views.products import ProductViewApi
# from faker import Faker

# fake = Faker()

# class ProductViewApiTest(TestCase):
#     def setUp(self):
#         self.factory = RequestFactory()
#         self.user = User.objects.create(username=fake.user_name())
#         self.access_token = AccessToken.objects.create(
#             user=self.user,
#             token='valid-access-token',
#             expires='2025-02-12T00:00:00Z',  
#             scope='read write',  
#         )
#         self.product1 = Product.objects.create(
#             name=fake.company(), 
#             description=fake.text(), 
#             price=fake.pydecimal(left_digits=3, right_digits=2), 
#             stock=fake.random_int(min=1, max=100)
#         )
#         self.product2 = Product.objects.create(
#             name=fake.company(), 
#             description=fake.text(), 
#             price=fake.pydecimal(left_digits=3, right_digits=2), 
#             stock=fake.random_int(min=1, max=100)
#         )

#     def test_create_product(self):
#         request = self.factory.post('/products/', {
#             'name': fake.company(), 
#             'description': fake.text(), 
#             'price': fake.pydecimal(left_digits=3, right_digits=2), 
#             'stock': fake.random_int(min=1, max=100)
#         })        
#         view = ProductViewApi.as_view()        
#         force_authenticate(request, user=self.user, token=self.access_token)
#         response = view(request)        
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)        
#         self.assertEqual(Product.objects.count(), 3)        
#         self.assertEqual(response.data['message'], "Product has been added successfully")
