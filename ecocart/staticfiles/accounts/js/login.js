// login.js
document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector(".form");
  const msg = document.querySelector(".msg");

  // Optional: auto-hide error message after 4 seconds
  if (msg) {
    setTimeout(() => {
      msg.style.display = "none";
    }, 4000);
  }

  // Smooth submit animation
  form.addEventListener("submit", () => {
    form.classList.add("submitting");
    setTimeout(() => {
      form.classList.remove("submitting");
    }, 1000);
  });
});
