# ecocart/coupons/models.py

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Coupon(models.Model):
    """
    Model to store coupon codes and their properties.
    Admins can create and manage these coupons from the Django admin interface.
    """
    DISCOUNT_TYPE_CHOICES = [
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
        ('shipping', 'Free Shipping'),
    ]

    code = models.CharField(
        max_length=50,
        unique=True,
        help_text="The unique code users will enter (e.g., FESTIVE20, FREESHIP)"
    )
    discount_type = models.CharField(
        max_length=10,
        choices=DISCOUNT_TYPE_CHOICES,
        default='percentage',
        help_text="Type of discount: Percentage, Fixed Amount, or Free Shipping"
    )
    value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Discount value (e.g., 0.10 for 10%, 20.00 for ₹20 fixed, 0 for free shipping)"
    )
    minimum_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0)],
        help_text="Minimum order total required to use this coupon (optional)"
    )
    active = models.BooleanField(
        default=True,
        help_text="Is this coupon currently active and usable?"
    )
    valid_from = models.DateTimeField(
        help_text="Date and time from which the coupon is valid"
    )
    valid_to = models.DateTimeField(
        help_text="Date and time until which the coupon is valid"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Coupon"
        verbose_name_plural = "Coupons"
        ordering = ['-created_at'] # Order by most recent first

    def __str__(self):
        """String representation for the Django admin."""
        if self.discount_type == 'percentage':
            return f"{self.code} ({self.value * 100:.0f}% off)"
        elif self.discount_type == 'fixed':
            return f"{self.code} (₹{self.value:.2f} off)"
        elif self.discount_type == 'shipping':
            return f"{self.code} (Free Shipping)"
        return self.code

    def get_discount(self, total_amount):
        """
        Calculates the discount amount based on the coupon and total order amount.
        Returns (discount_amount, is_valid_for_amount, is_free_shipping).
        """
        is_valid_for_amount = total_amount >= self.minimum_amount
        is_free_shipping = False
        discount_amount = 0

        if not self.active:
            return 0, False, False # Coupon not active

        # Check if coupon is within its valid date range
        from django.utils import timezone
        now = timezone.now()
        if not (self.valid_from <= now <= self.valid_to):
            return 0, False, False # Coupon expired or not yet valid

        if not is_valid_for_amount:
            return 0, False, False # Minimum amount not met

        if self.discount_type == 'percentage':
            discount_amount = total_amount * self.value
        elif self.discount_type == 'fixed':
            discount_amount = self.value
        elif self.discount_type == 'shipping':
            is_free_shipping = True
            # For free shipping, discount_amount is 0, but shipping cost will be set to 0 later

        return discount_amount, True, is_free_shipping
