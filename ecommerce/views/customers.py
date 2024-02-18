from ecommerce.models.orders import ShoppingCart
from ecommerce.models.users import CustomerProfile
from ecommerce.serializers.users import CustomerRegistrationSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User

class CustomerRegistrationAPIView(generics.CreateAPIView):
    serializer_class = CustomerRegistrationSerializer

    def post(self, request, *args, **kwargs):
        formData = request.data
        print("User Reg: ", formData)
        full_name = formData.get('full_name')
        Id_number = formData.get('Id_number')
        email = formData.get('email')
        phone_number = formData.get('phone_number')
        password = formData.get('password')

        # User creattion
        user = User.objects.create_user(username=email, email=email)
        user.set_password(password)
        user.save()

        # Customer creation
        customer = CustomerProfile.objects.create(
            user=user, 
            full_name=full_name, 
            Id_number=Id_number, 
            email=email, 
            phone_number=phone_number)

        ShoppingCart.objects.create(user=user)

        return Response({
            'message': "User has been registered successfully",
            'user': CustomerRegistrationSerializer(customer).data,
        }, status=status.HTTP_201_CREATED)