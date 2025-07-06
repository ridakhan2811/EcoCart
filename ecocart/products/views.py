# ecocart/products/views.py
from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProductSerializer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

def product_list_view(request):
    # This view renders the initial HTML page
    # Initial filter values for the JavaScript to pick up
    current_category_slug = request.GET.get('category', 'all')
    current_search_query = request.GET.get('search', '')
    eco_friendly_checked = request.GET.get('eco_friendly', 'false').lower() == 'true'
    current_sort_by = request.GET.get('sort_by', 'default')

    categories = Category.objects.all().order_by('name')

    context = {
        'pick_up_line': "Eco-Friendly Excellence at Your Fingertips.",
        'categories': categories,
        'current_category': current_category_slug,
        'current_search': current_search_query,
        'eco_friendly_checked': eco_friendly_checked,
        'current_sort_by': current_sort_by,
    }
    return render(request, 'products/product_list.html', context)

@api_view(['GET'])
def api_product_list(request):
    products = Product.objects.all()

    # --- Filtering ---
    category_slug = request.GET.get('category', 'all')
    if category_slug and category_slug != 'all':
        products = products.filter(category__slug=category_slug)

    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(short_description__icontains=search_query) |
            Q(brand__icontains=search_query)
        )

    eco_friendly = request.GET.get('eco_friendly', 'false').lower()
    if eco_friendly == 'true':
        products = products.filter(is_eco_friendly=True)

    # --- Sorting ---
    sort_by = request.GET.get('sort_by', 'default')
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'rating_desc':
        products = products.order_by('-rating')
    elif sort_by == 'name_asc':
        products = products.order_by('name')
    else: # Default or 'default'
        products = products.order_by('-created_at') # Or any other default sort

    # --- Pagination ---
    paginator = Paginator(products, 8)  # Show 8 products per page
    page_number = request.GET.get('page', 1)

    try:
        products_page = paginator.page(page_number)
    except PageNotAnInteger:
        products_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results
        products_page = paginator.page(paginator.num_pages)

    serializer = ProductSerializer(products_page, many=True)

    return Response({
        'products': serializer.data,
        'has_next': products_page.has_next(),
        'next_page_number': products_page.next_page_number() if products_page.has_next() else None,
        'total_pages': paginator.num_pages,
        'current_page': products_page.number,
    })

# Detail View (if you have one)
def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})