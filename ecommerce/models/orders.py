from django.db import models

from ecommerce.models.users import User

"""
    Shopping Cart Model
"""
class ShoppingCart(models.Model):
    user = models.ForeignKey(
        "ecommerce.User", on_delete=models.CASCADE)
    def __str__(self):
        return f"Shopping Cart for {self.user.username}"


"""
    Specific Cart item Model
"""
class CartItem(models.Model):
    product = models.ForeignKey(
        "ecommerce.Product", on_delete=models.CASCADE)
    shopping_cart = models.ForeignKey(
        "ecommerce.ShoppingCart", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

"""
     Order Model
"""
class Order(models.Model):
    PENDING = 'Pending'
    APPROVED = 'Approved'
    DELIVERED = 'Delivered'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (DELIVERED, 'Delivered'),
    ]
    user = models.ForeignKey(
        "ecommerce.User", on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)

    def __str__(self):
        return f"Order #{self.id} for {self.user.username} - {self.status}"

"""
    Specific OrderItem Model
"""
class OrderItem(models.Model):
    order = models.ForeignKey(
        "ecommerce.Order", on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order #{self.order.id}"