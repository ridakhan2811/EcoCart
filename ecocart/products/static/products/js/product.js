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

// --- Cart Manager ---
const Cart = {
    STORAGE_KEY: 'ecocart_items',

    getItems() {
        try {
            const data = localStorage.getItem(this.STORAGE_KEY);
            return data ? JSON.parse(data) : [];
        } catch (e) {
            console.error('Error reading cart from localStorage', e);
            return [];
        }
    },

    saveItems(items) {
        try {
            localStorage.setItem(this.STORAGE_KEY, JSON.stringify(items));
            this.updateCartCount();
        } catch (e) {
            console.error('Error saving cart to localStorage', e);
        }
    },

    addItem(product) {
        const items = this.getItems();
        const existingIndex = items.findIndex(item => String(item.id) === String(product.id));

        if (existingIndex > -1) {
            items[existingIndex].quantity += (product.quantity || 1);
        } else {
            items.push({
                id: String(product.id),
                name: product.name,
                price: parseFloat(product.price) || 0,
                image_url: product.image_url || (typeof PLACEHOLDER_IMG !== 'undefined' ? PLACEHOLDER_IMG : '/static/products/images/placeholder.jpg'),
                quantity: product.quantity || 1
            });
        }
        this.saveItems(items);
        showMessageBox(`"${product.name}" added to cart!`, 'success');
    },

    updateQuantity(productId, quantity) {
        let items = this.getItems();
        const index = items.findIndex(item => String(item.id) === String(productId));
        if (index > -1) {
            if (quantity <= 0) {
                items.splice(index, 1);
            } else {
                items[index].quantity = quantity;
            }
            this.saveItems(items);
        }
    },

    removeItem(productId) {
        let items = this.getItems();
        items = items.filter(item => String(item.id) !== String(productId));
        this.saveItems(items);
    },

    clearCart() {
        try {
            localStorage.removeItem(this.STORAGE_KEY);
            this.updateCartCount();
        } catch (e) {
            console.error('Error clearing cart', e);
        }
    },

    updateCartCount() {
        const items = this.getItems();
        const totalCount = items.reduce((sum, item) => sum + (parseInt(item.quantity) || 0), 0);
        const cartCountSpans = document.querySelectorAll('#cart-count');
        cartCountSpans.forEach(span => {
            span.textContent = totalCount;
        });
    }
};

window.Cart = Cart;

// Function to show a temporary message box toast
function showMessageBox(message, type = 'success') {
    const box = document.getElementById('message-box');
    if (!box) {
        console.log(`[Toast] ${type}: ${message}`);
        return;
    }
    box.textContent = message;

    box.classList.remove('bg-green-600', 'bg-red-600', 'bg-blue-600', 'bg-gray-700', 'hidden', 'opacity-0');
    if (type === 'error') {
        box.classList.add('bg-red-600');
    } else if (type === 'info') {
        box.classList.add('bg-blue-600');
    } else {
        box.classList.add('bg-green-600');
    }

    box.classList.add('show', 'opacity-100');

    setTimeout(() => {
        box.classList.remove('opacity-100', 'show');
        box.classList.add('opacity-0');
        setTimeout(() => {
            box.classList.add('hidden');
        }, 300);
    }, 3000);
}
window.showMessageBox = showMessageBox;

function showNotification(message) {
    showMessageBox(message, 'info');
}
window.showNotification = showNotification;

// Functional addToCart function
function addToCart(buttonElement) {
    const productId = buttonElement.dataset.productId;
    const productName = buttonElement.dataset.productName;
    const productPrice = buttonElement.dataset.productPrice;
    const productImage = buttonElement.dataset.productImageUrl;

    if (!productId) {
        console.error('addToCart missing productId');
        return;
    }

    Cart.addItem({
        id: productId,
        name: productName || 'Product',
        price: productPrice || 0,
        image_url: productImage || (typeof PLACEHOLDER_IMG !== 'undefined' ? PLACEHOLDER_IMG : '/static/products/images/placeholder.jpg'),
        quantity: 1
    });
}
window.addToCart = addToCart;

// Dummy toggleWishlist function
function toggleWishlist(element) {
    element.classList.toggle('active');
    const action = element.classList.contains('active') ? 'added to' : 'removed from';
    showMessageBox(`Product ${action} wishlist!`, 'info');
}
window.toggleWishlist = toggleWishlist;

// --- Product Rendering Logic ---

// Function to generate HTML string for a single product card
function createProductCardHTML(product) {
    const imageUrl = product.image_url || (typeof PLACEHOLDER_IMG !== 'undefined' ? PLACEHOLDER_IMG : '/static/products/images/placeholder.jpg');

    const originalPriceHtml = product.is_discounted ?
        `<span class="text-gray-400 line-through text-sm ml-2">₹${parseFloat(product.original_price).toFixed(2)}</span>
         <span class="ml-auto bg-red-100 text-red-600 font-bold text-xs px-2 py-0.5 rounded-full">${product.discount_percentage}% OFF</span>` : '';

    const ecoFriendlyBadge = product.is_eco_friendly ? `
        <div class="absolute top-3 right-3 bg-emerald-600/90 backdrop-blur-md text-white text-xs font-semibold px-3 py-1 rounded-full shadow-lg border border-emerald-400/30 flex items-center gap-1.5 transform group-hover:scale-105 transition-all">
            <span class="animate-bounce">🌿</span> Eco-Friendly
            ${product.eco_impact_statement ? `<span class="tooltip-text">${product.eco_impact_statement}</span>` : ''}
        </div>` : '';

    const impactBarHtml = (product.plastic_saved_kg !== null && typeof product.plastic_saved_kg === 'number' && !isNaN(product.plastic_saved_kg) && product.plastic_saved_kg > 0) ? `
        <div class="impact-bar bg-emerald-50/80 border border-emerald-200/60 rounded-full px-3 py-1.5 text-xs text-emerald-800 font-medium flex items-center gap-1.5 my-2">
            <i class="fa-solid fa-seedling text-emerald-600 animate-pulse"></i>
            <span>Saves:</span> <strong>${parseFloat(product.plastic_saved_kg).toFixed(2)}kg plastic</strong>
        </div>` : '';

    const stockInfoHtml = product.stock > 0 ?
        `<p class="text-emerald-700 text-xs font-semibold flex items-center mt-2"><i class="fas fa-check-circle mr-1 text-emerald-500"></i> In Stock (${product.stock})</p>

    // Generate HTML for star ratings
    const starsFull = '<i class="fas fa-star text-yellow-400 star-icon"></i>'.repeat(product.stars_full || 0);
    const starsHalf = product.stars_half ? '<i class="fas fa-star-half-alt text-yellow-400 star-icon"></i>' : '';
    const starsEmpty = '<i class="far fa-star text-gray-300 star-icon"></i>'.repeat(product.stars_empty || 0);

    return `
        <a href="/products/${product.id}/" class="product-card-link bg-white/90 backdrop-blur-md rounded-2xl border border-emerald-100/80 shadow-md hover:shadow-2xl hover:-translate-y-1.5 transition-all duration-300 overflow-hidden group product-item"
            data-category="${product.category_slug || 'uncategorized'}"
            data-price="${product.price}"
            data-rating="${product.rating}"
            data-name="${product.name.toLowerCase()}"
            data-eco-friendly="${product.is_eco_friendly}"
            data-product-id="${product.id}">
            <div class="product-card flex flex-col h-full">
                <div class="block relative overflow-hidden w-full h-52 bg-emerald-50/50">
                    <img src="${imageUrl}"
                         onerror="this.onerror=null; this.src='${typeof PLACEHOLDER_IMG !== 'undefined' ? PLACEHOLDER_IMG : '/static/products/images/placeholder.jpg'}';"
                         alt="${product.name}"
                         class="w-full h-full object-cover transition-transform duration-700 ease-out group-hover:scale-110">
                    ${ecoFriendlyBadge}
                    <button class="wishlist-icon absolute top-3 left-3 bg-white/80 backdrop-blur-md p-2 rounded-full shadow-md text-gray-400 hover:text-red-500 hover:scale-110 transition-all duration-200"
                       data-product-id="${product.id}">
                        <i class="far fa-heart text-lg"></i>
                    </button>
                </div>
                <div class="p-5 flex-grow flex flex-col justify-between">
                    <div>
                        <h2 class="text-xl font-bold text-gray-900 group-hover:text-emerald-700 transition-colors duration-200 truncate" title="${product.name}">
                            ${product.name}
                        </h2>
                        ${product.brand ? `<p class="text-emerald-700/70 text-xs font-semibold uppercase tracking-wider mb-1">${product.brand}</p>` : ''}
                        <p class="text-gray-600 text-xs leading-relaxed line-clamp-2 mb-2">${product.short_description || ''}</p>
                        ${impactBarHtml}
                    </div>
                    <div class="mt-3">
                        <div class="flex items-center text-xs mb-2">
                            ${starsFull}
                            ${starsHalf}
                            ${starsEmpty}
                            <span class="ml-1.5 text-gray-500">(${parseFloat(product.rating).toFixed(1)} / ${product.review_count})</span>
                        </div>
                        <div class="flex items-baseline justify-between mb-3">
                            <span class="text-2xl font-extrabold text-emerald-800">₹${parseFloat(product.price).toFixed(2)}</span>
                            ${originalPriceHtml}
                        </div>
                        <button class="add-to-cart-btn w-full bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-2.5 px-4 rounded-xl shadow-md hover:shadow-lg transition-all duration-300 flex items-center justify-center gap-2 group/btn"
                                data-product-id="${product.id}"
                                data-product-name="${product.name}"
                                data-product-price="${product.price}"
                                data-product-image-url="${imageUrl}"
                                ${product.stock === 0 ? 'disabled' : ''}>
                            <i class="fas fa-shopping-cart text-sm transition-transform group-hover/btn:scale-110"></i> Add to Cart 🌱
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