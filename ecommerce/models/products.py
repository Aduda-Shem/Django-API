from django.db import models
from simple_history.models import HistoricalRecords
import uuid

class Product(models.Model):
    """
     Product Models
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=100, decimal_places=2)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Stock(models.Model):
    """
     Stock Models
    """
    product = models.ForeignKey(
        Product, verbose_name="Product", on_delete=models.CASCADE, related_name='product_stock')
    quantity = models.IntegerField()
    reason_for_change = models.TextField(null=True, blank=True, verbose_name="Reason for Change")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    history = HistoricalRecords()

    def __str__(self):
        return str(self.quantity)

    class Meta:
        db_table = "stock_level"
        verbose_name = "Stock Level"
        verbose_name_plural = "Stock Levels"
