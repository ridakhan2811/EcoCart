from django.shortcuts import render

def product_page(request):   # Rename this
    return render(request, 'products/product.html')
