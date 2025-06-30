# ecocart/products/views.py
from django.shortcuts import render, get_object_or_404
from .models import Product # Corrected import: only import Product

def product_list_view(request):
    products = Product.objects.all()
    
    # --- THIS IS THE CRUCIAL LINE TO ADD/ENSURE IS PRESENT ---
    # Get categories directly from the Product model's choices
    categories = Product.CATEGORY_CHOICES 
    # --- END OF CRUCIAL LINE ---

    context = {
        'products': products,
        'categories': categories, # Now 'categories' is defined!
        'pick_up_line': "Curated for a Greener Tomorrow.", 
        'current_category': 'all', 
        'current_search': '', 
        'eco_friendly_checked': False, 
        'current_sort_by': 'default', 
    }
    return render(request, 'products/product_list.html', context)


def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {
        'product': product,
    }
    return render(request, 'products/product_detail.html', context)