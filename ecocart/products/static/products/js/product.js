/* static/products/js/product.js */
document.querySelectorAll('.wishlist').forEach(icon => {
    icon.addEventListener('click', () => {
        icon.classList.toggle('active');
        icon.textContent = icon.classList.contains('active') ? '💚' : '❤️';
    });
});

