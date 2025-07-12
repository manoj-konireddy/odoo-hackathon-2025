// Define fetchAPI utility function
function fetchAPI(endpoint, method = "GET", data = null) {
  const baseURL = "http://localhost:5000"; // Update if using different port or domain
  const options = {
    method,
    headers: {
      "Content-Type": "application/json"
    }
  };
  if (data) {
    options.body = JSON.stringify(data);
  }

  return fetch(baseURL + endpoint, options).then((res) => res.json());
}

// Handle registration form submission
const registerForm = document.getElementById("registerForm");

if (registerForm) {
  registerForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = document.getElementById("username").value;
    const email    = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    try {
      const res = await fetchAPI("/auth/register", "POST", { username, email, password });

      if (res.success) {
        // ✅ Redirect to login page after successful registration
        window.location.href = "login.html";
      } else {
        document.getElementById("registerMessage").textContent =
          res.message || "Registration failed";
      }
    } catch (err) {
      console.error(err);
      document.getElementById("registerMessage").textContent = "Server error. Please try again.";
    }
  });
}
