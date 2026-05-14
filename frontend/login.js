const API_BASE = window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1"
  ? "http://localhost:8000" 
  : "https://controle-de-estoque-eyi8.onrender.com";

const endpoints = {
  login: "/auth/login",
};

const els = {
  loginForm: document.querySelector("#login-form"),
  emailInput: document.querySelector("#email"),
  passwordInput: document.querySelector("#password"),
  messageDiv: document.querySelector("#message"),
};

async function login(event) {
  event.preventDefault();

  els.messageDiv.classList.remove("text-success");
  els.messageDiv.classList.add("text-danger");
  els.messageDiv.textContent = "";

  const formData = new URLSearchParams();
  const email = els.emailInput.value.trim();
  const password = els.passwordInput.value;
  formData.append("username", email);
  formData.append("password", password);

  try {
    const response = await fetch(`${API_BASE}${endpoints.login}`, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: formData,
    });

    const data = await response.json();

    if (response.ok && data.access_token) {
      localStorage.setItem("token", data.access_token);
      localStorage.setItem("vendedor_id", data.vendedor_id);

      els.messageDiv.classList.remove("text-danger");
      els.messageDiv.classList.add("text-success");
      els.messageDiv.textContent = "Sucesso! Redirecionando...";
      window.location.href = API_BASE;
      return;
    }
    else {
      els.messageDiv.textContent = `Erro: ${data.detail || "Falha no login"}`;
    }

    
  } catch (error) {
    console.error("Erro critico:", error);
    els.messageDiv.textContent = "Erro ao conectar com a API.";
  }
}

els.loginForm.addEventListener("submit", login);
