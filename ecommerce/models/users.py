from django.db import models
from django.contrib.auth.models import User

"""
    Customer Model
"""
class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    Id_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.full_name