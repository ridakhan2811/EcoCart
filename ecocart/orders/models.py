# ecocart/orders/models.py

from django.db import models
from django.conf import settings
import json
import uuid # <-- ADD THIS IMPORT

# Define a helper function for the default outside the class
def get_default_order_id():
    """Generates a unique order ID."""
    return 'ECO-' + str(uuid.uuid4().hex[:9]).upper()

class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="The user who placed the order (can be anonymous)"
    )
    order_id = models.CharField(
        max_length=100,
        unique=True,
        default=get_default_order_id # <-- FIX IS HERE: Reference the named function
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    payment_method = models.CharField(max_length=50)
    order_status = models.CharField(max_length=50, default='Pending')
    delivery_date = models.DateField(null=True, blank=True)

    order_summary_json = models.TextField()
    items_json = models.TextField()
    shipping_info_json = models.TextField()
    customer_email = models.EmailField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order {self.order_id}"

    def get_order_summary(self):
        return json.loads(self.order_summary_json) if self.order_summary_json else {}

    def get_items(self):
        return json.loads(self.items_json) if self.items_json else []

    def get_shipping_info(self):
        return json.loads(self.shipping_info_json) if self.shipping_info_json else {}

    def get_subtotal(self):
        return self.get_order_summary().get('subtotal', 0.00)

    def get_shipping_cost(self):
        return self.get_order_summary().get('shippingCost', 0.00)

    def get_discount_amount(self):
        return self.get_order_summary().get('discountAmount', 0.00)

    def get_total_amount(self):
        return self.get_order_summary().get('total', 0.00)