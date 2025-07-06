# ecocart/products/urls.py
from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # Corrected line: Reference 'product_list_view'
    path('', views.product_list_view, name='list'), # Product list view
    path('api/products/', views.api_product_list, name='api_list'), # API endpoint for products
    path('<int:pk>/', views.product_detail_view, name='detail'), # Product detail view
]