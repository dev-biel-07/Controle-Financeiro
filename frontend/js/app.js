/**
 * app.js — funções compartilhadas entre as páginas:
 * guardar/ler o token JWT e fazer chamadas autenticadas à API.
 *
 * Como o frontend é servido pela própria API (mesma origem),
 * não precisamos de CORS nem de configurar uma URL base externa.
 */

const TOKEN_KEY = "finance_tracker_token";

function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

function setToken(token) {
  localStorage.setItem(TOKEN_KEY, token);
}

function clearToken() {
  localStorage.removeItem(TOKEN_KEY);
}

function isLoggedIn() {
  return !!getToken();
}

function requireAuth() {
  if (!isLoggedIn()) {
    window.location.href = "/app/index.html";
  }
}

function logout() {
  clearToken();
  window.location.href = "/app/index.html";
}

/**
 * Wrapper de fetch que já inclui o header Authorization.
 * Se a API responder 401 (token inválido/expirado), desloga automaticamente.
 */
async function apiFetch(path, options = {}) {
  const headers = options.headers ? { ...options.headers } : {};
  const token = getToken();
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const response = await fetch(path, { ...options, headers });

  if (response.status === 401) {
    clearToken();
    window.location.href = "/app/index.html";
    throw new Error("Sessão expirada, faça login novamente.");
  }

  return response;
}

function showToast(message, isError = false) {
  let toast = document.getElementById("toast");
  if (!toast) {
    toast = document.createElement("div");
    toast.id = "toast";
    toast.className = "toast";
    document.body.appendChild(toast);
  }
  toast.textContent = message;
  toast.className = "toast" + (isError ? " error" : "");
  requestAnimationFrame(() => toast.classList.add("show"));
  setTimeout(() => toast.classList.remove("show"), 3000);
}

function formatCurrency(value) {
  return value.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });
}

function formatDate(isoString) {
  const date = new Date(isoString);
  return date.toLocaleDateString("pt-BR");
}
