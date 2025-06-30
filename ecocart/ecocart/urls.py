# your_project_name/ecocart/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# CHANGE THIS LINE:
from products.views import product_list_view 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('wishlist/', include('wishlist.urls')),
<<<<<<< HEAD
    path('products/', include('products.urls')), # This correctly includes products.urls
=======
    path('products/', include('products.urls', namespace='products')), # NEW: Products app URLs


>>>>>>> 29b799f3c1aef048cc7e0014e2c2f9dc948e699c
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)