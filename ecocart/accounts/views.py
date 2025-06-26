from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from .models import CustomUser
from django.contrib import messages

def home_view(request):
    return render(request, 'accounts/home.html')  # FIXED TEMPLATE PATH

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('profile')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})  # FIXED TEMPLATE PATH


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome {user.username}!")
            return redirect('profile')
        else:
            messages.error(request, "Invalid credentials.")
    return render(request, 'accounts/login.html')

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {'user': request.user})  # FIXED TEMPLATE PATH

def logout_view(request):
    logout(request)
    return redirect('home')
# --- ADD THESE NEW DUMMY VIEW FUNCTIONS ---
def blog_view(request):
    return render(request, 'placeholder.html', {'page_title': 'Our Eco Blog'})

def about_us_view(request):
    return render(request, 'placeholder.html', {'page_title': 'About EcoCart'})

def contact_view(request):
    return render(request, 'placeholder.html', {'page_title': 'Contact EcoCart'})
