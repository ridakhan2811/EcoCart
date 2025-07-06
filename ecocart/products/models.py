from django.db import models
from django.utils.text import slugify
import random


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=100, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    short_description = models.CharField(max_length=255)
    long_description = models.TextField(blank=True, null=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    review_count = models.PositiveIntegerField(default=0)
    is_eco_friendly = models.BooleanField(default=False)
    eco_impact_statement = models.TextField(blank=True, null=True, help_text="e.g., 'This product helps reduce carbon footprint.'")
    # Added this field based on your template and API view usage
    plastic_saved_kg = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="e.g., '3.50' kg of plastic saved per item.")
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

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
        if self.rating == 0.0:
            self.rating = round(random.uniform(3.0, 5.0), 1)
            self.review_count = random.randint(10, 200)
        super().save(*args, **kwargs)