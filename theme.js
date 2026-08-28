(function () {
  var storageKey = "sb-theme-v2";
  var root = document.documentElement;

  function getStoredTheme() {
    try {
      return localStorage.getItem(storageKey) === "dark" ? "dark" : "light";
    } catch (error) {
      return root.dataset.theme === "dark" ? "dark" : "light";
    }
  }

  function storeTheme(theme) {
    try {
      localStorage.setItem(storageKey, theme);
    } catch (error) {
      return;
    }
  }

  function applyTheme(theme) {
    var nextTheme = theme === "light" ? "dark" : "light";
    root.dataset.theme = theme;
    storeTheme(theme);

    document.querySelectorAll("[data-theme-toggle]").forEach(function (button) {
      var label = button.querySelector("[data-theme-label]");
      button.setAttribute("aria-pressed", String(theme === "light"));
      button.setAttribute("aria-label", nextTheme === "light" ? "Switch to light theme" : "Switch to dark theme");
      if (label) {
        label.textContent = nextTheme === "light" ? "Light" : "Dark";
      }
    });
  }

  applyTheme(getStoredTheme());

  document.addEventListener("click", function (event) {
    var button = event.target.closest("[data-theme-toggle]");
    if (!button) return;
    applyTheme(root.dataset.theme === "light" ? "dark" : "light");
  });
})();
