// products/static/products/js/product.js

// Cart object to manage items in local storage
const Cart = {
    // Retrieves all items currently in the cart from local storage.
    // If no cart exists, it returns an empty array.
    getItems: function() {
        const cart = localStorage.getItem('ecocart_cart');
        return cart ? JSON.parse(cart) : [];
    },

    // Saves the current array of cart items to local storage.
    // Includes a console log for debugging purposes.
    saveItems: function(items) {
        localStorage.setItem('ecocart_cart', JSON.stringify(items));
        console.log('Cart saved to localStorage:', items); // Debugging: Confirm cart save
    },

    // Add a product to the cart or increment its quantity if it already exists.
    // Takes a product object as an argument, which must contain id, name, price, and image_url.
    addItem: function(product) {
        console.log('Attempting to add item to cart:', product); // Debugging: Item received by addItem
        let items = this.getItems(); // Get current cart items
        const existingItemIndex = items.findIndex(item => item.id === product.id); // Check if product already in cart

        if (existingItemIndex > -1) {
            // If item exists, increment its quantity
            items[existingItemIndex].quantity += 1;
            console.log('Item already in cart, incrementing quantity:', items[existingItemIndex]); // Debugging
        } else {
            // If item does not exist, add it as a new item with quantity 1
            items.push({
                id: product.id,
                name: product.name,
                price: product.price,
                image_url: product.image_url,
                quantity: 1
            });
            console.log('New item added to cart:', product); // Debugging
        }
        this.saveItems(items); // Save updated cart to local storage
        this.updateCartCount(); // Update the cart count displayed in the navbar
    },

    // Remove an item from the cart based on its product ID.
    removeItem: function(productId) {
        let items = this.getItems();
        items = items.filter(item => item.id !== productId); // Filter out the item to be removed
        this.saveItems(items); // Save updated cart
        this.updateCartCount(); // Update cart count
        console.log('Item removed from cart:', productId); // Debugging
    },

    // Update the quantity of a specific item in the cart.
    // If the new quantity is 0 or less, the item is removed from the cart.
    updateQuantity: function(productId, newQuantity) {
        let items = this.getItems();
        const itemIndex = items.findIndex(item => item.id === productId);

        if (itemIndex > -1) {
            items[itemIndex].quantity = newQuantity;
            if (items[itemIndex].quantity <= 0) {
                // Remove item if quantity drops to 0 or less
                items.splice(itemIndex, 1);
                console.log('Item quantity updated to 0 or less, removing item:', productId); // Debugging
            }
            this.saveItems(items); // Save updated cart
            this.updateCartCount(); // Update cart count
            console.log(`Quantity updated for ${productId} to ${newQuantity}`); // Debugging
        }
    },

    // Calculates and returns the total number of items (sum of quantities) in the cart.
    getTotalItemsCount: function() {
        return this.getItems().reduce((total, item) => total + item.quantity, 0);
    },

    // Update the text content of the cart count element in the navbar.
    // Assumes an element with id 'cart-count' exists in the DOM.
    updateCartCount: function() {
        const cartCountElement = document.getElementById('cart-count');
        if (cartCountElement) {
            cartCountElement.textContent = this.getTotalItemsCount();
            console.log('Cart count updated to:', this.getTotalItemsCount()); // Debugging
        } else {
            console.warn('Cart count element #cart-count not found in the DOM.'); // Debugging: Warn if element is missing
        }
    },

    // Clears all items from the cart in local storage.
    clearCart: function() {
        localStorage.removeItem('ecocart_cart');
        this.updateCartCount(); // Reset cart count to 0
        console.log('Cart cleared.'); // Debugging
    }
};

// Function to display a temporary message box on the screen.
// It slides in, displays the message, and then fades out.
// 'type' can be 'success', 'error', or 'info' to apply different styling.
function showMessageBox(message, type = 'success') {
    const messageBox = document.getElementById('message-box');
    if (messageBox) {
        // Remove existing type classes and reset visibility
        messageBox.classList.remove('success', 'error', 'info', 'hidden', 'opacity-0');
        messageBox.classList.add('show', 'opacity-100'); // Show and make opaque

        messageBox.textContent = message; // Set the message text

        // Add type-specific class
        if (type === 'success') messageBox.classList.add('bg-green-600');
        else if (type === 'error') messageBox.classList.add('bg-red-600');
        else if (type === 'info') messageBox.classList.add('bg-blue-600');
        else messageBox.classList.add('bg-gray-700'); // Default if no valid type

        // Set a timeout to hide the message box
        setTimeout(() => {
            messageBox.classList.remove('opacity-100'); // Start fade out
            messageBox.classList.add('opacity-0');
            setTimeout(() => {
                messageBox.classList.add('hidden'); // Fully hide after transition
                // Remove type-specific classes to clean up for next message
                messageBox.classList.remove('bg-green-600', 'bg-red-600', 'bg-blue-600', 'bg-gray-700');
            }, 400); // Matches CSS transition duration for opacity
        }, 5000); // Message visible for 5 seconds
    } else {
        console.warn('Message box element #message-box not found in the DOM. Message:', message); // Debugging: Warn if element is missing
    }
}


// Global function to handle adding a product to the cart from a button click.
// It extracts product data from the button's data attributes.
function addToCart(element) {
    console.log('addToCart function called with element:', element); // Debugging: Confirm function call

    // Extract product data from data attributes of the clicked element
    const productId = element.dataset.productId;
    const productName = element.dataset.productName;
    const productPrice = parseFloat(element.dataset.productPrice); // Convert price to a number
    const productImageUrl = element.dataset.productImageUrl;

    console.log('Extracted product data:', {
        productId,
        productName,
        productPrice,
        productImageUrl
    }); // Debugging: Show extracted data

    // Validate extracted data
    if (!productId || !productName || isNaN(productPrice) || !productImageUrl) {
        console.error('Missing or invalid product data for Add to Cart:', {
            productId,
            productName,
            productPrice,
            productImageUrl
        });
        showMessageBox('Error: Could not add product to cart. Missing data.', 'error');
        return; // Stop execution if data is invalid
    }

    // Create a product object to pass to the Cart.addItem method
    const productToAdd = {
        id: productId,
        name: productName,
        price: productPrice,
        image_url: productImageUrl
    };

    Cart.addItem(productToAdd); // Add the product to the cart
    console.log(`Successfully called Cart.addItem for "${productName}" (ID: ${productId}).`);
    showMessageBox(`${productName} added to cart!`); // Show success notification
}

// Global function to toggle wishlist status of a product.
// It toggles the 'active' class on the heart icon.
function toggleWishlist(iconElement) {
    iconElement.classList.toggle('active');
    console.log('Wishlist toggled for product ID:', iconElement.dataset.productId);
    // In a real application, you would send an AJAX request here to update the user's wishlist on the server.
    showMessageBox('Wishlist status updated!', 'info');
}


// Debounce function for search input to prevent excessive API calls.
let debounceTimer;
function debounceFilter() {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
        filterProducts(); // Call filterProducts after a delay
    }, 300); // 300ms delay
}

// Function to filter products based on category, search query, eco-friendly status, and sort order.
// It makes an API call to fetch filtered products and updates the product grid.
function filterProducts(page = 1) { // Added page parameter for pagination
    const currentCategory = document.querySelector('.filter-btn.bg-emerald-600')?.dataset.filter || 'all';
    const searchInput = document.getElementById('product-search');
    const searchQuery = searchInput ? searchInput.value : '';
    const ecoFriendlyCheckbox = document.getElementById('eco_friendly_checkbox');
    const ecoFriendlyChecked = ecoFriendlyCheckbox ? ecoFriendlyCheckbox.checked : false;
    const sortBy = document.getElementById('sort-by')?.value || 'default';

    const params = new URLSearchParams();
    params.append('page', page); // Always append page for API call
    if (currentCategory !== 'all') params.append('category', currentCategory);
    if (searchQuery) params.append('search', searchQuery);
    if (ecoFriendlyChecked) params.append('eco_friendly', 'true');
    if (sortBy !== 'default') params.append('sort_by', sortBy);

    // Update URL without reloading page for better user experience, only if not loading more
    if (page === 1) {
        history.pushState(null, '', `?${params.toString()}`);
    }

    fetch(`/products/api/list/?${params.toString()}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            const productGrid = document.getElementById('product-grid');
            if (productGrid) {
                if (page === 1) { // Clear grid only for the first page of results
                    productGrid.innerHTML = '';
                }

                if (data.products.length === 0 && page === 1) { // Only show "no products" if no products on first load
                    productGrid.innerHTML = `
                        <div class="col-span-full text-center py-10">
                            <p class="text-xl text-gray-600">No products found matching your criteria. Try adjusting filters!</p>
                        </div>
                    `;
                } else {
                    data.products.forEach((product, index) => {
                        // Dynamically create product card HTML
                        const productCardHtml = `
                            <a href="/products/${product.id}/" class="product-card-link bg-white rounded-xl shadow-lg transform transition-all duration-500 ease-in-out hover:scale-105 hover:shadow-2xl overflow-hidden product-item"
                               data-category="${product.category_slug}"
                               data-price="${product.price}"
                               data-rating="${product.rating}"
                               data-name="${product.name.toLowerCase()}"
                               data-eco-friendly="${product.is_eco_friendly}"
                               data-product-id="${product.id}">
                                <div class="product-card" style="animation-delay: ${index * 0.08}s;">
                                    <div class="block relative overflow-hidden w-full h-48 bg-gray-100 rounded-t-xl">
                                        <img src="${product.image_url}"
                                             onerror="this.onerror=null; this.src='https://placehold.co/400x300/e0ffe0/333333?text=EcoProduct';"
                                             alt="${product.name}"
                                             class="w-full h-full object-cover transition-transform duration-500 hover:scale-110">
                                        ${product.is_eco_friendly ? `
                                            <div class="absolute top-2 right-2 bg-emerald-600 text-white text-xs font-semibold px-3 py-1 rounded-full shadow-md tooltip-container">
                                                Eco-Friendly 🌿
                                                ${product.eco_impact_statement ? `<span class="tooltip-text">${product.eco_impact_statement}</span>` : ''}
                                            </div>
                                        ` : ''}
                                        <i class="far fa-heart absolute top-2 left-2 text-2xl text-gray-300 hover:text-red-400 transition-colors duration-200 cursor-pointer wishlist-icon" data-product-id="${product.id}" onclick="event.preventDefault(); event.stopPropagation(); toggleWishlist(this);"></i>
                                    </div>
                                    <div class="p-6 flex-grow flex flex-col justify-between">
                                        <div>
                                            <h2 class="text-2xl font-semibold text-gray-900 mb-1 truncate" title="${product.name}">
                                                ${product.name}
                                            </h2>
                                            ${product.brand ? `<p class="text-gray-500 text-sm mb-2">${product.brand}</p>` : ''}
                                            <p class="text-gray-600 text-sm mb-4 line-clamp-3">${product.short_description}</p>

                                            ${product.plastic_saved_kg ? `
                                            <div class="impact-bar">
                                                <i class="fa-solid fa-seedling text-emerald-600"></i>
                                                <span>Impact:</span> By buying this, you help save ${product.plastic_saved_kg}kg of plastic!
                                            </div>
                                            ` : ''}
                                        </div>
                                        <div class="mt-4">
                                            <div class="flex items-center mb-2">
                                                ${'<i class="fas fa-star text-yellow-400 star-icon"></i>'.repeat(product.stars_full)}
                                                ${product.stars_half ? '<i class="fas fa-star-half-alt text-yellow-400 star-icon"></i>' : ''}
                                                ${'<i class="far fa-star text-gray-300 star-icon"></i>'.repeat(product.stars_empty)}
                                                <span class="ml-2 text-gray-600 text-sm">(${product.rating.toFixed(1)} / ${product.review_count} reviews)</span>
                                            </div>

                                            <div class="flex items-baseline justify-between mb-4">
                                               <span class="text-3xl font-bold text-emerald-700">₹${product.price.toFixed(2)}</span>
                                                ${product.is_discounted ? `
                                                   <span class="text-gray-400 line-through text-lg ml-2">₹${product.original_price.toFixed(2)}</span>
                                                    <span class="ml-auto text-red-500 font-semibold text-sm">${product.discount_percentage}% OFF</span>
                                                ` : ''}
                                            </div>
                                            <button class="add-to-cart-btn w-full bg-emerald-600 text-white font-bold py-3 rounded-full shadow-lg hover:bg-emerald-700 transition-all duration-300 ease-in-out transform hover:scale-105 active:scale-95"
                                                    data-product-id="${product.id}" data-product-name="${product.name}" data-product-price="${product.price}" data-product-image-url="${product.image_url}" onclick="event.preventDefault(); event.stopPropagation(); addToCart(this);"
                                                    ${product.stock === 0 ? 'disabled' : ''}>
                                                Add to Cart
                                            </button>

                                            ${product.stock > 0 ? `
                                                <p class="text-emerald-600 text-sm mt-3">In Stock: ${product.stock}</p>
                                                ${product.stock < 10 ? `<p class="text-orange-500 text-xs mt-1">Only ${product.stock} left!</p>` : ''}
                                            ` : `
                                                    <p class="text-red-600 text-sm mt-3">Out of Stock</p>
                                            `}
                                        </div>
                                    </div>
                                </div>
                            </a>
                        `;
                        productGrid.insertAdjacentHTML('beforeend', productCardHtml);
                    });

                    // IMPORTANT: Re-attach event listeners for newly added elements
                    // This is crucial because innerHTML replaces content, removing old listeners.
                    document.querySelectorAll('.wishlist-icon').forEach(icon => {
                        // Remove existing listener to prevent duplicates if filterProducts is called multiple times
                        icon.removeEventListener('click', (event) => { /* empty */ });
                        icon.addEventListener('click', (event) => {
                            event.preventDefault();
                            event.stopPropagation(); // Stop propagation to prevent parent link click
                            toggleWishlist(icon);
                        });
                    });
                    document.querySelectorAll('.add-to-cart-btn').forEach(btn => {
                        // Remove existing listener to prevent duplicates
                        btn.removeEventListener('click', (event) => { /* empty */ });
                        btn.addEventListener('click', (event) => {
                            event.preventDefault();
                            event.stopPropagation(); // Stop propagation to prevent parent link click
                            addToCart(btn); // Call the global addToCart function
                        });
                    });
                }

                // Update Load More button visibility and data attributes
                const loadMoreBtn = document.getElementById('load-more-btn');
                if (loadMoreBtn) {
                    if (data.has_next) {
                        loadMoreBtn.classList.remove('hidden');
                        loadMoreBtn.dataset.nextPage = data.next_page_number;
                        loadMoreBtn.dataset.currentCategory = currentCategory;
                        loadMoreBtn.dataset.currentSearch = searchQuery;
                        loadMoreBtn.dataset.ecoFriendlyChecked = ecoFriendlyChecked;
                        loadMoreBtn.dataset.currentSortBy = sortBy;
                    } else {
                        loadMoreBtn.classList.add('hidden');
                    }
                }
            }
        })
        .catch(error => {
            console.error('Error fetching products:', error);
            const productGrid = document.getElementById('product-grid');
            if (productGrid) {
                productGrid.innerHTML = `
                    <div class="col-span-full text-center py-10">
                        <p class="text-xl text-red-500">Failed to load products. Please try again later.</p>
                    </div>
                `;
            }
            showMessageBox('Failed to load products. Please try again.', 'error');
        });
}

// Carousel logic for related products on product detail page.
function scrollCarousel(direction) {
    const track = document.getElementById('related-products-track');
    if (!track) return;

    const itemWidth = track.firstElementChild ? track.firstElementChild.offsetWidth : 0;
    const scrollAmount = itemWidth * 1; // Scroll by one item at a time

    track.scrollBy({
        left: direction * scrollAmount,
        behavior: 'smooth'
    });
}


// Event Listeners for DOMContentLoaded to ensure elements are available
document.addEventListener('DOMContentLoaded', () => {
    // Initialize cart count on page load for the navbar icon
    Cart.updateCartCount();

    // Mobile Navigation Toggle
    const navToggle = document.getElementById('nav-toggle');
    const navContent = document.getElementById('nav-content');
    if (navToggle && navContent) {
        navToggle.addEventListener('click', function() {
            navContent.classList.toggle('hidden');
        });
    }

    // Apply staggered animation delay to product cards on initial load
    const productCards = document.querySelectorAll('.product-card');
    productCards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.08}s`;
    });

    // Attach event listeners for filter buttons
    document.querySelectorAll('.filter-btn').forEach(button => {
        button.addEventListener('click', function() {
            // Remove active class from all filter buttons
            document.querySelectorAll('.filter-btn').forEach(btn => {
                btn.classList.remove('bg-emerald-600', 'text-white');
                btn.classList.add('bg-emerald-100', 'text-emerald-800', 'hover:bg-emerald-200');
            });
            // Add active class to the clicked button
            this.classList.remove('bg-emerald-100', 'text-emerald-800', 'hover:bg-emerald-200');
            this.classList.add('bg-emerald-600', 'text-white');
            filterProducts(); // Re-filter products when category changes (resets to page 1)
        });
    });

    // Attach event listener for search input
    const searchInput = document.getElementById('product-search');
    if (searchInput) {
        searchInput.addEventListener('keyup', debounceFilter);
    }

    // Attach event listener for eco-friendly checkbox
    const ecoFriendlyCheckbox = document.getElementById('eco_friendly_checkbox');
    if (ecoFriendlyCheckbox) {
        ecoFriendlyCheckbox.addEventListener('change', filterProducts);
    }

    // Attach event listener for sort-by dropdown
    const sortByDropdown = document.getElementById('sort-by');
    if (sortByDropdown) {
        sortByDropdown.addEventListener('change', filterProducts);
    }


    // Attach event listener for Load More button
    const loadMoreBtn = document.getElementById('load-more-btn');
    if (loadMoreBtn) {
        loadMoreBtn.addEventListener('click', function() {
            const nextPage = parseInt(this.dataset.nextPage);
            filterProducts(nextPage); // Load next page of products
        });
    }

    // Attach event listeners for Add to Cart buttons that are present on initial page load
    // This handles cases where product_list.html or product_detail.html has static buttons
    document.querySelectorAll('.add-to-cart-btn').forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault(); // Prevent default link/form behavior
            event.stopPropagation(); // Stop event from bubbling up to parent elements (like product card link)
            addToCart(button); // Call the main addToCart function
        });
    });

    // Attach event listeners for Wishlist icons that are present on initial page load
    document.querySelectorAll('.wishlist-icon').forEach(icon => {
        icon.addEventListener('click', (event) => {
            event.preventDefault(); // Prevent default link behavior
            event.stopPropagation(); // Stop event from bubbling up to parent elements (like product card link)
            toggleWishlist(icon); // Call the main toggleWishlist function
        });
    });
});
