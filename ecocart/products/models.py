# products/models.py
from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('Home', 'Home'),
        ('Kitchen', 'Kitchen'),
        ('Grocery', 'Grocery'),
        ('Fashion', 'Fashion'),
        ('Personal Care', 'Personal Care'),
        ('Stationery', 'Stationery'),
        ('Cleaning', 'Cleaning'),
        ('Pet Care', 'Pet Care'),
    ]

    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    original_price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='products/')
    eco_friendly = models.BooleanField(default=True)
    rating = models.FloatField(default=4.0)
    in_stock = models.PositiveIntegerField(default=10)

    def __str__(self):
        return self.name