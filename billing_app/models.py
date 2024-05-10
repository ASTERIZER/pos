# models.py

from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

class Bill(models.Model):
    items = models.ManyToManyField(Item)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
