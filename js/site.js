(function () {
  var root = document.documentElement;
  var toggle = document.querySelector("[data-theme-toggle]");
  var navToggle = document.querySelector("[data-nav-toggle]");
  var nav = document.querySelector("[data-nav]");

  function currentTheme() {
    return root.getAttribute("data-theme") === "dark" ? "dark" : "light";
  }

  function applyTheme(theme) {
    root.setAttribute("data-theme", theme);
    var dark = theme === "dark";
    if (toggle) {
      toggle.setAttribute("aria-pressed", dark ? "true" : "false");
      toggle.setAttribute("aria-label", dark ? "Switch to light theme" : "Switch to dark theme");
    }
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.setAttribute("content", dark ? "#10120f" : "#f3efe6");
  }

  applyTheme(currentTheme());

  if (toggle) {
    toggle.addEventListener("click", function () {
      var next = currentTheme() === "dark" ? "light" : "dark";
      try {
        localStorage.setItem("theme", next);
      } catch (err) {
        /* Storage can be blocked; the choice still applies for this view. */
      }
      applyTheme(next);
    });
  }

  if (navToggle && nav) {
    navToggle.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      navToggle.setAttribute("aria-expanded", open ? "true" : "false");
      navToggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    });
    nav.addEventListener("click", function (event) {
      if (event.target.closest("a")) {
        nav.classList.remove("is-open");
        navToggle.setAttribute("aria-expanded", "false");
        navToggle.setAttribute("aria-label", "Open menu");
      }
    });
  }

  var form = document.querySelector("#contact-form");
  if (form) {
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      var data = new FormData(form);
      var name = String(data.get("name") || "").trim();
      var email = String(data.get("email") || "").trim();
      var message = String(data.get("message") || "").trim();
      var status = document.querySelector("#form-status");
      if (!name || !email || !message) {
        if (status) status.textContent = "Add your name, email, and a message, or use the email address above.";
        return;
      }
      var body = message + "\n\nFrom: " + name + " <" + email + ">";
      var href = "mailto:harryodhiambo17@gmail.com?subject=" +
        encodeURIComponent("Portfolio note from " + name) +
        "&body=" + encodeURIComponent(body);
      if (status) status.textContent = "Opening your email app to harryodhiambo17@gmail.com.";
      window.location.href = href;
    });
  }
})();
