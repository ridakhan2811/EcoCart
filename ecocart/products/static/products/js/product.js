// ecocart/products/static/products/js/product.js

// Global references to DOM elements
const productGrid = document.getElementById('product-grid');
const loadMoreBtn = document.getElementById('load-more-btn');
const messageBox = document.getElementById('message-box');
const productSearchInput = document.getElementById('product-search');
const categoryButtons = document.querySelectorAll('.filter-btn');
const ecoFriendlyCheckbox = document.getElementById('eco_friendly_checkbox');
const sortByDropdown = document.getElementById('sort-by');

// Initial state for filters and pagination (defaults, will be overwritten by INITIAL_FILTERS from Django)
let currentPage = 1;
let currentFilters = {
    category: 'all',
    search: '',
    eco_friendly: false,
    sort_by: 'default',
};

// Placeholder for image path from Django context (set in product_list.html)
let PLACEHOLDER_IMG = '/static/products/images/placeholder.jpg'; // Fallback if not set by Django

let debounceTimer; // For search input debounce

// --- Utility Functions ---

// Debounce function to limit how often a function runs
function debounce(func, delay) {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(func, delay);
}

// Function to show a temporary notification (e.g., "Product added to cart!")
function showNotification(message) {
    messageBox.textContent = message;
    messageBox.classList.remove('hidden', 'opacity-0');
    messageBox.classList.add('opacity-100');
    setTimeout(() => {
        messageBox.classList.remove('opacity-100');
        messageBox.classList.add('opacity-0');
        setTimeout(() => {
            messageBox.classList.add('hidden');
        }, 300); // Wait for fade-out transition
    }, 3000); // Show for 3 seconds
}

// Placeholder for updating cart count (client-side for now)
function updateCartCount(newCount) {
    const cartCountSpan = document.getElementById('cart-count');
    if (cartCountSpan) {
        // In a real application, you'd likely fetch this from a cart API or local storage
        let currentCount = parseInt(cartCountSpan.textContent) || 0;
        if (newCount !== undefined) {
             cartCountSpan.textContent = newCount;
        } else {
             cartCountSpan.textContent = currentCount + 1; // Increment by 1
        }
    }
}

// Dummy addToCart function
function addToCart(buttonElement) {
    const productId = buttonElement.dataset.productId;
    const productName = buttonElement.dataset.productName;
    const productPrice = buttonElement.dataset.productPrice;
    const productImage = buttonElement.dataset.productImageUrl;

    // In a real application, you'd send an AJAX request to your cart API to add the item
    console.log(`Adding product "${productName}" (ID: ${productId}) to cart. Price: ${productPrice}`);
    showNotification(`${productName} added to cart!`);
    updateCartCount(); // Update client-side count
}

// Dummy toggleWishlist function
function toggleWishlist(element) {
    element.classList.toggle('active'); // Toggles the red heart
    const action = element.classList.contains('active') ? 'added to' : 'removed from';
    console.log(`Product ID: ${element.dataset.productId} ${action} wishlist.`);
    showNotification(`Product ${action} wishlist!`);
}

// --- Product Rendering Logic ---

// Function to generate HTML string for a single product card
function createProductCardHTML(product) {
    // Determine image URL with fallback
    const imageUrl = product.image_url || PLACEHOLDER_IMG;

    // Generate HTML for original price and discount if applicable
    const originalPriceHtml = product.is_discounted ?
        `<span class="text-gray-400 line-through text-lg ml-2">₹${parseFloat(product.original_price).toFixed(2)}</span>
         <span class="ml-auto text-red-500 font-semibold text-sm">${product.discount_percentage}% OFF</span>` : '';

    // Generate HTML for eco-friendly badge with tooltip if applicable
    const ecoFriendlyBadge = product.is_eco_friendly ? `
        <div class="absolute top-2 right-2 bg-emerald-600 text-white text-xs font-semibold px-3 py-1 rounded-full shadow-md tooltip-container">
            Eco-Friendly 🌿
            ${product.eco_impact_statement ? `<span class="tooltip-text">${product.eco_impact_statement}</span>` : ''}
        </div>` : '';

    // Generate HTML for plastic impact bar if applicable
    const impactBarHtml = (product.plastic_saved_kg !== null && typeof product.plastic_saved_kg === 'number' && !isNaN(product.plastic_saved_kg) && product.plastic_saved_kg > 0) ? `
        <div class="impact-bar">
            <i class="fa-solid fa-seedling text-emerald-600"></i>
            <span>Impact:</span> By buying this, you help save ${parseFloat(product.plastic_saved_kg).toFixed(2)}kg of plastic!
        </div>` : '';

    // Generate HTML for stock info
    const stockInfoHtml = product.stock > 0 ?
        `<p class="text-emerald-600 text-sm mt-3">In Stock: ${product.stock}</p>
         ${product.stock < 10 ? `<p class="text-orange-500 text-xs mt-1">Only ${product.stock} left!</p>` : ''}` :
        `<p class="text-red-600 text-sm mt-3">Out of Stock</p>`;

    // Generate HTML for star ratings
    const starsFull = '<i class="fas fa-star text-yellow-400 star-icon"></i>'.repeat(product.stars_full || 0);
    const starsHalf = product.stars_half ? '<i class="fas fa-star-half-alt text-yellow-400 star-icon"></i>' : '';
    const starsEmpty = '<i class="far fa-star text-gray-300 star-icon"></i>'.repeat(product.stars_empty || 0);

    return `
        <a href="/products/${product.id}/" class="product-card-link bg-white rounded-xl shadow-lg transform transition-all duration-500 ease-in-out hover:scale-105 hover:shadow-2xl overflow-hidden product-item"
            data-category="${product.category_slug || 'uncategorized'}"
            data-price="${product.price}"
            data-rating="${product.rating}"
            data-name="${product.name.toLowerCase()}"
            data-eco-friendly="${product.is_eco_friendly}"
            data-product-id="${product.id}">
            <div class="product-card">
                <div class="block relative overflow-hidden w-full h-48 bg-gray-100 rounded-t-xl">
                    <img src="${imageUrl}"
                         onerror="this.onerror=null; this.src='${PLACEHOLDER_IMG}';"
                         alt="${product.name}"
                         class="w-full h-full object-cover transition-transform duration-500 hover:scale-110">
                    ${ecoFriendlyBadge}
                    <i class="far fa-heart absolute top-2 left-2 text-2xl text-gray-300 hover:text-red-400 transition-colors duration-200 cursor-pointer wishlist-icon"
                       data-product-id="${product.id}"></i>
                </div>
                <div class="p-6 flex-grow flex flex-col justify-between">
                    <div>
                        <h2 class="text-2xl font-semibold text-gray-900 mb-1 truncate" title="${product.name}">
                            ${product.name}
                        </h2>
                        ${product.brand ? `<p class="text-gray-500 text-sm mb-2">${product.brand}</p>` : ''}
                        <p class="text-gray-600 text-sm mb-4 line-clamp-3">${product.short_description || ''}</p>
                        ${impactBarHtml}
                    </div>
                    <div class="mt-4">
                        <div class="flex items-center mb-2">
                            ${starsFull}
                            ${starsHalf}
                            ${starsEmpty}
                            <span class="ml-2 text-gray-600 text-sm">(${parseFloat(product.rating).toFixed(1)} / ${product.review_count} reviews)</span>
                        </div>
                        <div class="flex items-baseline justify-between mb-4">
                            <span class="text-3xl font-bold text-emerald-700">₹${parseFloat(product.price).toFixed(2)}</span>
                            ${originalPriceHtml}
                        </div>
                        <button class="add-to-cart-btn w-full bg-emerald-600 text-white font-bold py-3 rounded-full shadow-lg hover:bg-emerald-700 transition-all duration-300 ease-in-out transform hover:scale-105 active:scale-95"
                                data-product-id="${product.id}"
                                data-product-name="${product.name}"
                                data-product-price="${product.price}"
                                data-product-image-url="${imageUrl}"
                                ${product.stock === 0 ? 'disabled' : ''}>
                            Add to Cart
                        </button>
                        ${stockInfoHtml}
                    </div>
                </div>
            </div>
        </a>
    `;
}

// Function to render products onto the grid
function renderProducts(products, append = false) {
    if (!append) {
        productGrid.innerHTML = ''; // Clear existing products if not appending (new filter/search)
    }

    if (products.length === 0 && !append) {
        // Show message if no products match criteria and it's not an append call
        productGrid.innerHTML = `
            <div class="col-span-full text-center py-10">
                <p class="text-xl text-gray-600">No products found matching your criteria. Try adjusting filters!</p>
            </div>
        `;
        // Hide load more button if no products are found
        if (loadMoreBtn) loadMoreBtn.classList.add('hidden', 'opacity-0');
        return;
    }

    products.forEach((product, index) => {
        const productCardHtml = createProductCardHTML(product);
        productGrid.insertAdjacentHTML('beforeend', productCardHtml);
        // Apply animation delay to newly inserted cards
        const insertedCard = productGrid.lastElementChild.querySelector('.product-card');
        if (insertedCard) {
            // Calculate delay based on its position in the grid
            const currentTotalCards = productGrid.querySelectorAll('.product-card').length;
            insertedCard.style.animationDelay = `${(currentTotalCards - products.length + index) * 0.08}s`;
            insertedCard.style.opacity = '1'; // Make it visible after delay
        }
    });

    // Reattach event listeners to newly added buttons (important for dynamically added content)
    productGrid.querySelectorAll('.add-to-cart-btn').forEach(btn => {
        // Prevent default link behavior and event bubbling for the button inside the <a> tag
        btn.onclick = (e) => { e.preventDefault(); e.stopPropagation(); addToCart(btn); };
    });
    productGrid.querySelectorAll('.wishlist-icon').forEach(icon => {
        // Prevent default link behavior and event bubbling for the <a> tag
        icon.onclick = (e) => { e.preventDefault(); e.stopPropagation(); toggleWishlist(icon); };
    });
}

// --- Main Data Fetching Logic ---

// Fetches products from the API based on current filters and page
async function fetchProducts(resetPage = false) {
    if (resetPage) {
        currentPage = 1; // Reset to first page for new filter/sort/search
        if (loadMoreBtn) loadMoreBtn.classList.add('opacity-0', 'hidden'); // Temporarily hide while loading
        productGrid.innerHTML = `
            <div class="col-span-full text-center py-10">
                <p class="text-xl text-gray-600">Loading products...</p>
            </div>
        `; // Show loading message
    }

    // Construct URL parameters from currentFilters and currentPage
    const params = new URLSearchParams();
    params.append('page', currentPage);
    if (currentFilters.category && currentFilters.category !== 'all') {
        params.append('category', currentFilters.category);
    }
    if (currentFilters.search) {
        params.append('search', currentFilters.search);
    }
    if (currentFilters.eco_friendly) {
        params.append('eco_friendly', 'true');
    }
    if (currentFilters.sort_by && currentFilters.sort_by !== 'default') {
        params.append('sort_by', currentFilters.sort_by);
    }

    try {
        const response = await fetch(`/products/api/products/?${params.toString()}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();

        renderProducts(data.products, !resetPage); // Pass resetPage inverse to control appending vs. clearing

        // Update load more button visibility and next page number
        if (loadMoreBtn) {
            if (data.has_next) {
                loadMoreBtn.dataset.nextPage = data.next_page_number;
                loadMoreBtn.classList.remove('hidden', 'opacity-0');
                loadMoreBtn.classList.add('opacity-100');
            } else {
                loadMoreBtn.classList.add('hidden', 'opacity-0'); // Hide if no more pages
            }
        }
        // Update currentPage for the next 'Load More' click
        currentPage = data.next_page_number || currentPage;

    } catch (error) {
        console.error('Error fetching products:', error);
        productGrid.innerHTML = `
            <div class="col-span-full text-center py-10 text-red-600">
                <p>Failed to load products. Please try again later.</p>
            </div>
        `;
        if (loadMoreBtn) loadMoreBtn.classList.add('hidden'); // Hide button on error
    }
}

// --- Event Listeners for Filters and Load More ---

// Define a function to setup event listeners
function setupEventListeners() {
    // Event listener for Category Filters
    categoryButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Update active class visually
            categoryButtons.forEach(btn => {
                btn.classList.remove('bg-emerald-600', 'text-white');
                btn.classList.add('bg-emerald-100', 'text-emerald-800', 'hover:bg-emerald-200');
            });
            button.classList.remove('bg-emerald-100', 'text-emerald-800', 'hover:bg-emerald-200');
            button.classList.add('bg-emerald-600', 'text-white');

            currentFilters.category = button.dataset.filter;
            fetchProducts(true); // Reset page and fetch new products
        });
    });

    // Event listener for Search Input (with debounce)
    if (productSearchInput) {
        productSearchInput.addEventListener('keyup', () => {
            debounce(() => {
                currentFilters.search = productSearchInput.value.trim();
                fetchProducts(true); // Reset page and fetch new products
            }, 500); // 500ms debounce delay
        });
    }

    // Event listener for Eco-Friendly Checkbox
    if (ecoFriendlyCheckbox) {
        ecoFriendlyCheckbox.addEventListener('change', () => {
            currentFilters.eco_friendly = ecoFriendlyCheckbox.checked;
            fetchProducts(true); // Reset page and fetch new products
        });
    }

    // Event listener for Sort Dropdown
    if (sortByDropdown) {
        sortByDropdown.addEventListener('change', () => {
            currentFilters.sort_by = sortByDropdown.value;
            fetchProducts(true); // Reset page and fetch new products
        });
    }

    // Event listener for Load More Button
    if (loadMoreBtn) {
        loadMoreBtn.addEventListener('click', () => {
            fetchProducts(false); // Do not reset page, append results
        });
    }
}


document.addEventListener('DOMContentLoaded', () => {
    // Initialize global PLACEHOLDER_IMG if set by Django template
    if (typeof PLACEHOLDER_IMG_URL !== 'undefined') {
        PLACEHOLDER_IMG = PLACEHOLDER_IMG_URL;
    }

    // Initialize currentFilters with values passed from Django context
    if (typeof INITIAL_FILTERS !== 'undefined') {
        currentFilters.category = INITIAL_FILTERS.category;
        currentFilters.search = INITIAL_FILTERS.search;
        currentFilters.eco_friendly = INITIAL_FILTERS.eco_friendly === 'true'; // Ensure boolean
        currentFilters.sort_by = INITIAL_FILTERS.sort_by;
    }

    // Set active class for initial category button
    categoryButtons.forEach(button => {
        if (button.dataset.filter === currentFilters.category) {
            button.classList.remove('bg-emerald-100', 'text-emerald-800', 'hover:bg-emerald-200');
            button.classList.add('bg-emerald-600', 'text-white');
        } else {
             button.classList.remove('bg-emerald-600', 'text-white');
             button.classList.add('bg-emerald-100', 'text-emerald-800', 'hover:bg-emerald-200');
        }
    });

    // Set initial value for search input
    if (productSearchInput) {
        productSearchInput.value = currentFilters.search;
    }

    // Set initial state for eco-friendly checkbox
    if (ecoFriendlyCheckbox) {
        ecoFriendlyCheckbox.checked = currentFilters.eco_friendly;
    }

    // Set initial value for sort dropdown
    if (sortByDropdown) {
        sortByDropdown.value = currentFilters.sort_by;
    }


    // Call the function to setup all event listeners
    setupEventListeners();

    // Initial load of products when the page is ready
    fetchProducts(true); // Load the first page of products based on initial filters
    updateCartCount(0); // Initialize cart count, or fetch from persistent storage if implemented
});