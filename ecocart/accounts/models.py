from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    Includes fields for email, phone, gender, profile picture,
    and integrated fields previously found in the separate Profile model (bio, address).
    """
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, verbose_name="Phone Number")

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True, default='default.jpg')
    
    # Fields moved from the previous 'Profile' model - ADDED THESE
    bio = models.TextField(blank=True, null=True, verbose_name="Biography")
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="Shipping Address")

    def __str__(self):
        """
        String representation of the CustomUser object.
        """
        return self.username

    # Note: Image resizing logic is typically handled in forms or signals,
    # not directly overriding AbstractUser's save method to avoid complexities.
