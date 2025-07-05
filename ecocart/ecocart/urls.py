# ecocart/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # This line is correct and necessary for namespacing
    path('', include('accounts.urls', namespace='accounts')),
    path('wishlist/', include('wishlist.urls')), # Assuming wishlist/urls.py has app_name = 'wishlist'
    path('products/', include('products.urls', namespace='products')), # Assuming products/urls.py has app_name = 'products'
    path('orders/', include('orders.urls', namespace='orders')), # Assuming orders/urls.py exists and has app_name = 'orders'
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)