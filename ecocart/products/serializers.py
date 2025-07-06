# ecocart/products/serializers.py
from rest_framework import serializers
from .models import Product, Category

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_slug = serializers.CharField(source='category.slug', read_only=True)
    image_url = serializers.SerializerMethodField()
    is_discounted = serializers.BooleanField(read_only=True)
    discount_percentage = serializers.IntegerField(read_only=True)
    stars_full = serializers.IntegerField(read_only=True)
    stars_half = serializers.IntegerField(read_only=True)
    stars_empty = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'brand', 'short_description', # Keep 'short_description'
            'price', 'original_price', 'image', 'image_url', 'category',
            'category_name', 'category_slug', 'is_eco_friendly',
            'eco_impact_statement', 'stock', 'rating', 'review_count',
            'plastic_saved_kg', # Ensure this field is included
            'is_discounted', 'discount_percentage',
            'stars_full', 'stars_half', 'stars_empty',
        ]

    def get_image_url(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            return obj.image.url
        return None