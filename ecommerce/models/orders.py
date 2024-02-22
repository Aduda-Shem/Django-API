from django.db import models
from django.contrib.auth.models import User
import uuid

class Order(models.Model):
    """
    Order Models
    """
    PENDING = 'Pending'
    APPROVED = 'Approved'
    DELIVERED = 'Delivered'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (DELIVERED, 'Delivered'),
    ]
    
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    customer = models.ForeignKey("ecommerce.Customer", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    products = models.JSONField()

    def __str__(self):
        return f"Order #{self.uuid} for {self.customer.full_name} - {self.status}"
