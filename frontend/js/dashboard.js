/**
 * dashboard.js — carrega os dados da API e monta a tela principal.
 */

requireAuth();

let chartInstance = null;

async function loadDashboard() {
  await Promise.all([loadExpenses(), loadCategories(), loadReport()]);
}

// ---------- Gastos ----------
async function loadExpenses() {
  const response = await apiFetch("/expenses/?limit=20");
  const expenses = await response.json();
  renderExpenseList(expenses);
  document.getElementById("summary-count").textContent = expenses.length;
}

function renderExpenseList(expenses) {
  const list = document.getElementById("expense-list");
  list.innerHTML = "";

  if (expenses.length === 0) {
    list.innerHTML = '<li class="empty-state">Nenhum gasto registrado ainda.</li>';
    return;
  }

  const categoryMap = window.__categoryMap || {};

  expenses.forEach((expense) => {
    const li = document.createElement("li");
    li.className = "expense-item";

    const categoryName = expense.category_id ? categoryMap[expense.category_id] : null;

    li.innerHTML = `
      <div class="expense-info">
        <div class="description">${escapeHtml(expense.description)}</div>
        <div class="meta">${formatDate(expense.date)}</div>
        ${categoryName ? `<span class="category-pill">${escapeHtml(categoryName)}</span>` : ""}
      </div>
      <div style="display:flex; align-items:center;">
        <span class="expense-amount">${formatCurrency(expense.amount)}</span>
        <button class="btn btn-danger" data-id="${expense.id}">Excluir</button>
      </div>
    `;

    li.querySelector(".btn-danger").addEventListener("click", () => deleteExpense(expense.id));
    list.appendChild(li);
  });
}

async function deleteExpense(id) {
  if (!confirm("Tem certeza que deseja excluir esse gasto?")) return;
  try {
    await apiFetch(`/expenses/${id}`, { method: "DELETE" });
    showToast("Gasto excluído.");
    await loadDashboard();
  } catch (err) {
    showToast("Erro ao excluir gasto.", true);
  }
}

document.getElementById("expense-form").addEventListener("submit", async (e) => {
  e.preventDefault();

  const description = document.getElementById("expense-description").value;
  const amount = parseFloat(document.getElementById("expense-amount").value);
  const categoryId = document.getElementById("expense-category").value;

  try {
    const response = await apiFetch("/expenses/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        description,
        amount,
        category_id: categoryId ? parseInt(categoryId) : null,
      }),
    });

    if (!response.ok) throw new Error("Falha ao criar gasto");

    e.target.reset();
    showToast("Gasto adicionado!");
    await loadDashboard();
  } catch (err) {
    showToast("Erro ao adicionar gasto.", true);
  }
});

// ---------- Categorias ----------
async function loadCategories() {
  const response = await apiFetch("/categories/");
  const categories = await response.json();

  window.__categoryMap = {};
  categories.forEach((c) => (window.__categoryMap[c.id] = c.name));

  document.getElementById("summary-categories").textContent = categories.length;

  const select = document.getElementById("expense-category");
  select.innerHTML = '<option value="">Sem categoria</option>';
  categories.forEach((c) => {
    const option = document.createElement("option");
    option.value = c.id;
    option.textContent = c.name;
    select.appendChild(option);
  });

  const chipList = document.getElementById("category-chip-list");
  chipList.innerHTML = "";
  if (categories.length === 0) {
    chipList.innerHTML = '<span class="empty-state">Nenhuma categoria ainda.</span>';
  } else {
    categories.forEach((c) => {
      const chip = document.createElement("span");
      chip.className = "category-chip";
      chip.textContent = c.name;
      chipList.appendChild(chip);
    });
  }
}

document.getElementById("category-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const nameInput = document.getElementById("category-name");
  const name = nameInput.value.trim();
  if (!name) return;

  try {
    const response = await apiFetch("/categories/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name }),
    });
    if (!response.ok) throw new Error("Falha ao criar categoria");

    nameInput.value = "";
    showToast("Categoria criada!");
    await loadCategories();
  } catch (err) {
    showToast("Erro ao criar categoria.", true);
  }
});

// ---------- Relatório / Gráfico ----------
async function loadReport() {
  const response = await apiFetch("/expenses/report/by-category");
  const totals = await response.json();

  const entries = Object.entries(totals);
  const totalGeral = entries.reduce((sum, [, value]) => sum + value, 0);
  document.getElementById("summary-total").textContent = formatCurrency(totalGeral);

  const chartCanvas = document.getElementById("category-chart");
  const emptyState = document.getElementById("chart-empty");

  if (entries.length === 0) {
    chartCanvas.classList.add("hidden");
    emptyState.classList.remove("hidden");
    return;
  }

  chartCanvas.classList.remove("hidden");
  emptyState.classList.add("hidden");

  const labels = entries.map(([name]) => name);
  const values = entries.map(([, value]) => value);
  const colors = ["#10b981", "#3b82f6", "#f59e0b", "#ef4444", "#8b5cf6", "#ec4899", "#14b8a6"];

  if (chartInstance) {
    chartInstance.destroy();
  }

  chartInstance = new Chart(chartCanvas, {
    type: "doughnut",
    data: {
      labels,
      datasets: [
        {
          data: values,
          backgroundColor: labels.map((_, i) => colors[i % colors.length]),
          borderWidth: 0,
        },
      ],
    },
    options: {
      plugins: {
        legend: { position: "bottom", labels: { boxWidth: 12, font: { size: 12 } } },
      },
    },
  });
}

// ---------- Utilidades ----------
function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

loadDashboard();
