/* ==========================================================================
   SECCO INTERNAL — helpers de frontend
   A oficina acontece no backend; este arquivo so faz chamadas HTTP e renderiza.
   ========================================================================== */

const TOKEN_KEY = "secco_token";

function saveToken(token) {
  localStorage.setItem(TOKEN_KEY, token);
}

function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

function clearToken() {
  localStorage.removeItem(TOKEN_KEY);
}

/** Redireciona para o login se nao houver token salvo. */
function requireToken() {
  const token = getToken();
  if (!token) {
    window.location.href = "index.html";
    return null;
  }
  return token;
}

/** Chamada JSON autenticada. Devolve { ok, status, data }. */
async function api(path, options = {}) {
  const response = await fetch(path, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      Authorization: "Bearer " + (getToken() || ""),
      ...(options.headers || {}),
    },
  });

  let data = null;
  try {
    data = await response.json();
  } catch (error) {
    data = null;
  }

  if (response.status === 401) {
    clearToken();
    window.location.href = "index.html";
  }

  return { ok: response.ok, status: response.status, data };
}

async function logout() {
  try {
    await api("/api/logout", { method: "POST" });
  } catch (error) {
    /* mesmo se a chamada falhar, limpamos o token local */
  }
  clearToken();
  window.location.href = "index.html";
}

function showAlert(message, kind = "error") {
  const element = document.getElementById("alert");
  if (!element) return;
  element.textContent = message;
  element.className = "alert " + kind;
  element.hidden = false;
}

function hideAlert() {
  const element = document.getElementById("alert");
  if (element) element.hidden = true;
}

/** Escapa texto vindo da API antes de injetar no HTML. */
function escapeHtml(value) {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function roleBadge(role) {
  const safe = escapeHtml(role);
  return `<span class="badge ${safe}">${safe}</span>`;
}

function statusBadge(status) {
  const safe = escapeHtml(status);
  return `<span class="badge ${safe}">${safe}</span>`;
}

/** Monta a barra superior comum a todas as paginas internas. */
function renderTopbar(activePage) {
  const host = document.getElementById("topbar");
  if (!host) return;

  const pages = [
    { href: "dashboard.html", label: "Dashboard", id: "dashboard" },
    { href: "users.html", label: "Usuários", id: "users" },
    { href: "admin.html", label: "Administração", id: "admin" },
  ];

  const links = pages
    .map(
      (page) =>
        `<a href="${page.href}"${
          page.id === activePage ? ' class="active" aria-current="page"' : ""
        }>${page.label}</a>`
    )
    .join("");

  host.innerHTML = `
    <div class="topbar">
      <div class="topbar-inner">
        <div class="brand">
          <img src="secco-logo.svg" alt="SECCO" />
          <span class="brand-divider"></span>
          <span class="brand-tag">Internal</span>
        </div>
        <div class="row">
          <span class="status-pill"
            ><span class="status-dot" aria-hidden="true"></span>Sistema online</span
          >
          <button class="ghost" onclick="logout()">Sair</button>
        </div>
      </div>
    </div>
    <div class="page">
      <nav class="tabs" aria-label="Seções">${links}</nav>
      <div id="page-body"></div>
    </div>
  `;

  return document.getElementById("page-body");
}
