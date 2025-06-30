<<<<<<< HEAD
# ecocart/products/models.py

from django.db import models
from django.utils.text import slugify # You'll need this if you add a slug to Category or Product later

=======
# products/models.py

from django.db import models
from django.utils.text import slugify # For creating URL-friendly names
import random # For generating random ratings and stock
>>>>>>> 29b799f3c1aef048cc7e0014e2c2f9dc948e699c

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True) # For clean URLs

<<<<<<< HEAD
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

=======
    class Meta:
        verbose_name_plural = "Categories" # Correct pluralization in Django Admin

    def save(self, *args, **kwargs):
        # Auto-generate slug from name if not provided
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
>>>>>>> 29b799f3c1aef048cc7e0014e2c2f9dc948e699c

    def __str__(self):
        return self.name

<<<<<<< HEAD
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
=======
class Product(models.Model):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=100, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    image = models.ImageField(upload_to='products/', blank=True, null=True) # Images will be stored in media/products/
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) # For discounted items
    short_description = models.CharField(max_length=255)
    long_description = models.TextField(blank=True, null=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0) # E.g., 4.5
    review_count = models.PositiveIntegerField(default=0) # Number of reviews, for popularity/sorting
    is_eco_friendly = models.BooleanField(default=False)
    eco_impact_statement = models.TextField(blank=True, null=True, help_text="e.g., 'Saves 3kg of plastic'")
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at'] # Default order for new products

    def __str__(self):
        return self.name

    @property
    def is_discounted(self):
        return self.original_price and self.price < self.original_price

    @property
    def discount_percentage(self):
        if self.is_discounted:
            return round(((self.original_price - self.price) / self.original_price) * 100)
        return 0

    @property
    def get_stars_full(self):
        return int(self.rating)

    @property
    def get_stars_half(self):
        return 1 if (self.rating - self.get_stars_full) >= 0.5 else 0

    @property
    def get_stars_empty(self):
        return 5 - self.get_stars_full - self.get_stars_half

    def save(self, *args, **kwargs):
        # If rating is not set, provide a random one (for dummy data)
        if self.rating == 0.0:
            self.rating = round(random.uniform(3.0, 5.0), 1)
            self.review_count = random.randint(10, 200) # Give some dummy review count
        if self.stock == 0:
            self.stock = random.randint(5, 100) # Give some dummy stock
        super().save(*args, **kwargs)

>>>>>>> 29b799f3c1aef048cc7e0014e2c2f9dc948e699c
