from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Import your CustomUser model and the updated forms
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm # Ensure CustomUserChangeForm is imported

# Dummy pick-up lines (if used elsewhere, otherwise can be removed)
PICK_UP_LINES = [
    "Sustainable Choices, Happy Planet.",
    "Shop Smarter, Live Greener.",
    "Eco-Friendly Excellence at Your Fingertips.",
    "Making a Difference, One Product at a Time.",
    "Your Journey to Sustainable Living Starts Here.",
]

def home_view(request):
    """
    Renders the main landing page.
    """
    return render(request, 'accounts/home.html')

def register_view(request):
    """
    Handles user registration.
    Redirects to accounts:login upon successful registration.
    """
    if request.method == 'POST':
        # --- ENHANCED DEBUG PRINTS ---
        print("\n--- REGISTER VIEW: POST Request Received ---")
        print("request.POST:", request.POST)
        print("request.FILES:", request.FILES)
        # --- END ENHANCED DEBUG PRINTS ---

        # Pass request.FILES to handle profile_picture upload
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # No automatic login after registration, redirect to login page instead
            messages.success(request, f"Account created for {user.username}! Please log in.")
            print(f"--- REGISTER VIEW: Form is VALID. Redirecting to accounts:login for user {user.username} ---")
            return redirect('accounts:login') # Redirect to login page
        else:
            # --- DEBUG PRINT: This will show validation errors in your terminal ---
            print("--- REGISTER VIEW: Form is NOT valid. Errors: ---")
            print(form.errors)
            print("--------------------------------------------------")
            # --- END DEBUG PRINT ---

            # Display form errors using messages
            # This block should be working if messages are configured correctly
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.replace('_', ' ').title()}: {error}")
            # Also add a general error message if there are any non-field errors
            if form.non_field_errors():
                for error in form.non_field_errors():
                    messages.error(request, f"Error: {error}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    """
    Handles user login.
    Redirects to products:list upon successful login.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('products:list') # Redirect to the products list page
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'accounts/login.html')

@login_required
def profile_view(request):
    """
    Handles displaying and updating CustomUser profile information.
    """
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('accounts:profile') # Redirect back to profile to show updates
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.replace('_', ' ').title()}: {error}")
    else:
        form = CustomUserChangeForm(instance=request.user)

    context = {
        'form': form,
        'user_object': request.user # Pass the user object directly for display in template
    }
    return render(request, 'accounts/profile.html', context)

def logout_view(request):
    """
    Logs out the user and redirects to the login page.
    """
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('accounts:login') # Redirect to login page after logout

# --- BLOG VIEW ---
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

# --- Other VIEWS ---
def about_us_view(request):
    """
    Renders the About Us page.
    """
    return render(request, 'accounts/about.html', {'page_title': 'About EcoCart'})

def contact_view(request):
    """
    Renders the Contact page.
    """
    return render(request, 'accounts/contact.html', {'page_title': 'Contact EcoCart'})

def forgot_password_view(request):
    """
    Renders the Forgot Password page.
    """
    return render(request, 'accounts/forgot_pass.html')
