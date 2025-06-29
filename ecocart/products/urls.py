# products/urls.py

from django.urls import path
from . import views

app_name = 'products' # Namespace for your app URLs

urlpatterns = [
    path('', views.product_list, name='list'), # products/
    path('<int:pk>/', views.product_detail, name='detail'), # products/1/ (for specific product)
    path('api/products/', views.api_product_list, name='api_list'), # API for JS filters/pagination
]
