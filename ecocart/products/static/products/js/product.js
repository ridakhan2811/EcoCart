document.addEventListener('DOMContentLoaded', function () {
  const cartButtons = document.querySelectorAll('.add-cart-btn');
  cartButtons.forEach(button => {
    button.addEventListener('click', () => {
      button.innerText = "✔️ Added!";
      button.disabled = true;
      button.classList.add('clicked');
      setTimeout(() => {
        button.innerText = "🛒 Add to Cart";
        button.disabled = false;
        button.classList.remove('clicked');
      }, 1500);
    });
  });
});
