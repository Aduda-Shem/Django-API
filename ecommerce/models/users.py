from django.db import models
import uuid

class Customer(models.Model):
    """
     Customer Models
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    full_name = models.CharField(max_length=500, verbose_name='Full Name', null=False, blank=False)
    code = models.CharField(max_length=50, verbose_name='Code', null=False, blank=False, unique=True)
    phone_number = models.CharField(max_length=250, verbose_name='Phone Number', null=False, blank=False)
    date_created = models.DateTimeField(verbose_name='Date Created', auto_now_add=True)

    def __str__(self):
        return self.full_name
    
    class Meta:
        db_table = "Customers"
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
