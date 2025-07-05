{# products/templates/products/checkout.html #}
{% load static %}

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Checkout | EcoCart</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    {# Load Stripe.js library conditionally - only if online payment is chosen #}
    {% if payment_method == 'online' %}
    <script src="https://js.stripe.com/v3/"></script>
    {% endif %}
    <style>
        :root {
            --color-primary-lightest: #E8F5E9; /* Lightest green */
            --color-primary-medium: #A5D6A7;   /* Medium green */
            --color-primary-dark: #66BB6A; /* Darker green */
            --color-emerald-800: #065F46; /* From your landing page header */
            --color-emerald-600: #059669; /* From your landing page buttons */
        }

        body {
            font-family: 'Poppins', sans-serif;
            @apply bg-gray-50 text-gray-800;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }

        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #f1f1f1;
        }
        ::-webkit-scrollbar-thumb {
            background: var(--color-primary-medium);
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: var(--color-primary-dark);
        }

        /* Message Box Styles (consistent across pages) */
        #message-box {
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            padding: 1rem 1.5rem;
            border-radius: 0.5rem;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
            color: white;
            z-index: 1000;
            opacity: 0;
            transform: translateY(20px);
            transition: opacity 0.4s ease-out, transform 0.4s ease-out;
            pointer-events: none;
        }

        #message-box.show {
            opacity: 1;
            transform: translateY(0);
            pointer-events: auto;
        }

        #message-box.hidden {
            display: none;
        }

        #message-box.bg-green-600 { background-color: #059669; }
        #message-box.bg-red-600 { background-color: #dc2626; }
        #message-box.bg-blue-600 { background-color: #2563eb; }
        #message-box.bg-gray-700 { background-color: #374151; }

        /* Checkout specific styles */
        .checkout-container {
            display: grid;
            gap: 2rem;
            padding: 2rem;
            max-width: 900px;
            margin: 0 auto;
        }

        @media (min-width: 768px) { /* Medium screens and up */
            .checkout-container {
                grid-template-columns: 1.5fr 1fr; /* Billing/Shipping on left, Order Summary/Payment on right */
            }
        }

        .form-label {
            @apply block text-gray-700 text-sm font-bold mb-2;
        }
        .form-input {
            @apply shadow appearance-none border rounded w-full py-3 px-4 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent;
        }
        .form-select {
            @apply block appearance-none w-full bg-white border border-gray-400 hover:border-gray-500 px-4 py-3 pr-8 rounded shadow leading-tight focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent;
        }
        .submit-button {
            @apply w-full py-3 rounded-full font-bold text-white transition-all duration-300 ease-in-out transform hover:scale-105 active:scale-95;
            background: linear-gradient(to right, #059669, #10B981); /* Emerald gradient */
            box-shadow: 0 4px 10px rgba(5, 150, 105, 0.4);
        }
        .submit-button:hover {
            box-shadow: 0 6px 15px rgba(5, 150, 105, 0.6);
        }

        /* Stripe Elements styling */
        #card-element {
            border: 1px solid #e2e8f0; /* Tailwind gray-300 */
            padding: 0.75rem 1rem;
            border-radius: 0.25rem;
            background-color: white;
            box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            transition: all 0.2s ease-in-out;
        }
        #card-element.StripeElement--focus {
            border-color: #10B981; /* Tailwind emerald-500 */
            box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.3); /* Ring effect */
        }
        .StripeElement--invalid {
            border-color: #ef4444; /* Tailwind red-500 */
        }
        .StripeElement--webkit-autofill {
            background-color: #fefcbf !important; /* Tailwind yellow-100 */
        }

        #card-errors {
            @apply text-red-500 text-sm mt-2;
        }

        .promo-input {
            @apply flex-grow p-3 border border-gray-300 rounded-l-lg focus:outline-none focus:ring-2 focus:ring-emerald-500;
        }
        .apply-promo-btn {
            @apply px-5 py-3 bg-emerald-600 text-white font-semibold rounded-r-lg hover:bg-emerald-700 transition-colors duration-200;
        }
    </style>
</head>
<body class="min-h-screen flex flex-col">

    {# START OF HEADER/NAV BAR CONTENT #}
    <header id="main-navbar" class="bg-emerald-800 p-4 shadow-lg sticky top-0 z-40 transition-all duration-300 ease-in-out">
        <div class="container mx-auto flex items-center justify-between flex-wrap">
            {# Left side of navbar: EcoCart Logo #}
            <a href="{% url 'accounts:home' %}" class="flex items-center flex-shrink-0 text-white mr-6">
                <span class="font-bold text-3xl tracking-tight text-white flex items-center">
                    EcoCart <span class="ml-2 text-green-300">🌿</span>
                </span>
            </a>

            <div class="block lg:hidden">
                <button id="nav-toggle" class="flex items-center px-3 py-2 border rounded text-green-200 border-green-400 hover:text-white hover:border-white focus:outline-none focus:ring-2 focus:ring-white">
                    <svg class="fill-current h-3 w-3" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><title>Menu</title><path d="M0 3h20v2H0V3zm0 6h20v2H0V9zm0 6h20v2H0v-2z"/></svg>
                </button>
            </div>

            <div id="nav-content" class="w-full block flex-grow lg:flex lg:items-center lg:w-auto hidden">
                <div class="text-lg lg:flex-grow">
                    <a href="{% url 'products:list' %}" class="block mt-4 lg:inline-block lg:mt-0 text-white hover:text-green-200 mr-6 transition duration-300 ease-in-out">
                        Shop Eco
                    </a>
                    <a href="{% url 'accounts:blog' %}" class="block mt-4 lg:inline-block lg:mt-0 text-white hover:text-green-200 mr-6 transition duration-300 ease-in-out">
                        Blog
                    </a>
                    <a href="{% url 'accounts:about_us' %}" class="block mt-4 lg:inline-block lg:mt-0 text-white hover:text-green-200 mr-6 transition duration-300 ease-in-out">
                        About Us
                    </a>
                    <a href="{% url 'accounts:contact' %}" class="block mt-4 lg:inline-block lg:mt-0 text-white hover:text-green-200 transition duration-300 ease-in-out">
                        Contact
                    </a>
                </div>
                <div class="flex items-center">
                    {# Cart Icon and Count #}
                    <a href="{% url 'accounts:cart_detail' %}" class="text-white text-xl relative mr-6 mt-4 lg:mt-0">
                        <i class="fas fa-shopping-cart"></i>
                        <span id="cart-count" class="absolute -top-2 -right-2 bg-red-500 text-white text-xs rounded-full px-2 py-1">0</span>
                    </a>

                    {% if user.is_authenticated %}
                        {# Profile Picture and Name moved to the right #}
                        <a href="{% url 'accounts:profile' %}" class="flex items-center text-white text-lg hover:text-green-200 transition duration-300 ease-in-out mr-4 mt-4 lg:mt-0">
                            <img src="{% if user.profile.profile_picture %}{{ user.profile.profile_picture.url }}{% else %}{% static 'products/images/placeholder.jpg' %}{% endif %}"
                                 onerror="this.onerror=null; this.src='{% static 'products/images/placeholder.jpg' %}';"
                                 alt="{{ user.username }} Profile Picture"
                                 class="w-8 h-8 rounded-full border-2 border-white object-cover mr-2">
                            <span class="hidden sm:inline">{{ user.username }}</span>
                        </a>
                        <a href="{% url 'accounts:logout' %}" class="inline-block text-lg px-4 py-2 leading-none border border-white rounded-full text-white hover:bg-white hover:text-emerald-800 mt-4 lg:mt-0 transition duration-300 ease-in-out">
                            Logout
                        </a>
                    {% else %}
                        <a href="{% url 'accounts:login' %}" class="inline-block text-lg px-4 py-2 leading-none border border-white rounded-full text-white hover:bg-white hover:text-emerald-800 mt-4 lg:mt-0 transition duration-300 ease-in-out mr-2">
                            Login
                        </a>
                        <a href="{% url 'accounts:register' %}" class="inline-block text-lg px-4 py-2 leading-none border border-white rounded-full text-white hover:bg-white hover:text-emerald-800 mt-4 lg:mt-0 transition duration-300 ease-in-out">
                            Register
                        </a>
                    {% endif %}
                </div>
            </div>
        </div>
    </header>
    {# END OF HEADER/NAV BAR CONTENT #}

    <main class="flex-grow container mx-auto px-4 py-8">
        <h1 class="text-4xl font-bold text-center text-gray-900 mb-10 tracking-tight">Secure Checkout</h1>

        <div class="checkout-container bg-white p-8 rounded-lg shadow-xl">
            {# Left Column: Billing & Shipping Address #}
            <section>
                <h2 class="text-2xl font-semibold text-gray-800 mb-6 border-b pb-4">Shipping Information</h2>
                <form id="shipping-form" class="space-y-4">
                    <div>
                        <label for="full-name" class="form-label">Full Name</label>
                        <input type="text" id="full-name" class="form-input" placeholder="John Doe" required>
                    </div>
                    <div>
                        <label for="email" class="form-label">Email Address</label> {# NEW: Email Input #}
                        <input type="email" id="email" class="form-input" placeholder="you@example.com" value="{% if user.is_authenticated %}{{ user.email }}{% endif %}" required>
                    </div>
                    <div>
                        <label for="address-line1" class="form-label">Address Line 1</label>
                        <input type="text" id="address-line1" class="form-input" placeholder="123 Eco Street" required>
                    </div>
                    <div>
                        <label for="address-line2" class="form-label">Address Line 2 (Optional)</label>
                        <input type="text" id="address-line2" class="form-input" placeholder="Apt 4B">
                    </div>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <label for="city" class="form-label">City</label>
                            <input type="text" id="city" class="form-input" placeholder="Greenville" required>
                        </div>
                        <div>
                            <label for="state" class="form-label">State / Province</label>
                            <input type="text" id="state" class="form-input" placeholder="CA" required>
                        </div>
                    </div>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <label for="zip-code" class="form-label">Zip Code</label>
                            <input type="text" id="zip-code" class="form-input" placeholder="90210" required>
                        </div>
                        <div>
                            <label for="country" class="form-label">Country</label>
                            <select id="country" class="form-select" required>
                                <option value="IN">India</option>
                                <option value="US">United States</option>
                                <option value="CA">Canada</option>
                                <option value="GB">United Kingdom</option>
                                {# Add more countries as needed #}
                            </select>
                        </div>
                    </div>
                    <div>
                        <label for="phone-number" class="form-label">Phone Number</label>
                        <input type="tel" id="phone-number" class="form-input" placeholder="+91 9876543210" required>
                    </div>
                </form>
            </section>

            {# Right Column: Order Summary & Payment #}
            <aside>
                <h2 class="text-2xl font-semibold text-gray-800 mb-6 border-b pb-4">Order Summary</h2>
                <div class="space-y-3 text-lg mb-6">
                    <div class="flex justify-between">
                        <span>Items Subtotal:</span>
                        <span class="font-semibold">₹<span id="checkout-subtotal">0.00</span></span>
                    </div>
                    <div class="flex justify-between">
                        <span>Shipping:</span>
                        <span class="font-semibold">₹<span id="checkout-shipping">0.00</span></span>
                    </div>
                    <div class="flex justify-between text-emerald-600 font-bold" id="checkout-discount-row" style="display: none;">
                        <span>Discount (<span id="checkout-promo-code-display"></span>):</span>
                        <span>- ₹<span id="checkout-discount">0.00</span></span>
                    </div>
                    <div class="border-t border-gray-200 pt-4 flex justify-between items-center text-2xl font-bold text-gray-900">
                        <span>Total:</span>
                        <span>₹<span id="checkout-total">0.00</span></span>
                    </div>
                </div>

                {# Promo Code Section - REMAINS ON CHECKOUT PAGE ONLY #}
                <div class="mt-8">
                    <h3 class="text-xl font-semibold text-gray-800 mb-4">Have a promo code?</h3>
                    <div class="flex">
                        <input type="text" id="promo-code-input" placeholder="Enter code" class="promo-input">
                        <button id="apply-promo-btn" class="apply-promo-btn">Apply</button>
                    </div>
                    <p id="promo-message" class="text-sm mt-2"></p>
                </div>

                <h2 class="text-2xl font-semibold text-gray-800 mb-6 border-b pb-4 mt-8">Payment Information</h2>

                {# Conditional Payment Form based on selection from cart page #}
                {% if payment_method == 'online' %}
                    <div id="online-payment-section">
                        <form id="payment-form" class="space-y-4">
                            <div>
                                <label for="card-name" class="form-label">Name on Card</label>
                                <input type="text" id="card-name" class="form-input" placeholder="John Doe" required>
                            </div>
                            <div>
                                <label class="form-label">Card Details</label>
                                <div id="card-element">
                                    {# A Stripe Element will be inserted here by Stripe.js #}
                                </div>
                                {# Used to display form errors from Stripe.js #}
                                <div id="card-errors" role="alert"></div>
                            </div>
                            <button id="submit-button-online" class="submit-button mt-6">
                                Pay Now <i class="fas fa-lock ml-2"></i>
                            </button>
                            <p class="text-xs text-gray-500 text-center mt-4">
                                Your payment is securely processed by Stripe. This is a simulation.
                            </p>
                        </form>
                    </div>
                {% elif payment_method == 'cod' %}
                    <div id="cod-payment-section" class="text-center py-8">
                        <p class="text-lg text-gray-700 mb-6">You have selected **Cash on Delivery (COD)**.</p>
                        <p class="text-md text-gray-600 mb-8">Please confirm your order. Payment will be collected upon delivery.</p>
                        <button id="submit-button-cod" class="submit-button mt-6">
                            Confirm Order (COD) <i class="fas fa-truck-fast ml-2"></i>
                        </button>
                    </div>
                {% else %}
                    <div class="text-center py-8 text-red-500">
                        <p>Invalid payment method selected. Please go back to cart and choose a method.</p>
                        <a href="{% url 'accounts:cart_detail' %}" class="mt-4 inline-block text-emerald-600 hover:underline">Go to Cart</a>
                    </div>
                {% endif %}
            </aside>
        </div>

        {# Simple Message Box for confirmations #}
        <div id="message-box" class="fixed bottom-8 right-8 bg-green-600 text-white px-6 py-4 rounded-lg shadow-xl hidden z-50 transition-opacity duration-300 ease-out opacity-0">
            Message will appear here.
        </div>

    </main>

    {# START OF FOOTER CONTENT #}
    <footer class="bg-emerald-800 text-green-100 py-8 text-center shadow-inner mt-auto">
        <div class="container mx-auto px-4">
            <div class="text-sm">
                &copy; {{ "now"|date:"Y" }} EcoCart <span class="ml-1">🌱</span> — Built with sustainability in mind.
            </div>
        </div>
    </footer>
    {# END OF FOOTER CONTENT #}

    {# Load product.js for the Cart object and showMessageBox function #}
    <script src="{% static 'products/js/product.js' %}"></script>

    <script>
        console.log("checkout.html script started.");
        // Get the payment method passed from Django context
        const paymentMethod = "{{ payment_method }}";
        console.log("Payment Method from Django context:", paymentMethod);

        // Ensure Cart object and showMessageBox from product.js are available
        if (typeof Cart === 'undefined') {
            console.error('Cart object not found. Ensure product.js is loaded before checkout.html script.');
            window.showMessageBox = window.showMessageBox || function(msg, type) { console.log(`Message: ${msg} (${type})`); };
        } else {
            Cart.updateCartCount();
            console.log("Cart object found and navbar count updated.");
        }

        let stripe;
        let elements;
        let cardElement;

        // Initialize Stripe.js only if online payment is selected
        if (paymentMethod === 'online') {
            console.log("Initializing Stripe.js...");
            // Ensure stripe_publishable_key is available from Django context
            const stripePublishableKey = "{{ stripe_publishable_key }}";
            if (!stripePublishableKey) {
                console.error("Stripe Publishable Key is not provided in Django context.");
                showMessageBox("Payment gateway configuration error. Please try again later.", "error");
            } else {
                stripe = Stripe(stripePublishableKey);
                elements = stripe.elements();

                cardElement = elements.create('card', {
                    style: {
                        base: {
                            iconColor: '#059669',
                            color: '#374151',
                            fontWeight: '500',
                            fontFamily: 'Poppins, sans-serif',
                            fontSize: '16px',
                            '::placeholder': { color: '#9ca3af' },
                            ':-webkit-autofill': { color: '#fefcbf !important' },
                        },
                        invalid: {
                            iconColor: '#ef4444',
                            color: '#ef4444',
                        },
                    },
                });
                cardElement.mount('#card-element');
                console.log("Stripe card element mounted.");

                cardElement.on('change', function(event) {
                    const displayError = document.getElementById('card-errors');
                    if (event.error) {
                        displayError.textContent = event.error.message;
                        console.log("Stripe card error:", event.error.message);
                    } else {
                        displayError.textContent = '';
                    }
                });
            }
        }

        // --- Order Summary Calculation and Promo Code Logic ---
        let appliedPromoCode = '';
        let currentDiscountAmount = 0;
        let originalShippingCost = 50.00;

        const validPromoCodes = {
            'ECOSAVE10': { type: 'percentage', value: 0.10, message: '10% off applied!' },
            'FREESHIP': { type: 'shipping', value: 0, message: 'Free shipping applied!' },
            'SAVE20': { type: 'flat', value: 20.00, message: '₹20 flat discount applied!' }
        };

        function calculateCheckoutSummary() {
            console.log("Calculating checkout summary...");
            const cartItems = Cart.getItems();
            let subtotal = cartItems.reduce((sum, item) => sum + (item.price * item.quantity), 0);
            let shippingCost = originalShippingCost;
            let discountAmount = 0;

            if (appliedPromoCode) {
                const codeInfo = validPromoCodes[appliedPromoCode.toUpperCase()];
                if (codeInfo) {
                    if (codeInfo.type === 'percentage') {
                        discountAmount = subtotal * codeInfo.value;
                    } else if (codeInfo.type === 'flat') {
                        discountAmount = codeInfo.value;
                    } else if (codeInfo.type === 'shipping') {
                        shippingCost = 0;
                    }
                }
            }
            currentDiscountAmount = discountAmount;

            const total = (subtotal + shippingCost - discountAmount);

            document.getElementById('checkout-subtotal').textContent = subtotal.toFixed(2);
            document.getElementById('checkout-shipping').textContent = shippingCost.toFixed(2);
            document.getElementById('checkout-total').textContent = Math.max(0, total).toFixed(2);

            const discountRow = document.getElementById('checkout-discount-row');
            const checkoutDiscountSpan = document.getElementById('checkout-discount');
            const checkoutPromoCodeDisplay = document.getElementById('checkout-promo-code-display');

            if (discountAmount > 0 || (appliedPromoCode && validPromoCodes[appliedPromoCode.toUpperCase()]?.type === 'shipping')) {
                discountRow.style.display = 'flex';
                checkoutDiscountSpan.textContent = discountAmount.toFixed(2);
                checkoutPromoCodeDisplay.textContent = appliedPromoCode;
            } else {
                discountRow.style.display = 'none';
            }
            console.log(`Summary: Subtotal=${subtotal}, Shipping=${shippingCost}, Discount=${discountAmount}, Total=${total}`);
            return {
                subtotal: subtotal,
                shippingCost: shippingCost,
                discountAmount: discountAmount,
                total: Math.max(0, total),
                appliedPromoCode: appliedPromoCode,
                originalShippingCost: originalShippingCost
            };
        }

        document.getElementById('apply-promo-btn').addEventListener('click', () => {
            console.log("Apply promo button clicked.");
            const promoInput = document.getElementById('promo-code-input');
            const promoCode = promoInput.value.trim().toUpperCase();
            const promoMessage = document.getElementById('promo-message');

            if (promoCode === '') {
                promoMessage.textContent = 'Please enter a promo code.';
                promoMessage.classList.remove('text-green-600', 'text-red-600');
                promoMessage.classList.add('text-orange-500');
                appliedPromoCode = '';
                calculateCheckoutSummary();
                return;
            }

            const codeInfo = validPromoCodes[promoCode];
            if (codeInfo) {
                appliedPromoCode = promoCode;
                promoMessage.textContent = codeInfo.message;
                promoMessage.classList.remove('text-red-600', 'text-orange-500');
                promoMessage.classList.add('text-green-600');
                showMessageBox(`Coupon "${promoCode}" applied!`, 'success');
                console.log(`Coupon ${promoCode} applied successfully.`);
            } else {
                promoMessage.textContent = 'Invalid promo code. Please try again.';
                promoMessage.classList.remove('text-green-600', 'text-orange-500');
                promoMessage.classList.add('text-red-600');
                appliedPromoCode = '';
                showMessageBox('Invalid coupon code.', 'error');
                console.log(`Coupon ${promoCode} is invalid.`);
            }
            calculateCheckoutSummary();
        });

        // Function to collect all order details for sending to backend and receipt
        function collectOrderDetails(paymentMethod, orderStatus) {
            console.log("Collecting order details...");
            const summary = calculateCheckoutSummary();
            const shippingForm = document.getElementById('shipping-form');

            const orderDetails = {
                // The orderId here is client-side generated for immediate use.
                // The backend will generate the authoritative one.
                orderId: 'ECO-' + Math.random().toString(36).substring(2, 11).toUpperCase(),
                orderDate: new Date().toLocaleDateString('en-IN', { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' }),
                paymentMethod: paymentMethod,
                orderStatus: orderStatus,
                items: Cart.getItems().map(item => ({
                    id: item.id,
                    name: item.name,
                    quantity: item.quantity,
                    price: item.price,
                    total_price: item.price * item.quantity // Add total_price for convenience
                })),
                orderSummary: summary, // Pass the entire summary object
                shippingInfo: {
                    fullName: shippingForm.elements['full-name'].value,
                    customerEmail: shippingForm.elements['email'].value, // NEW: Include email
                    address1: shippingForm.elements['address-line1'].value,
                    address2: shippingForm.elements['address-line2'].value,
                    city: shippingForm.elements['city'].value,
                    state: shippingForm.elements['state'].value,
                    zipCode: shippingForm.elements['zip-code'].value,
                    country: shippingForm.elements['country'].value,
                    phoneNumber: shippingForm.elements['phone-number'].value,
                }
            };
            console.log("Collected Order Details:", orderDetails);
            return orderDetails;
        }

        // Function to get CSRF token for Django AJAX calls
        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        // Handle form submission based on payment method
        document.addEventListener('DOMContentLoaded', () => {
            console.log("DOM Content Loaded. Initializing checkout logic.");
            calculateCheckoutSummary();

            if (paymentMethod === 'online') {
                const onlineForm = document.getElementById('payment-form');
                const submitButtonOnline = document.getElementById('submit-button-online');
                const shippingForm = document.getElementById('shipping-form');

                if (onlineForm && submitButtonOnline) {
                    console.log("Online payment section detected. Attaching event listener.");
                    onlineForm.addEventListener('submit', async function(event) {
                        event.preventDefault();
                        console.log("Online payment form submitted.");

                        if (!shippingForm.checkValidity()) {
                            showMessageBox('Please fill in all required shipping information.', 'error');
                            shippingForm.reportValidity();
                            submitButtonOnline.disabled = false;
                            submitButtonOnline.innerHTML = 'Pay Now <i class="fas fa-lock ml-2"></i>';
                            console.log("Shipping form validation failed.");
                            return;
                        }

                        submitButtonOnline.disabled = true;
                        submitButtonOnline.textContent = 'Processing...';

                        // --- SIMULATED STRIPE PAYMENT (Client-side) ---
                        // In a real app, this would involve a backend call to create PaymentIntent first.
                        const { paymentMethod: stripePaymentMethod, error: stripeError } = await stripe.createPaymentMethod({
                            type: 'card',
                            card: cardElement,
                            billing_details: {
                                name: document.getElementById('card-name').value,
                                email: document.getElementById('email').value, // Pass email to Stripe
                            },
                        });

                        if (stripeError) {
                            const errorDisplay = document.getElementById('card-errors');
                            errorDisplay.textContent = stripeError.message;
                            showMessageBox(stripeError.message, 'error');
                            console.log("Stripe createPaymentMethod error:", stripeError.message);
                            submitButtonOnline.disabled = false;
                            submitButtonOnline.innerHTML = 'Pay Now <i class="fas fa-lock ml-2"></i>';
                            return; // Stop execution on Stripe error
                        }

                        console.log("Stripe Payment Method created:", stripePaymentMethod.id);

                        // Collect all order details
                        const orderDetails = collectOrderDetails(paymentMethod, 'Processing'); // Assuming 'Processing' for online
                        orderDetails.stripePaymentMethodId = stripePaymentMethod.id; // Add Stripe PaymentMethod ID

                        // Send order details to your Django backend
                        try {
                            const response = await fetch('{% url "orders:process_order" %}', { // Corrected URL
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json',
                                    'X-CSRFToken': getCookie('csrftoken'),
                                    'X-Requested-With': 'XMLHttpRequest', // <--- ADDED THIS HEADER
                                },
                                body: JSON.stringify(orderDetails)
                            });

                            const data = await response.json();
                            console.log("Backend response:", data);

                            if (data.status === 'success') {
                                showMessageBox(data.message, 'success');
                                Cart.clearCart(); // Clear the cart
                                Cart.updateCartCount(); // Update navbar cart count
                                localStorage.setItem('lastOrderDetails', JSON.stringify(data.orderDetails)); // Store for receipt page
                                // Redirect to a success page or update UI
                                window.location.href = data.redirect_url || '{% url "orders:order_success" %}?order_id=' + data.order_id; // Pass order_id
                            } else {
                                showMessageBox(data.message || 'Order failed. Please try again.', 'error');
                                submitButtonOnline.disabled = false;
                                submitButtonOnline.innerHTML = 'Pay Now <i class="fas fa-lock ml-2"></i>';
                            }
                        } catch (error) {
                            console.error("Error during order placement (fetch API):", error);
                            showMessageBox('An error occurred during payment. Please try again.', 'error');
                            submitButtonOnline.disabled = false;
                            submitButtonOnline.innerHTML = 'Pay Now <i class="fas fa-lock ml-2"></i>';
                        }
                    });
                }
            } else if (paymentMethod === 'cod') {
                const submitButtonCod = document.getElementById('submit-button-cod');
                const shippingForm = document.getElementById('shipping-form');

                if (submitButtonCod) {
                    console.log("COD payment section detected. Attaching event listener.");
                    submitButtonCod.addEventListener('click', async function() {
                        console.log("COD confirm order button clicked.");

                        if (!shippingForm.checkValidity()) {
                            showMessageBox('Please fill in all required shipping information.', 'error');
                            shippingForm.reportValidity();
                            submitButtonCod.disabled = false;
                            submitButtonCod.innerHTML = 'Confirm Order (COD) <i class="fas fa-truck-fast ml-2"></i>';
                            console.log("Shipping form validation failed for COD.");
                            return;
                        }

                        submitButtonCod.disabled = true;
                        submitButtonCod.textContent = 'Confirming...';

                        // Collect all order details for COD
                        const orderDetails = collectOrderDetails(paymentMethod, 'Pending'); // COD orders are typically 'Pending' initially

                        // Send order details to your Django backend
                        try {
                            const response = await fetch('{% url "orders:process_order" %}', { // Corrected URL
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json',
                                    'X-CSRFToken': getCookie('csrftoken'),
                                    'X-Requested-With': 'XMLHttpRequest', // <--- ADDED THIS HEADER
                                },
                                body: JSON.stringify(orderDetails)
                            });

                            const data = await response.json();
                            console.log("Backend response for COD:", data);

                            if (data.status === 'success') {
                                showMessageBox(data.message, 'success');
                                Cart.clearCart(); // Clear the cart
                                Cart.updateCartCount(); // Update navbar cart count
                                localStorage.setItem('lastOrderDetails', JSON.stringify(data.orderDetails)); // Store for receipt page
                                // Redirect to a success page or update UI
                                window.location.href = data.redirect_url || '{% url "orders:order_success" %}?order_id=' + data.order_id;
                            } else {
                                showMessageBox(data.message || 'Order failed. Please try again.', 'error');
                                submitButtonCod.disabled = false;
                                submitButtonCod.innerHTML = 'Confirm Order (COD) <i class="fas fa-truck-fast ml-2"></i>';
                            }
                        } catch (error) {
                            console.error("Error during order placement (fetch API for COD):", error);
                            showMessageBox('An error occurred during COD order. Please try again.', 'error');
                            submitButtonCod.disabled = false;
                            submitButtonCod.innerHTML = 'Confirm Order (COD) <i class="fas fa-truck-fast ml-2"></i>';
                        }
                    });
                }
            }
        });

        // Navbar toggle for mobile
        const navToggle = document.getElementById('nav-toggle');
        const navContent = document.getElementById('nav-content');

        if (navToggle && navContent) {
            navToggle.addEventListener('click', function () {
                navContent.classList.toggle('hidden');
            });
        }
    </script>

</body>
</html>
