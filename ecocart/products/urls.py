<<<<<<< HEAD
# ecocart/products/urls.py
=======
# products/urls.py
>>>>>>> 29b799f3c1aef048cc7e0014e2c2f9dc948e699c

from django.urls import path
from . import views

<<<<<<< HEAD
app_name = 'products' # <--- MAKE SURE THIS LINE IS PRESENT AND CORRECT

urlpatterns = [
    path('', views.product_list_view, name='list'), # Assuming 'list' is the name for your product list page
    path('<int:pk>/', views.product_detail_view, name='detail'), # Assuming 'detail' is for product detail
    # ... other product-related URLs
]
=======
app_name = 'products' # Namespace for your app URLs

urlpatterns = [
    path('', views.product_list, name='list'), # products/
    path('<int:pk>/', views.product_detail, name='detail'), # products/1/ (for specific product)
    path('api/products/', views.api_product_list, name='api_list'), # API for JS filters/pagination
]
>>>>>>> 29b799f3c1aef048cc7e0014e2c2f9dc948e699c
