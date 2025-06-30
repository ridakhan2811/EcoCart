# ecocart/products/models.py

from django.db import models
from django.utils.text import slugify # You'll need this if you add a slug to Category or Product later


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
    price = models.DecimalField(max_digits=10, decimal_places=2) # Changed max_digits to 10 for potentially larger prices
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) # Changed max_digits to 10
    image = models.ImageField(upload_to='products/', blank=True, null=True) # Added blank=True, null=True to image field
                                                                            # as per your traceback indicating it might be missing
    eco_friendly = models.BooleanField(default=True)
    rating = models.FloatField(default=4.0)
    in_stock = models.PositiveIntegerField(default=10)
    # Fields for discount logic (from template's expectation)
    is_discounted = models.BooleanField(default=False)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True) # e.g., 20.00 for 20%

    # Fields for eco-impact (from template's expectation)
    plastic_saved_kg = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    eco_impact_statement = models.TextField(blank=True, null=True)

    # Fields for reviews (from template's expectation)
    review_count = models.IntegerField(default=0)


    def __str__(self):
        return self.name

    # Helper methods for star ratings (from template's expectation)
    def get_stars_full(self):
        return int(self.rating)

    def get_stars_half(self):
        # Check if there's a half star (0.5 or more in the decimal part)
        return 1 if (self.rating - int(self.rating)) >= 0.5 else 0

    def get_stars_empty(self):
        full = self.get_stars_full()
        half = self.get_stars_half()
        # Calculate empty stars out of 5 total stars
        return 5 - (full + half)

    # Override save method to automatically calculate discount (as discussed)
    def save(self, *args, **kwargs):
        if self.original_price and self.price < self.original_price:
            self.is_discounted = True
            # Ensure discount_percentage is calculated only if there's an original_price
            if self.original_price > 0: # Avoid division by zero
                self.discount_percentage = ((self.original_price - self.price) / self.original_price) * 100
            else:
                self.discount_percentage = 0.00 # Or set to None if original_price is 0
        else:
            self.is_discounted = False
            self.discount_percentage = None # Set to None if no discount
        super().save(*args, **kwargs)