# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from .models import CustomUser
from django.contrib import messages

def home_view(request):
    return render(request, 'accounts/home.html')

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
    return render(request, 'accounts/register.html', {'form': form})

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
    return render(request, 'accounts/profile.html', {'user': request.user})

def logout_view(request):
    logout(request)
    return redirect('home')

# --- BLOG VIEW (image_url paths are now relative to the static folder) ---
def blog_view(request):
    """
    Renders the Blog page with mock blog post data. Image URLs are now
    relative paths expected by Django's {% static %} tag.
    """
    blog_posts_data = [
        {'title': 'The Rise of Sustainable Fashion', 'category': 'Fashion', 'summary': 'Discover how the fashion industry is shifting towards eco-friendly practices and what you can do to be part of the change. From ethical sourcing to circular economy models, sustainable fashion is more than just a trend.', 'image_url': 'accounts/images/Blogs/sustainable_fashion.jpeg', 'animation_class': 'from-left'},
        {'title': 'Zero-Waste Kitchen Hacks', 'category': 'Home', 'summary': 'Reduce your household waste with these simple yet effective kitchen hacks. Learn about composting, reusable containers, and smart shopping strategies to minimize your environmental footprint.', 'image_url': 'accounts/images/Blogs/zero_waste_kitchen.jpeg', 'animation_class': 'from-bottom'},
        {'title': 'Understanding Your Carbon Footprint', 'category': 'Environment', 'summary': 'A comprehensive guide to understanding what a carbon footprint is, how it\'s calculated, and practical steps you can take to reduce your personal impact on the planet.', 'image_url': 'accounts/images/Blogs/carbon_footprint.jpeg', 'animation_class': 'from-right'},
        {'title': 'The Benefits of Composting at Home', 'category': 'Gardening', 'summary': 'Turn your food scraps into nutrient-rich soil. This post explores the many benefits of composting for your garden and the environment, along with easy setup tips.', 'image_url': 'accounts/images/Blogs/composting.jpeg', 'animation_class': 'from-left'},
        {'title': 'Eco-Friendly Travel Destinations', 'category': 'Travel', 'summary': 'Explore stunning destinations that prioritize sustainability. Learn about eco-tourism principles and how to plan your next adventure responsibly.', 'image_url': 'accounts/images/Blogs/eco_travel.jpeg', 'animation_class': 'from-bottom'},
        {'title': 'DIY Natural Cleaning Products', 'category': 'Home', 'summary': 'Save money and protect your family from harsh chemicals by making your own effective natural cleaning solutions with everyday ingredients.', 'image_url': 'accounts/images/Blogs/cleaning_products.jpeg', 'animation_class': 'from-right'},
        {'title': 'Saving Water: Simple Habits, Big Impact', 'category': 'Conservation', 'summary': 'Water conservation is more critical than ever. Discover easy daily habits that can significantly reduce your water consumption at home and contribute to global efforts.', 'image_url': 'accounts/images/Blogs/save_water.jpeg', 'animation_class': 'from-left'},
        {'title': 'The Future of Renewable Energy', 'category': 'Technology', 'summary': 'A look into the exciting advancements in solar, wind, and geothermal energy. How these technologies are shaping our future and combating climate change.', 'image_url': 'accounts/images/Blogs/renewable_energy.jpeg', 'animation_class': 'from-bottom'},
        {'title': 'Understanding Product Certifications', 'category': 'Consumer Guide', 'summary': 'Navigating eco-labels can be confusing. This guide breaks down common certifications like Organic, Fair Trade, and Leaping Bunny to help you make informed choices.', 'image_url': 'accounts/images/Blogs/product_certification.jpeg', 'animation_class': 'from-right'},
        {'title': 'Gardening for Biodiversity', 'category': 'Gardening', 'summary': 'Transform your garden into a haven for local wildlife. Learn how planting native species and creating habitats can boost biodiversity in your backyard.', 'image_url': 'accounts/images/Blogs/biodiversity.jpeg', 'animation_class': 'from-left'},
        {'title': 'The Power of Ethical Investing', 'category': 'Finance', 'summary': 'Align your investments with your values. Explore how ethical and sustainable investing can generate returns while supporting responsible companies.', 'image_url': 'accounts/images/Blogs/investing.jpeg', 'animation_class': 'from-bottom'},
        {'title': 'Minimalism: Less is More for the Planet', 'category': 'Lifestyle', 'summary': 'Embrace minimalism to reduce consumption and waste. Discover how decluttering your life can lead to a more sustainable and fulfilling existence.', 'image_url': 'accounts/images/Blogs/minimalism.jpeg', 'animation_class': 'from-right'},
        {'title': 'Green Living for City Dwellers', 'category': 'Urban Life', 'summary': 'Sustainable living isn\'t just for rural areas. This guide provides practical tips for reducing your environmental impact in an urban environment.', 'image_url': 'accounts/images/Blogs/green_city.jpeg', 'animation_class': 'from-left'},
        {'title': 'The Importance of Bees and Pollinators', 'category': 'Ecology', 'summary': 'Learn about the vital role bees and other pollinators play in our ecosystem and food supply, and what you can do to protect them.', 'image_url': 'accounts/images/Blogs/pollinators.jpeg', 'animation_class': 'from-bottom'},
        {'title': 'Reusable Products: A Comprehensive Guide', 'category': 'Productivity', 'summary': 'From coffee cups to food containers, making the switch to reusable items is easier than you think. Find out which reusable products are right for you.', 'image_url': 'accounts/images/Blogs/reusable_products.jpeg', 'animation_class': 'from-right'},
        {'title': 'The Circular Economy: A Sustainable Future', 'category': 'Economy', 'summary': 'Explore the principles of the circular economy and how it contrasts with traditional linear models. Discover how businesses and consumers are embracing reuse, repair, and recycling.', 'image_url': 'accounts/images/Blogs/circular_economy.jpeg', 'animation_class': 'from-bottom'},
    ]
    return render(request, 'accounts/blog.html', {'posts': blog_posts_data, 'page_title': 'Our Eco-Blog'})

# --- Other VIEWS (ensure these match your local file) ---
def about_us_view(request):
    return render(request, 'accounts/about.html', {'page_title': 'About EcoCart'})

def contact_view(request):
    return render(request, 'accounts/contact.html', {'page_title': 'Contact EcoCart'})

def forgot_password_view(request):
    return render(request, 'accounts/forgot_pass.html')

def product_list_view(request):
    products_data_mock = [
        {'id': 1, 'name': 'Bamboo Toothbrush', 'price': 150, 'category': 'Oral Care', 'eco_friendly': True, 'image_url': 'https://placehold.co/220x220/34D399/FFFFFF?text=Toothbrush'},
        {'id': 2, 'name': 'Reusable Shopping Bag', 'price': 300, 'category': 'Household', 'eco_friendly': True, 'image_url': 'https://placehold.co/220x220/6EE7B7/0F3F2D?text=Bag'},
        {'id': 3, 'name': 'Organic Cotton T-Shirt', 'price': 800, 'category': 'Apparel', 'eco_friendly': True, 'image_url': 'https://placehold.co/220x220/A7F3D0/0F3F2D?text=T-Shirt'},
        {'id': 4, 'name': 'Solid Shampoo Bar', 'price': 450, 'category': 'Personal Care', 'eco_friendly': True, 'image_url': 'https://placehold.co/200x200/D1FAE5/0F3F2D?text=Shampoo'},
        {'id': 5, 'name': 'Stainless Steel Water Bottle', 'price': 600, 'category': 'Hydration', 'eco_friendly': True, 'image_url': 'https://placehold.co/220x220/E0F2E5/0F3F2D?text=Bottle'},
        {'id': 6, 'name': 'Compostable Phone Case', 'price': 750, 'category': 'Accessories', 'eco_friendly': True, 'image_url': 'https://placehold.co/220x220/FDF8F0/0F3F2D?text=Phone+Case'},
        {'id': 7, 'name': 'Beeswax Food Wraps', 'price': 400, 'category': 'Kitchen', 'eco_friendly': True, 'image_url': 'https://placehold.co/220x220/6EE7B7/0F3F2D?text=Wraps'},
        {'id': 8, 'name': 'Biodegradable Laundry Pods', 'price': 900, 'category': 'Home Cleaning', 'eco_friendly': True, 'image_url': 'https://placehold.co/220x220/A7F3D0/0F3F2D?text=Pods'},
        {'id': 9, 'name': 'Recycled Notebook', 'price': 200, 'category': 'Stationery', 'eco_friendly': True, 'image_url': 'https://placehold.co/220x220/D1FAE5/0F3F2D?text=Notebook'},
        {'id': 10, 'name': 'Solar-Powered Charger', 'price': 1200, 'category': 'Electronics', 'eco_friendly': True, 'image_url': 'https://placehold.co/220x220/E0F2E5/0F3F2D?text=Charger'},
        {'id': 11, 'name': 'Upcycled Denim Bag', 'price': 700, 'category': 'Apparel', 'eco_friendly': True, 'image_url': 'https://placehold.co/220x220/FDF8F0/0F3F2D?text=Denim+Bag'},
        {'id': 12, 'name': 'Plant-Based Dish Soap', 'price': 250, 'category': 'Home Cleaning', 'eco_friendly': True, 'image_url': 'https://placehold.co/220x220/6EE7B7/0F3F2D?text=Dish+Soap'},
        {'id': 13, 'name': 'Wooden Toys Set', 'price': 1100, 'category': 'Kids & Baby', 'eco_friendly': True, 'image_url': 'https://placehold.co/220x220/A7F3D0/0F3F2D?text=Wooden+Toys'},
        {'id': 14, 'name': 'Eco-Friendly Yoga Mat', 'price': 1500, 'category': 'Fitness', 'eco_friendly': True, 'image_url': 'https://placehold.co/220x220/D1FAE5/0F3F2D?text=Yoga+Mat'},
        {'id': 15, 'name': 'Natural Soy Candle', 'price': 350, 'category': 'Home Decor', 'eco_friendly': True, 'image_url': 'https://placehold.co/220x220/E0F2E5/0F3F2D?text=Candle'},
    ]

    products_for_template = []
    for p in products_data_mock:
        products_for_template.append({
            'id': p['id'],
            'name': p['name'],
            'price': p['price'],
            'category': p['category'],
            'eco_friendly': p['eco_friendly'],
            'image': type('obj', (object,), {'url': p['image_url']})()
        })
    return render(request, 'products/product.html', {'products': products_for_template})