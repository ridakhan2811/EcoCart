document.addEventListener("DOMContentLoaded", () => {
  const toast = document.getElementById("toast");
  if (toast) {
    toast.classList.add("show");
    setTimeout(() => {
      toast.classList.remove("show");
    }, 4000);
  }

  const editBtn = document.querySelector("button[onclick='editProfile()']");
  if (editBtn) {
    editBtn.addEventListener("click", () => {
      alert("Edit functionality coming soon!");
    });
  }
});
