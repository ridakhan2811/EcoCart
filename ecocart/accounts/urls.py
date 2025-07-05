# ecocart/accounts/urls.py

from django.urls import path
from . import views

app_name = 'accounts' # This defines the namespace for {% url "accounts:..." %}

urlpatterns = [
    # Change the path for your home view from 'home/' to ''
    path('', views.home_view, name='home'), # <--- This looks correct for the root URL
    # If you still want /home/ to work as an alternative path to the same view,
    # you can add another line:
    # path('home/', views.home_view, name='home_explicit'),

    # Basic authentication views
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),

    # Other general pages
    path('blog/', views.blog_view, name='blog'),
    path('about-us/', views.about_us_view, name='about_us'),
    path('contact/', views.contact_view, name='contact'),

    # Cart, Checkout, Wishlist (these views are still in accounts/views.py as per your last provided file)
    path('cart/', views.cart_detail, name='cart_detail'),
    path('wishlist/', views.wishlist_view, name='wishlist_view'),
    path('checkout/', views.checkout_view, name='checkout_view'),

    # Order Receipt and Printable Invoice (these views are still in accounts/views.py as per your last provided file)
    path('order-receipt/<str:order_id>/', views.order_receipt_view, name='order_receipt'),
    path('order-receipt/<str:order_id>/print/', views.printable_invoice_view, name='printable_invoice'),

    # REMOVED: path('process-order/', views.process_order, name='process_order'),
    # This URL will be moved to ecocart/orders/urls.py
]
