# ecocart/products/urls.py

from django.urls import path
from . import views

app_name = 'products'  # Namespace for your app URLs

urlpatterns = [
    path('', views.product_list, name='list'),  # Product list view
    path('<int:pk>/', views.product_detail, name='detail'),  # Product detail view
    path('api/products/', views.api_product_list, name='api_list'),  # API endpoint (if used)
]
