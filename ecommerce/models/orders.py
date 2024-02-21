from django.db import models
from django.contrib.auth.models import User
import uuid

class ShoppingCart(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Shopping Cart for {self.user.username}"

class CartItem(models.Model):
    product = models.ForeignKey("ecommerce.Product", on_delete=models.CASCADE)
    shopping_cart = models.ForeignKey("ecommerce.ShoppingCart", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class Order(models.Model):
    PENDING = 'Pending'
    APPROVED = 'Approved'
    DELIVERED = 'Delivered'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (DELIVERED, 'Delivered'),
    ]
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)

    def _get_order_total(self):
        order_items = OrderItem.objects.filter(order=self)
        total = sum(item.product.price * item.quantity for item in order_items)
        return total

    total = property(_get_order_total)

    def __str__(self):
        return f"Order #{self.uuid} for {self.user.username} - {self.status}"

class OrderItem(models.Model):
    order = models.ForeignKey("ecommerce.Order", on_delete=models.CASCADE)
    product = models.ForeignKey("ecommerce.Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order #{self.order.uuid}"
