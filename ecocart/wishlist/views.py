from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import WishlistItem
from products.models import Product
from .forms import AddToWishlistForm

@login_required
def wishlist_view(request):
    wishlist = WishlistItem.objects.filter(user=request.user)
    return render(request, 'wishlist/wishlist.html', {'wishlist': wishlist})

@login_required
def add_to_wishlist(request):
    if request.method == 'POST':
        form = AddToWishlistForm(request.POST)
        if form.is_valid():
            product = get_object_or_404(Product, id=form.cleaned_data['product_id'])
            WishlistItem.objects.get_or_create(user=request.user, product=product)
    return redirect('wishlist')

@login_required
def remove_from_wishlist(request, product_id):
    WishlistItem.objects.filter(user=request.user, product__id=product_id).delete()
    return redirect('wishlist')
