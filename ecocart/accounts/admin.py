from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm # Import your custom forms

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Custom Admin configuration for the CustomUser model.
    Extends Django's default UserAdmin to include custom fields.
    Uses CustomUserCreationForm for adding users and CustomUserChangeForm for changing users.
    """
    # Use your custom forms for adding and changing users in the admin
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    # Fields to display in the list view of the admin
    list_display = ('username', 'email', 'phone', 'gender', 'first_name', 'last_name', 'is_staff', 'is_active')
    
    # Fields to filter by in the admin sidebar
    list_filter = ('is_staff', 'is_active', 'gender', 'groups')
    
    # Fields to search by
    search_fields = ('username', 'email', 'phone', 'first_name', 'last_name')
    
    # Ordering of users in the list view
    ordering = ('email',)

    # Fieldsets for organizing fields in the add/change user form
    # We are extending the default UserAdmin fieldsets
    # Note: UserAdmin.fieldsets already includes password fields for existing users
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone', 'gender', 'profile_picture', 'bio', 'address')}),
    )
    
    # Add custom fields to the add_fieldsets for creating new users in admin
    # UserAdmin.add_fieldsets already includes username, password, password2
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email', 'phone', 'gender', 'profile_picture', 'bio', 'address', 'first_name', 'last_name')}),
    )

