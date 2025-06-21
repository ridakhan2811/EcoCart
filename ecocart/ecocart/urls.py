from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('products/', include('products.urls')),
    path('cart/', include('cart.urls')),
    path('wishlist/', include('wishlist.urls')),
    path('reviews/', include('reviews.urls')),
    path('orders/', include('orders.urls')),
    path('payments/', include('payments.urls')),
    path('coupons/', include('coupons.urls')),
    path('contact/', include('contact.urls')),
]   + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

