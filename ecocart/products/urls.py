# products/urls.py
from django.urls import path
from . import views # Import the entire views module from the current app

app_name = 'products' # This sets the application namespace

urlpatterns = [
    # The path here should be an empty string if 'products/' is handled by the main urls.py
    path('', views.product_list_view, name='list'),
    # You would add paths for individual product details etc., here if needed:
    # path('<int:pk>/', views.product_detail_view, name='detail'),
]
