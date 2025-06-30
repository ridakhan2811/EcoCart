# ecocart/products/urls.py

from django.urls import path
from . import views

app_name = 'products' # <--- MAKE SURE THIS LINE IS PRESENT AND CORRECT

urlpatterns = [
    path('', views.product_list_view, name='list'), # Assuming 'list' is the name for your product list page
    path('<int:pk>/', views.product_detail_view, name='detail'), # Assuming 'detail' is for product detail
    # ... other product-related URLs
]