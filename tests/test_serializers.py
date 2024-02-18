from django.test import TestCase
from django.contrib.auth.models import User
from ecommerce.models.users import CustomerProfile
from ecommerce.serializers.users import CustomerRegistrationSerializer

"""
this is the test fro customer serializer
"""
class CustomerRegistrationSerializerTest(TestCase):
    def setUp(self):
        self.user_data = {
            'full_name': 'Aduda Shem',
            'Id_number': '1234567890',
            'email': 'shemaduda001@gmail.com',
            'phone_number': '0741732778',
            'password': 'password123'
        }

    def test_create_customer(self):
        serializer = CustomerRegistrationSerializer(data=self.user_data)

        self.assertTrue(serializer.is_valid())
        customer = serializer.save()

        self.assertIsInstance(customer.user, User)
        self.assertIsInstance(customer, CustomerProfile)

        self.assertEqual(customer.user.email, self.user_data['email'])

        self.assertEqual(customer.full_name, self.user_data['full_name'])
        self.assertEqual(customer.Id_number, self.user_data['Id_number'])
        self.assertEqual(customer.phone_number, self.user_data['phone_number'])

        self.assertTrue(customer.user.check_password(self.user_data['password']))

    def test_missing_required_field(self):
        del self.user_data['full_name']
        serializer = CustomerRegistrationSerializer(data=self.user_data)

        self.assertFalse(serializer.is_valid())

