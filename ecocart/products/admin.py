from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Product # Import your Product model

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'in_stock', 'eco_friendly')
    list_filter = ('category', 'eco_friendly', 'in_stock')
    search_fields = ('name', 'description', 'brand')
    ordering = ('name',)