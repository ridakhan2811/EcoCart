# ecocart/orders/admin.py

from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Admin interface for the Order model.
    """
    list_display = (
        'order_id',
        'user',
        'customer_email',
        'payment_method',
        'order_status',
        'delivery_date',
        'created_at',
    )
    list_filter = ('order_status', 'payment_method', 'created_at', 'delivery_date')
    search_fields = ('order_id', 'user__username', 'customer_email')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('order_id', 'user', 'customer_email', 'payment_method', 'order_status', 'delivery_date')
        }),
        ('Order Details (JSON)', {
            'fields': ('order_summary_json', 'items_json', 'shipping_info_json'),
            'classes': ('collapse',) # Makes this section collapsible
        }),
    )
