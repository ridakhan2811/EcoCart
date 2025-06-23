from django import forms

class AddToWishlistForm(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput())
