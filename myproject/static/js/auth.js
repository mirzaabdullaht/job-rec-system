document.addEventListener("DOMContentLoaded", () => {
  // Helper: get CSRF token
  function getCsrfToken() {
    let csrfToken = document.querySelector("[name=csrfmiddlewaretoken]");
    return csrfToken ? csrfToken.value : "";
  }

  // Handle Login
  const loginForm = document.getElementById("loginForm");
  if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
      e.preventDefault();

      const url = "/accounts/login/";
      const payload = {
        email: document.getElementById("email").value,
        password: document.getElementById("password").value,
      };

      try {
        const response = await fetch(url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCsrfToken(),
          },
          body: JSON.stringify(payload),
        });

        const data = await response.json();

        if (data.success) {
          alert("Login successful!");
          window.location.href = data.redirect_url;
        } else {
          alert(data.error || "Login failed. Try again.");
        }
      } catch (error) {
        console.error("Login error:", error);
        alert("Something went wrong. Try again later.");
      }
    });
  }

  // Handle Signup
  const signupForm = document.getElementById("signupForm");
  if (signupForm) {
    signupForm.addEventListener("submit", async (e) => {
      e.preventDefault();

      const url = "/accounts/signup/";
      const payload = {
        username: document.getElementById("username").value,
        email: document.getElementById("email").value,
        password: document.getElementById("password").value,
        confirm_password: document.getElementById("confirm-password").value,
      };

      if (payload.password !== payload.confirm_password) {
        alert("Passwords do not match!");
        return;
      }

      try {
        const response = await fetch(url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCsrfToken(),
          },
          body: JSON.stringify(payload),
        });

        const data = await response.json();

        if (data.success) {
          alert("Signup successful! Redirecting...");
          window.location.href = data.redirect_url;
        } else {
          alert(data.error || "Signup failed. Try again.");
        }
      } catch (error) {
        console.error("Signup error:", error);
        alert("Something went wrong. Try again later.");
      }
    });
  }
});
