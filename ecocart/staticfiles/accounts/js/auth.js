document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector(".form");
  const toast = document.getElementById("toast");

  if (toast && toast.classList.contains("show")) {
    setTimeout(() => {
      toast.classList.remove("show");
    }, 3000);
  }

  // Smooth input focus animation
  const inputs = form.querySelectorAll("input, select");
  inputs.forEach(input => {
    input.addEventListener("focus", () => {
      input.style.borderColor = "#66bb6a";
    });
    input.addEventListener("blur", () => {
      input.style.borderColor = "#c8e6c9";
    });
  });
});
