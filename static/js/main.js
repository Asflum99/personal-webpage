document.addEventListener("DOMContentLoaded", () => {
  // Variables para el cambio de tema
  const html = document.documentElement;
  const themeToggle = document.getElementById("theme-toggle");

  // Cambiar el tema cuando se hace clic en el botón
  if (themeToggle) {
    themeToggle.addEventListener("click", () => {
      const currentTheme = html.getAttribute("data-theme");
      const newTheme = currentTheme === "dark" ? "light" : "dark";
      html.setAttribute("data-theme", newTheme);
      localStorage.setItem("theme", newTheme);
    });
  }

  // Función para habilitar el botón back-to-top
  const backToTopButton = document.getElementById("backtotop-button");

  backToTopButton.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });

  // Función para mostrar el botón back-to-top cuando el usuario haya bajado x píxeles
  window.addEventListener("scroll", () => {
    if (window.scrollY > 300) {
      backToTopButton.classList.add("show");
    } else {
      backToTopButton.classList.remove("show");
    }
  });

  // Función para ocultar el botón si se ingresa a la página desde Internet Samsung
  if (/SamsungBrowser/i.test(navigator.userAgent)) {
    if (backToTopButton) {
      backToTopButton.style.display = "none";
    }
  }
});
