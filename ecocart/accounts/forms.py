from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    """
    A custom form for creating new CustomUser instances.
    Extends Django's built-in UserCreationForm.
    """
    profile_picture = forms.ImageField(required=False, label="Profile Picture")
    email = forms.EmailField(required=True, label="Email Address") # Ensure email is required
    phone = forms.CharField(max_length=15, required=False, label="Phone Number")
    gender = forms.ChoiceField(choices=CustomUser.GENDER_CHOICES, required=False, label="Gender")
    bio = forms.CharField(widget=forms.Textarea, required=False, label="Biography")
    address = forms.CharField(max_length=255, required=False, label="Shipping Address")

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        # Include all fields from CustomUser that you want to be editable during creation
        # UserCreationForm.Meta.fields already includes username, password, password2
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name', 'phone', 'gender', 'profile_picture', 'bio', 'address')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control rounded-md px-3 py-2 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-emerald-500 transition duration-200'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control rounded-md px-3 py-2 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-emerald-500 transition duration-200'}),
            'email': forms.EmailInput(attrs={'class': 'form-control rounded-md px-3 py-2 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-emerald-500 transition duration-200'}),
            'username': forms.TextInput(attrs={'class': 'form-control rounded-md px-3 py-2 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-emerald-500 transition duration-200'}),
            'phone': forms.TextInput(attrs={'class': 'form-control rounded-md px-3 py-2 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-emerald-500 transition duration-200', 'placeholder': 'e.g., +91 12345 67890'}),
            'gender': forms.Select(attrs={'class': 'form-control rounded-md px-3 py-2 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-emerald-500 transition duration-200'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 focus:outline-none file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-emerald-50 file:text-emerald-700 hover:file:bg-emerald-100'}),
            'bio': forms.Textarea(attrs={'class': 'form-control rounded-md px-3 py-2 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-emerald-500 transition duration-200 h-24', 'placeholder': 'Tell us about yourself...'}),
            'address': forms.TextInput(attrs={'class': 'form-control rounded-md px-3 py-2 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-emerald-500 transition duration-200', 'placeholder': 'Your full shipping address'}),
        }


class CustomUserChangeForm(UserChangeForm):
    """
    A custom form for changing existing CustomUser instances.
    Extends Django's built-in UserChangeForm.
    """
    password = None # Don't show password field for user updates
    profile_picture = forms.ImageField(required=False, label="Profile Picture") # Moved this declaration here

    class Meta:
        model = CustomUser
        # Include all fields from CustomUser that you want to be editable during change
        # Exclude 'password' as it's handled by separate password change views
        fields = ('username', 'email', 'phone', 'gender', 'profile_picture', 'bio', 'address', 'first_name', 'last_name')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control rounded-md px-3 py-2 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-emerald-500 transition duration-200'}),
            'username': forms.TextInput(attrs={'class': 'form-control rounded-md px-3 py-2 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-emerald-500 transition duration-200'}),
            'phone': forms.TextInput(attrs={'class': 'form-control rounded-md px-3 py-2 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-emerald-500 transition duration-200', 'placeholder': 'e.g., +91 12345 67890'}),
            'gender': forms.Select(attrs={'class': 'form-control rounded-md px-3 py-2 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-emerald-500 transition duration-200'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 focus:outline-none file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-emerald-50 file:text-emerald-700 hover:file:bg-emerald-100'}),
            'bio': forms.Textarea(attrs={'class': 'form-control rounded-md px-3 py-2 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-emerald-500 transition duration-200 h-24', 'placeholder': 'Tell us about yourself...'}),
            'address': forms.TextInput(attrs={'class': 'form-control rounded-md px-3 py-2 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-emerald-500 transition duration-200', 'placeholder': 'Your full shipping address'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control rounded-md px-3 py-2 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-emerald-500 transition duration-200'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control rounded-md px-3 py-2 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-emerald-500 transition duration-200'}),
        }
