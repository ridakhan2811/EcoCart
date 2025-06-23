document.addEventListener("DOMContentLoaded", () => {
  const loginForm = document.querySelector(".form");
  const toast = document.getElementById("toast");

  if (toast && toast.classList.contains("show")) {
    setTimeout(() => {
      toast.classList.remove("show");
    }, 3000);
  }

  loginForm.addEventListener("submit", () => {
    loginForm.classList.add("submitting");
    setTimeout(() => {
      loginForm.classList.remove("submitting");
    }, 1000);
  });
});
