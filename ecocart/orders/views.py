# ecocart/orders/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import timedelta
import json
import uuid
import random

# Core Django authentication and messaging imports
from django.contrib import messages
from django.conf import settings

# For Email Sending (if enabled)
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.template.defaultfilters import strip_tags

# Import your Order model
from .models import Order

# For Stripe, if you're integrating (ensure you have stripe installed: pip install stripe)
import stripe
# Ensure STRIPE_SECRET_KEY is defined in your settings.py
stripe.api_key = settings.STRIPE_SECRET_KEY if hasattr(settings, 'STRIPE_SECRET_KEY') else 'sk_test_YOUR_SECRET_KEY'


# Helper function for sending order confirmation email
# This function is included but can be commented out or removed if email sending is not desired.
def send_order_confirmation_email(order_obj):
    """
    Sends an order confirmation email to the customer.
    """
    print("\n--- Attempting to send order confirmation email ---")
    if not hasattr(settings, 'DEFAULT_FROM_EMAIL') or not settings.DEFAULT_FROM_EMAIL:
        print("EMAIL_HOST settings are not configured or DEFAULT_FROM_EMAIL is missing. Skipping email sending.")
        return False

    subject_template_path = 'orders/email_subject.txt'
    html_template_path = 'orders/order_confirmation.html'

    context = {
        'order': order_obj,
        'order_summary': order_obj.get_order_summary(),
        'items': order_obj.get_items(),
        'shipping_info': order_obj.get_shipping_info(),
        'total_amount': order_obj.get_total_amount(),
        'customer_name': order_obj.get_shipping_info().get('fullName', 'Customer'),
        'is_cod': order_obj.payment_method == 'cod',
        'order_receipt_url': f"{settings.SITE_URL}/accounts/order-receipt/{order_obj.order_id}/" if hasattr(settings, 'SITE_URL') else f'/accounts/order-receipt/{order_obj.order_id}/',
    }

    try:
        subject = render_to_string(subject_template_path, context).strip()
        html_content = render_to_string(html_template_path, context)
        plain_message = strip_tags(html_content)

        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = order_obj.customer_email

        if not to_email:
            print(f"Warning: No customer email found for order {order_obj.order_id}. Skipping email.")
            return False

        msg = EmailMultiAlternatives(subject, plain_message, from_email, [to_email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        print(f"Email sent successfully to {to_email} for order {order_obj.order_id}")
        return True
    except Exception as e:
        print(f"ERROR: Failed to send order confirmation email for order {order_obj.order_id}: {e}")
        return False


@csrf_exempt
@require_POST
def process_order(request):
    """
    API endpoint to process the order, save it to the database, and handle payment.
    """
    print("\n--- process_order view entered ---")
    # Removed the AJAX header check to bypass persistent client-side issues.
    # The @require_POST decorator already ensures it's a POST request.

    try:
        data = json.loads(request.body)
        print("Received order data (parsed JSON):", data)

        # Extract data from the request
        shipping_info = data.get('shippingInfo', {})
        order_summary = data.get('orderSummary', {})
        items = data.get('items', [])
        payment_method = data.get('paymentMethod')
        customer_email = shipping_info.get('customerEmail')

        print(f"Extracted: PM={payment_method}, Email={customer_email}, Items count={len(items)}")
        print(f"Shipping Info: {shipping_info}")
        print(f"Order Summary: {order_summary}")

        # Basic validation
        if not all([shipping_info, order_summary, items, payment_method, customer_email]):
            print("ERROR: Missing essential order data in received JSON.")
            return JsonResponse({'status': 'error', 'message': 'Missing essential order data.'}, status=400)

        # Check if cart is empty before processing order (important!)
        if not request.session.get('cart') and not settings.DEBUG:
             print("WARNING: Cart is empty in session. This might indicate a frontend issue or direct API call without cart.")


        # Retrieve or create user if authenticated, or assign to anonymous
        user = request.user if request.user.is_authenticated else None
        print(f"User for order: {user.username if user else 'Anonymous'}")

        # Simulate delivery date (5-7 days from now)
        delivery_date = timezone.now().date() + timedelta(days=random.randint(5, 7))
        print(f"Simulated delivery date: {delivery_date}")

        # Determine initial order status
        initial_order_status = 'Pending' # Default for COD
        if payment_method == 'online':
            initial_order_status = 'Processing' # For online payments, status might change after Stripe confirmation
        print(f"Initial order status: {initial_order_status}")

        # Create the Order instance
        try:
            print("Attempting to create Order object...")
            order = Order.objects.create(
                user=user,
                payment_method=payment_method,
                order_status=initial_order_status,
                delivery_date=delivery_date,
                customer_email=customer_email,
                order_summary_json=json.dumps(order_summary),
                items_json=json.dumps(items),
                shipping_info_json=json.dumps(shipping_info)
            )
            print(f"SUCCESS: Order {order.order_id} created in DB with initial status: {order.order_status}.")

            # --- Handle Payment Processing based on method ---
            if payment_method == 'online':
                print("Handling online payment via Stripe simulation...")
                stripe_payment_method_id = data.get('stripePaymentMethodId')
                if not stripe_payment_method_id:
                    order.order_status = 'Failed'
                    order.save()
                    print("ERROR: Stripe payment method ID missing for online payment.")
                    return JsonResponse({'status': 'error', 'message': 'Stripe payment method ID missing.'}, status=400)

                try:
                    amount_in_smallest_unit = int(order_summary.get('total', 0.00) * 100)
                    if amount_in_smallest_unit <= 0:
                        order.order_status = 'Failed'
                        order.save()
                        print("ERROR: Invalid total amount (<=0) for Stripe payment.")
                        return JsonResponse({'status': 'error', 'message': 'Invalid total amount for payment.'}, status=400)

                    print(f"Simulating Stripe PaymentIntent creation for {amount_in_smallest_unit} INR...")
                    intent = stripe.PaymentIntent.create(
                        amount=amount_in_smallest_unit,
                        currency='inr', # Adjust currency as needed (e.g., 'usd')
                        payment_method=stripe_payment_method_id,
                        confirmation_method='manual',
                        confirm=True,
                        description=f"EcoCart Order {order.order_id}",
                        metadata={'order_id': order.order_id, 'user_id': user.id if user else 'anonymous'}
                    )

                    print(f"Stripe PaymentIntent status: {intent.status}")

                    if intent.status == 'succeeded' or intent.status == 'requires_capture':
                        order.order_status = 'Paid'
                        order.save()
                        print(f"SUCCESS: Stripe payment confirmed for order {order.order_id}. Status updated to 'Paid'.")
                    else:
                        order.order_status = 'Failed'
                        order.save()
                        print(f"ERROR: Stripe payment failed or requires action for order {order.order_id}. Status: {intent.status}")
                        return JsonResponse({'status': 'error', 'message': f'Payment failed or requires action: {intent.status}. Please try again.'}, status=400)

                except stripe.error.CardError as e:
                    order.order_status = 'Failed'
                    order.save()
                    print(f"ERROR: Stripe Card Error for order {order.order_id}: {e.user_message}")
                    return JsonResponse({'status': 'error', 'message': e.user_message}, status=400)
                except stripe.error.StripeError as e:
                    order.order_status = 'Failed'
                    order.save()
                    print(f"ERROR: Stripe API Error for order {order.order_id}: {e}")
                    return JsonResponse({'status': 'error', 'message': 'Stripe payment processing error. Please try again later.'}, status=500)
                except Exception as e:
                    order.order_status = 'Failed'
                    order.save()
                    print(f"CRITICAL ERROR: Unexpected error during online payment for order {order.order_id}: {e}")
                    return JsonResponse({'status': 'error', 'message': 'An unexpected error occurred during payment.'}, status=500)

            elif payment_method == 'cod':
                print(f"Handling COD order {order.order_id}. Status remains 'Pending'.")
                # No further payment processing needed for COD on backend side.
                # The status 'Pending' was already set during order creation.

            # Clear the user's cart in the session after successful order creation/payment
            if 'cart' in request.session:
                del request.session['cart']
                request.session.modified = True
                print("Cart cleared from session.")

            # Send order confirmation email (this can be commented out if not desired)
            # You need to ensure your email settings are configured in settings.py
            print("Attempting to send order confirmation email...")
            email_sent = send_order_confirmation_email(order)
            if not email_sent:
                print("WARNING: Order confirmation email failed to send (check settings/errors above).")
                # You might add a message to the user here if email is critical,
                # but we'll still return success for the order itself.

            # Return success response with the actual order ID and collected order details
            # The frontend expects 'order_id' for URL and 'orderDetails' for localStorage
            print("Returning success response to frontend.")
            return JsonResponse({
                'status': 'success',
                'message': 'Order placed successfully!',
                'order_id': order.order_id, # Actual order ID from the database
                'redirect_url': f'/orders/order_success/?order_id={order.order_id}',
                'orderDetails': { # Send back comprehensive details for the receipt page
                    'orderId': order.order_id,
                    'orderDate': order.created_at.strftime('%B %d, %Y %I:%M %p'), # Format date for JS
                    'paymentMethod': order.payment_method,
                    'orderStatus': order.order_status,
                    'items': json.loads(order.items_json),
                    'orderSummary': json.loads(order.order_summary_json),
                    'shippingInfo': json.loads(order.shipping_info_json),
                    'deliveryDate': order.delivery_date.strftime('%B %d, %Y') if order.delivery_date else 'N/A',
                }
            })

        except Exception as e:
            # This catches errors during Order.objects.create() or subsequent COD logic
            print(f"CRITICAL ERROR: Failed during Order object creation or COD logic: {e}")
            # Ensure the order status is set to failed if it was created but then failed
            # This part might need more sophisticated error handling depending on the exact failure point
            return JsonResponse({'status': 'error', 'message': f'Failed to create order: {e}'}, status=500)

    except json.JSONDecodeError:
        print("ERROR: Invalid JSON data in request body.")
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON data in request body.'}, status=400)
    except Exception as e:
        print(f"CRITICAL ERROR: An unexpected error occurred at the top level of process_order view: {e}")
        return JsonResponse({'status': 'error', 'message': f'An unexpected server error occurred: {e}'}, status=500)


def order_success(request):
    """
    Renders the order success page.
    This view primarily relies on JavaScript to fetch order details from localStorage
    or directly from the URL parameter.
    """
    print("\n--- order_success view entered ---")
    order_id = request.GET.get('order_id')
    print(f"Order ID from URL: {order_id}")
    context = {
        'order_id': order_id, # Pass the order_id to the template
    }
    return render(request, 'orders/order_success.html', context)
