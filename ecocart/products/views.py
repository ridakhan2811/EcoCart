from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, Http404
from .models import Product, Category
from django.core.paginator import Paginator
from django.db.models import Q  # For search functionality
import random  # For pick-up line
from django.core import serializers
from .models import Product


def load_more_products(request):
    offset = int(request.GET.get('offset', 0))
    limit = 4  # how many products to load at once

    products = Product.objects.all()[offset:offset+limit]
    data = serializers.serialize('json', products)
    return JsonResponse({'products': data})


# Dummy pick-up lines
PICK_UP_LINES = [
    "Sustainable Choices, Happy Planet.",
    "Shop Smarter, Live Greener.",
    "Eco-Friendly Excellence at Your Fingertips.",
    "Making a Difference, One Product at a Time.",
    "Your Journey to Sustainable Living Starts Here.",
]


def get_product_queryset(request):
    """Helper function to build the base queryset with filters and sorting."""
    queryset = Product.objects.all().select_related('category')

    # Filtering
    category_slug = request.GET.get('category', 'all')
    search_query = request.GET.get('search', '').strip()
    eco_friendly_only = request.GET.get('eco_friendly', 'false').lower() == 'true'

    if category_slug != 'all':
        queryset = queryset.filter(category__slug=category_slug)

    if search_query:
        queryset = queryset.filter(
            Q(name__icontains=search_query) |
            Q(brand__icontains=search_query) |
            Q(short_description__icontains=search_query) |
            Q(long_description__icontains=search_query)
        )

    if eco_friendly_only:
        queryset = queryset.filter(is_eco_friendly=True)

    # Sorting
    sort_by = request.GET.get('sort_by', 'default')
    if sort_by == 'price_asc':
        queryset = queryset.order_by('price')
    elif sort_by == 'price_desc':
        queryset = queryset.order_by('-price')
    elif sort_by == 'rating_desc':
        queryset = queryset.order_by('-rating', '-review_count')
    elif sort_by == 'name_asc':
        queryset = queryset.order_by('name')
    else:
        queryset = queryset.order_by('-created_at')

    return queryset


def product_list(request):
    all_categories = Category.objects.all().order_by('name')
    initial_products = get_product_queryset(request)

    # Pagination
    paginator = Paginator(initial_products, 8)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # DEBUG: Print stock for products on initial load
    print(f"--- Debugging product_list view ---")
    for product in page_obj:
        print(f"Product: {product.name}, Stock: {product.stock}")
    print(f"-----------------------------------")


    context = {
        'products': page_obj,
        'categories': all_categories,
        'current_category': request.GET.get('category', 'all'),
        'current_search': request.GET.get('search', ''),
        'eco_friendly_checked': request.GET.get('eco_friendly', 'false').lower() == 'true',
        'current_sort_by': request.GET.get('sort_by', 'default'),
        'pick_up_line': random.choice(PICK_UP_LINES),
    }

    return render(request, 'products/product_list.html', context)


def api_product_list(request):
    products_qs = get_product_queryset(request)

    paginator = Paginator(products_qs, 8)
    page_number = request.GET.get('page')

    try:
        page_obj = paginator.page(page_number)
    except Exception:
        return JsonResponse({'products': [], 'has_next': False}, status=200)

    products_data = []
    # DEBUG: Print stock for products in API response
    print(f"--- Debugging api_product_list view ---")
    for product in page_obj:
        print(f"API Product: {product.name}, Stock: {product.stock}")
        products_data.append({
            'id': product.id,
            'name': product.name,
            'brand': product.brand,
            'category_slug': product.category.slug if product.category else '',
            'category_name': product.category.name if product.category else '',
            'image_url': product.image.url if product.image else 'https://placehold.co/400x300/e0ffe0/333333?text=EcoProduct',
            'price': float(product.price),
            'original_price': float(product.original_price) if product.original_price else None,
            'short_description': product.short_description,
            'rating': float(product.rating),
            'review_count': product.review_count,
            'is_eco_friendly': product.is_eco_friendly,
            'eco_impact_statement': product.eco_impact_statement,
            'stock': product.stock, # Ensure this is 'stock' to match model and HTML
            'is_discounted': product.is_discounted,
            'discount_percentage': product.discount_percentage,
            'stars_full': product.get_stars_full,
            'stars_half': product.get_stars_half,
            'stars_empty': product.get_stars_empty,
        })
    print(f"---------------------------------------")

    return JsonResponse({
        'products': products_data,
        'has_next': page_obj.has_next,
        'next_page_number': page_obj.next_page_number if page_obj.has_next else None,
    })


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    # DEBUG: Print stock for product on detail page
    print(f"--- Debugging product_detail view ---")
    print(f"Detail Product: {product.name}, Stock: {product.stock}")
    print(f"-------------------------------------")

    related_products = Product.objects.filter(
        category=product.category
    ).exclude(pk=pk).order_by('?')[:4]

    context = {
        'product': product,
        'related_products': related_products,
        'pick_up_line': random.choice(PICK_UP_LINES),
    }

    return render(request, 'products/product_detail.html', context)
