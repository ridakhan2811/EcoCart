# ecocart/coupons/admin.py

from django.contrib import admin
from .models import Coupon

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    """
    Customizing the Coupon model display in the Django admin interface.
    """
    list_display = (
        'code',
        'discount_type',
        'value',
        'active',
        'valid_from',
        'valid_to',
        'minimum_amount',
        'created_at',
    )
    list_filter = ('active', 'discount_type', 'valid_from', 'valid_to')
    search_fields = ('code',)
    date_hierarchy = 'valid_from' # Adds a date navigation bar for valid_from field
    ordering = ('-valid_from',) # Default ordering in admin list
    fieldsets = (
        (None, {
            'fields': ('code', 'discount_type', 'value', 'minimum_amount', 'active')
        }),
        ('Validity Dates', {
            'fields': ('valid_from', 'valid_to'),
            'classes': ('collapse',) # Makes this section collapsible in admin
        }),
    )
