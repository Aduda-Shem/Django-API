from django.db import models
from simple_history.models import HistoricalRecords

"""
    Product Model
"""
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=100, decimal_places=2)
    stock = models.IntegerField(default=0)

    history = HistoricalRecords()

    def __str__(self):
        return self.name