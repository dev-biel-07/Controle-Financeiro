/**
 * login.js — lida com o envio dos formulários de login e cadastro.
 */

// Se já estiver logado, vai direto pro dashboard
if (isLoggedIn()) {
  window.location.href = "/app/dashboard.html";
}

function switchTab(tab) {
  const isLogin = tab === "login";
  document.getElementById("tab-login").classList.toggle("active", isLogin);
  document.getElementById("tab-register").classList.toggle("active", !isLogin);
  document.getElementById("login-form").classList.toggle("hidden", !isLogin);
  document.getElementById("register-form").classList.toggle("hidden", isLogin);
}

document.getElementById("login-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const errorEl = document.getElementById("login-error");
  errorEl.classList.remove("visible");

  const email = document.getElementById("login-email").value;
  const password = document.getElementById("login-password").value;

  // A rota de login espera dados de formulário (OAuth2), não JSON.
  const body = new URLSearchParams();
  body.append("username", email);
  body.append("password", password);

  try {
    const response = await fetch("/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body,
    });

    if (!response.ok) {
      const data = await response.json().catch(() => ({}));
      throw new Error(data.detail || "Email ou senha incorretos.");
    }

    const data = await response.json();
    setToken(data.access_token);
    window.location.href = "/app/dashboard.html";
  } catch (err) {
    errorEl.textContent = err.message;
    errorEl.classList.add("visible");
  }
});

document.getElementById("register-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const errorEl = document.getElementById("register-error");
  errorEl.classList.remove("visible");

  const email = document.getElementById("register-email").value;
  const password = document.getElementById("register-password").value;

  try {
    const response = await fetch("/auth/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    if (!response.ok) {
      const data = await response.json().catch(() => ({}));
      throw new Error(data.detail || "Não foi possível criar a conta.");
    }

    // Cadastro deu certo: faz login automaticamente
    const body = new URLSearchParams();
    body.append("username", email);
    body.append("password", password);

    const loginResponse = await fetch("/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body,
    });
    const loginData = await loginResponse.json();
    setToken(loginData.access_token);
    window.location.href = "/app/dashboard.html";
  } catch (err) {
    errorEl.textContent = err.message;
    errorEl.classList.add("visible");
  }
});
