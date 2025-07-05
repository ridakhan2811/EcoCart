# ecocart/orders/urls.py

from django.urls import path
from . import views # Assuming you will have views in orders/views.py

app_name = 'orders' # This line is essential for the namespace to work

urlpatterns = [
    # API endpoint for processing orders (moved from accounts/urls.py)
    path('process_order/', views.process_order, name='process_order'),

    # TEMPORARY FIX: Comment out this line until views.py is provided and fixed
    path('order_success/', views.order_success, name='order_success'),

    # Define your other order-related URL patterns here later if needed.
    # For example:
    # path('my-orders/', views.my_orders_view, name='my_orders'),
    # path('order-details/<int:order_id>/', views.order_detail_view, name='order_detail'),
]
