# products/models.py
from django.db import models

class Product(models.Model):
    """
    A simple mock Product model to demonstrate product listing.
    In a real application, you'd likely have more fields and relationships.
    """
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    brand = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    short_description = models.TextField(blank=True)
    stock = models.IntegerField(default=0)
    is_eco_friendly = models.BooleanField(default=False)
    eco_impact_statement = models.TextField(blank=True, null=True)
    is_discounted = models.BooleanField(default=False)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    discount_percentage = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    image = models.ImageField(upload_to='products/images/', blank=True, null=True) # Requires Pillow

    class Meta:
        # Define default ordering for products
        ordering = ['name'] # Order by name by default

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Calculate discount_percentage if discounted and original_price exists
        if self.is_discounted and self.original_price and self.price < self.original_price:
            self.discount_percentage = ((self.original_price - self.price) / self.original_price) * 100
        elif not self.is_discounted:
            self.original_price = None
            self.discount_percentage = None
        super().save(*args, **kwargs)

