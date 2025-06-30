# products/admin.py

from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)} # Automatically populates slug from name

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'original_price', 'is_eco_friendly', 'stock', 'rating', 'review_count', 'created_at')
    list_filter = ('category', 'is_eco_friendly', 'brand')
    search_fields = ('name', 'short_description', 'long_description', 'brand')
    raw_id_fields = ('category',) # Useful for many categories
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    readonly_fields = ('review_count',) # Review count is set programmatically or by user reviews
    fieldsets = (
        (None, {
            'fields': ('name', 'brand', 'category', 'image', 'short_description', 'long_description')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'original_price', 'stock')
        }),
        ('Eco-Friendly Details', {
            'fields': ('is_eco_friendly', 'eco_impact_statement')
        }),
        ('Rating & Reviews', {
            'fields': ('rating', 'review_count')
        }),
    )

<<<<<<< HEAD
# Register your models here.
from django.contrib import admin
from .models import Product # Import your Product model

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'in_stock', 'eco_friendly')
    list_filter = ('category', 'eco_friendly', 'in_stock')
    search_fields = ('name', 'description', 'brand')
    ordering = ('name',)
=======
>>>>>>> 29b799f3c1aef048cc7e0014e2c2f9dc948e699c
