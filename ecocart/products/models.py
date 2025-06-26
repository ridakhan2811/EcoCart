from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(default="No description available.")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')  # make sure media settings are enabled
    category = models.CharField(max_length=100, default='General')
    eco_friendly = models.BooleanField(default=False)

    def __str__(self):
        return self.name
