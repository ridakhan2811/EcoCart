from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'accounts' 


urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('blog/', views.blog_view, name='blog'),
    path('about-us/', views.about_us_view, name='about_us'), 
    path('contact/', views.contact_view, name='contact'),
    path('forgot_password/', views.forgot_password_view, name='forgot_password'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
