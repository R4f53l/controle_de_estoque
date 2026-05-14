
const API_BASE = window.location.origin.startsWith("http")
  ? window.location.origin
  : "http://localhost:8000";


(async () => {
    try {
        await verificar_token();
    } catch (error) {
        console.error(error);
    }
})();

const state = {
  products: [],
  purchases: [],
  purchaseItems: [],
  purchaseDraftItems: [],
  sales: [],
  saleItems: [],
  saleDraftItems: [],
  activeSection: "overview",
};

const endpoints = {
  products: "/produtos/listar_produtos",
  productCreate: "/produtos/adicionar_produto",
  productUpdate: (id) => `/produtos/atualizar_produto/${id}`,
  productDelete: (id) => `/produtos/excluir_produto/${id}`,
  purchases: "/compras/listar_compras",
  purchaseCreate: "/compras/adicionar_compra",
  purchaseCreateWithItems: "/compras/adicionar_compra_com_itens",
  purchaseUpdate: (id) => `/compras/atualizar_compra/${id}`,
  purchaseDelete: (id) => `/compras/excluir_compra/${id}`,
  purchaseItems: "/compra_produto/listar_todos",
  purchaseItemCreate: "/compra_produto/",
  sales: "/vendas/listar_vendas",
  saleCreate: "/vendas/adicionar_venda",
  saleCreateWithItems: "/vendas/adicionar_venda_com_itens",
  saleUpdate: (id) => `/vendas/atualizar_venda/${id}`,
  saleDelete: (id) => `/vendas/excluir_venda/${id}`,
  saleItems: "/venda_item/listar_todos",
  saleItemCreate: "/venda_item/",
};

const money = new Intl.NumberFormat("pt-BR", {
  style: "currency",
  currency: "BRL",
});

const els = {
  get pageTitle() { return document.querySelector("#page-title"); },
  get alerts() { return document.querySelector("#alerts"); },
  get connectionDot() { return document.querySelector("#connection-dot"); },
  get connectionText() { return document.querySelector("#connection-text"); },
  get refreshButton() { return document.querySelector("#refresh-button"); },
  get stockSearch() { return document.querySelector("#stock-search"); },
  get productSearch() { return document.querySelector("#product-search"); },
  get stockTable() { return document.querySelector("#stock-table"); },
  get productsTable() { return document.querySelector("#products-table"); },
  get purchasesTable() { return document.querySelector("#purchases-table"); },
  get salesTable() { return document.querySelector("#sales-table"); },
  get movementSummary() { return document.querySelector("#movement-summary"); },
  get metricProducts() { return document.querySelector("#metric-products"); },
  get metricStock() { return document.querySelector("#metric-stock"); },
  get metricPurchases() { return document.querySelector("#metric-purchases"); },
  get metricSales() { return document.querySelector("#metric-sales"); },
  get productForm() { return document.querySelector("#product-form"); },
  get productId() { return document.querySelector("#product-id"); },
  get productName() { return document.querySelector("#product-name"); },
  get productDescription() { return document.querySelector("#product-description"); },
  get productFormTitle() { return document.querySelector("#product-form-title"); },
  get cancelProductEdit() { return document.querySelector("#cancel-product-edit"); },
  get purchaseForm() { return document.querySelector("#purchase-form"); },
  get purchaseId() { return document.querySelector("#purchase-id"); },
  get purchaseDate() { return document.querySelector("#purchase-date"); },
  get purchaseReceivedDate() { return document.querySelector("#purchase-received-date"); },
  get purchaseForStock() { return document.querySelector("#purchase-for-stock"); },
  get purchaseTax() { return document.querySelector("#purchase-tax"); },
  get purchaseFormTitle() { return document.querySelector("#purchase-form-title"); },
  get cancelPurchaseEdit() { return document.querySelector("#cancel-purchase-edit"); },
  get purchaseItemBuilder() { return document.querySelector("#purchase-item-builder"); },
  get addPurchaseItem() { return document.querySelector("#add-purchase-item"); },
  get purchaseItemProduct() { return document.querySelector("#purchase-item-product"); },
  get purchaseItemQuantity() { return document.querySelector("#purchase-item-quantity"); },
  get purchaseItemPrice() { return document.querySelector("#purchase-item-price"); },
  get purchaseDraftList() { return document.querySelector("#purchase-draft-list"); },
  get purchaseDraftTable() { return document.querySelector("#purchase-draft-table"); },
  get purchaseDraftTotal() { return document.querySelector("#purchase-draft-total"); },
  get saleForm() { return document.querySelector("#sale-form"); },
  get saleId() { return document.querySelector("#sale-id"); },
  get saleDate() { return document.querySelector("#sale-date"); },
  get saleDirect() { return document.querySelector("#sale-direct"); },
  get saleFormTitle() { return document.querySelector("#sale-form-title"); },
  get cancelSaleEdit() { return document.querySelector("#cancel-sale-edit"); },
  get saleItemBuilder() { return document.querySelector("#sale-item-builder"); },
  get addSaleItem() { return document.querySelector("#add-sale-item"); },
  get saleItemProduct() { return document.querySelector("#sale-item-product"); },
  get saleItemQuantity() { return document.querySelector("#sale-item-quantity"); },
  get saleItemPrice() { return document.querySelector("#sale-item-price"); },
  get saleDraftList() { return document.querySelector("#sale-draft-list"); },
  get saleDraftTable() { return document.querySelector("#sale-draft-table"); },
  get saleDraftTotal() { return document.querySelector("#sale-draft-total"); },
};

function byId(collection, id) {
  return collection.find((item) => Number(item.id) === Number(id));
}

function formatDate(value) {
  if (!value) return "-";
  const [year, month, day] = value.split("-");
  return `${day}/${month}/${year}`;
}

function valueOrNull(value) {
  if (value === "" || value === null || value === undefined) return null;
  return Number(value);
}

function purchaseDraftTotal() {
  return state.purchaseDraftItems.reduce((sum, item) => {
    return sum + item.quantidade * (item.valor_unitario || 0);
  }, 0);
}

function purchaseTotalFromItems(purchase) {
  const items = state.purchaseItems.filter((item) => Number(item.compra_id) === Number(purchase.id));
  if (!items.length) return Number(purchase.valor || 0);

  return items.reduce((sum, item) => {
    return sum + Number(item.quantidade || 0) * Number(item.valor_unitario || 0);
  }, 0);
}

function saleDraftTotal() {
  return state.saleDraftItems.reduce((sum, item) => {
    return sum + item.quantidade * (item.valor_unitario || 0);
  }, 0);
}

function saleTotalFromItems(sale) {
  const items = state.saleItems.filter((item) => Number(item.venda_id) === Number(sale.id));
  if (!items.length) return Number(sale.valor || 0);

  return items.reduce((sum, item) => {
    return sum + Number(item.quantidade || 0) * Number(item.valor_unitario || 0);
  }, 0);
}

function setConnection(online, text) {
  els.connectionDot.classList.toggle("online", online);
  els.connectionDot.classList.toggle("offline", !online);
  els.connectionText.textContent = text;
}

function notify(message, type = "success") {
  const alert = document.createElement("div");
  alert.className = `alert ${type}`;
  alert.textContent = message;
  els.alerts.appendChild(alert);
  window.setTimeout(() => alert.remove(), 4500);
}

async function verificar_token() {
  const token = localStorage.getItem("token");

  if (!token) {
    window.location.href = API_BASE + "/login";
    return;
  }

  try {
    const response = await fetch(`${API_BASE}/auth/verificar_token`, {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      }
    });

    if (!response.ok) {
      // Se o status for 401 ou qualquer erro, limpa o token e desloga
      throw new Error("Sessão inválida ou expirada");
    }

    return token; // Token válido, segue o fluxo
  } catch (error) {
    console.error("Erro de autenticação:", error);
    localStorage.removeItem("token"); // Limpa o rastro
    window.location.href = API_BASE + "/login";
  }
}
  

  

async function request(path, options = {}) {
  const token = await verificar_token();

  if (!token) {
    throw new Error("Token de autenticação não encontrado. Faça login novamente.");
  }

  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`,
      ...(options.headers || {}),
    },
  });  


  const contentType = response.headers.get("content-type") || "";
  const data = contentType.includes("application/json")
    ? await response.json()
    : await response.text();

  if (!response.ok) {
    const detail = typeof data === "object" ? data.detail || data.message : data;
    throw new Error(detail || "Erro ao conversar com a API.");
  }

  return data;
}

async function loadData() {
  try {
    const [products, purchases, purchaseItems, sales, saleItems] = await Promise.all([
      request(endpoints.products),
      request(endpoints.purchases),
      request(endpoints.purchaseItems),
      request(endpoints.sales),
      request(endpoints.saleItems),
    ]);

    state.products = products;
    state.purchases = purchases;
    state.purchaseItems = purchaseItems.compra_produto || [];
    state.sales = sales;
    state.saleItems = saleItems.venda_item || [];
    setConnection(true, "API conectada");
    render();
  } catch (error) {
    setConnection(false, "API indisponivel");
    notify(error.message, "error");
  }
}

function stockRows() {
  return state.products.map((product) => {
    const purchased = state.purchaseItems
      .filter((item) => {
        if (Number(item.produto_id) !== Number(product.id)) return false;
        const purchase = byId(state.purchases, item.compra_id);
        return purchase && purchase.para_estoque && purchase.dataderecebimento !== null && purchase.dataderecebimento !== "";
      })
      .reduce((sum, item) => sum + Number(item.quantidade || 0), 0);
    const sold = state.saleItems
      .filter((item) => {
        if (Number(item.produto_id) !== Number(product.id)) return false;
        const sale = byId(state.sales, item.venda_id);
        return sale && sale.venda_direta === false; 
      })
      .reduce((sum, item) => sum + Number(item.quantidade || 0), 0);

    return {
      ...product,
      purchased,
      sold,
      balance: purchased - sold,
    };
  });
}

function badgeForStock(balance) {
  if (balance < 0) return '<span class="badge danger">Negativo</span>';
  if (balance === 0) return '<span class="badge warn">Zerado</span>';
  if (balance <= 5) return '<span class="badge warn">Baixo</span>';
  return '<span class="badge ok">Disponivel</span>';
}

function renderMetrics(rows) {
  const totalStock = rows.reduce((sum, item) => sum + item.balance, 0);
  const totalPurchases = state.purchases.reduce((sum, item) => sum + purchaseTotalFromItems(item), 0);
  const tax = state.purchases.reduce((sum, purchase) => sum + (purchase.valor_imposto || 0),0);
  const totalSales = state.sales.reduce((sum, item) => sum + saleTotalFromItems(item), 0);
 
  const result = tax + totalPurchases
  els.metricProducts.textContent = state.products.length;
  els.metricStock.textContent = totalStock;
  els.metricPurchases.textContent = money.format(result);
  els.metricSales.textContent = money.format(totalSales);

  els.movementSummary.innerHTML = [
    ["Compras registradas", state.purchases.length],
    ["Itens comprados", state.purchaseItems.length],
    ["Vendas registradas", state.sales.length],
    ["Itens vendidos", state.saleItems.length],
  ]
    .map(([label, value]) => `
      <div class="movement-item">
        <span>${label}</span>
        <strong>${value}</strong>
      </div>
    `)
    .join("");
}

function renderStockTable(rows) {
  const query = els.stockSearch.value.trim().toLowerCase();
  const filtered = rows.filter((row) => row.nome.toLowerCase().includes(query));

  els.stockTable.innerHTML = filtered.length
    ? filtered.map((row) => `
      <tr>
        <td><strong>${row.nome}</strong><br><span class="muted">${row.descricao || "-"}</span></td>
        <td>${row.purchased}</td>
        <td>${row.sold}</td>
        <td><strong>${row.balance}</strong></td>
        <td>${badgeForStock(row.balance)}</td>
      </tr>
    `).join("")
    : '<tr><td class="empty" colspan="5">Nenhum produto encontrado.</td></tr>';
}

function renderProductsTable(rows) {
  const query = els.productSearch.value.trim().toLowerCase();
  const filtered = rows.filter((row) => row.nome.toLowerCase().includes(query));

  els.productsTable.innerHTML = filtered.length
    ? filtered.map((row) => `
      <tr>
        <td>#${row.id}</td>
        <td><strong>${row.nome}</strong></td>
        <td>${row.descricao || "-"}</td>
        <td>${row.balance}</td>
        <td>
          <div class="actions">
            <button class="secondary" data-action="edit-product" data-id="${row.id}" type="button">Editar</button>
            <button class="danger" data-action="delete-product" data-id="${row.id}" type="button">Excluir</button>
          </div>
        </td>
      </tr>
    `).join("")
    : '<tr><td class="empty" colspan="5">Cadastre o primeiro produto.</td></tr>';
}

function renderPurchasesTable() {
  els.purchasesTable.innerHTML = state.purchases.length
    ? state.purchases.map((purchase) => {
      const items = state.purchaseItems.filter((item) => Number(item.compra_id) === Number(purchase.id));
      const total = purchaseTotalFromItems(purchase);
      return `
        <tr>
          <td>#${purchase.id}</td>
          <td>${formatDate(purchase.datadecompra)}</td>
          <td>${formatDate(purchase.dataderecebimento)}</td>
          <td>${money.format(total)}</td>
          <td>${money.format(purchase.valor_imposto || 0)}</td>
          <td>${purchase.para_estoque ? "Sim" : "Não"}</td>
          <td>${describeItems(items, "produto_id")}</td>
          <td>
            <div class="actions">
              <button class="secondary" data-action="edit-purchase" data-id="${purchase.id}" type="button">Editar</button>
              <button class="danger" data-action="delete-purchase" data-id="${purchase.id}" type="button">Excluir</button>
            </div>
          </td>
        </tr>
      `;
    }).join("")
    : '<tr><td class="empty" colspan="8">Nenhuma compra registrada.</td></tr>';
}

function renderSalesTable() {
  els.salesTable.innerHTML = state.sales.length
    ? state.sales.map((sale) => {
      const items = state.saleItems.filter((item) => Number(item.venda_id) === Number(sale.id));
      const total = saleTotalFromItems(sale);
      return `
        <tr>
          <td>#${sale.id}</td>
          <td>${formatDate(sale.datadevenda)}</td>
          <td>${money.format(total)}</td>
          <td>${sale.venda_direta ? "Sim" : "Não"}</td>
          <td>${describeItems(items, "produto_id")}</td>
          <td>
            <div class="actions">
              <button class="secondary" data-action="edit-sale" data-id="${sale.id}" type="button">Editar</button>
              <button class="danger" data-action="delete-sale" data-id="${sale.id}" type="button">Excluir</button>
            </div>
          </td>
        </tr>
      `;
    }).join("")
    : '<tr><td class="empty" colspan="5">Nenhuma venda registrada.</td></tr>';
}

function describeItems(items) {
  if (!items.length) return '<span class="badge">Sem itens</span>';
  return items
    .map((item) => {
      const product = byId(state.products, item.produto_id);
      const productName = product ? product.nome : `Produto #${item.produto_id}`;
      const total = Number(item.quantidade || 0) * Number(item.valor_unitario || 0);
      return `${item.quantidade}x ${productName} (${money.format(total)})`;
    })
    .join("<br>");
}

function option(label, value) {
  return `<option value="${value}">${label}</option>`;
}

function renderSelects() {
  const productOptions = state.products.length
    ? state.products.map((product) => option(product.nome, product.id)).join("")
    : option("Cadastre um produto primeiro", "");

  els.purchaseItemProduct.innerHTML = productOptions;
  els.saleItemProduct.innerHTML = productOptions;
}

function render() {
  const rows = stockRows();
  renderMetrics(rows);
  renderStockTable(rows);
  renderProductsTable(rows);
  renderPurchasesTable();
  renderSalesTable();
  renderSelects();
  renderPurchaseDraft();
  renderSaleDraft();
}

function renderPurchaseDraft() {
  els.purchaseDraftTotal.textContent = money.format(purchaseDraftTotal());
  els.purchaseDraftTable.innerHTML = state.purchaseDraftItems.length
    ? state.purchaseDraftItems.map((item, index) => {
      const product = byId(state.products, item.produto_id);
      const productName = product ? product.nome : `Produto #${item.produto_id}`;
      const total = item.quantidade * (item.valor_unitario || 0);
      return `
        <tr>
          <td>${productName}</td>
          <td>${item.quantidade}</td>
          <td>${money.format(item.valor_unitario || 0)}</td>
          <td>${money.format(total)}</td>
          <td>
            <button class="danger" data-action="remove-purchase-draft-item" data-index="${index}" type="button">Remover</button>
          </td>
        </tr>
      `;
    }).join("")
    : '<tr><td class="empty" colspan="5">Adicione os produtos desta compra.</td></tr>';
}

function renderSaleDraft() {
  els.saleDraftTotal.textContent = money.format(saleDraftTotal());
  els.saleDraftTable.innerHTML = state.saleDraftItems.length
    ? state.saleDraftItems.map((item, index) => {
      const product = byId(state.products, item.produto_id);
      const productName = product ? product.nome : `Produto #${item.produto_id}`;
      const total = item.quantidade * (item.valor_unitario || 0);
      return `
        <tr>
          <td>${productName}</td>
          <td>${item.quantidade}</td>
          <td>${money.format(item.valor_unitario || 0)}</td>
          <td>${money.format(total)}</td>
          <td>
            <button class="danger" data-action="remove-sale-draft-item" data-index="${index}" type="button">Remover</button>
          </td>
        </tr>
      `;
    }).join("")
    : '<tr><td class="empty" colspan="5">Adicione os produtos desta venda.</td></tr>';
}

function switchSection(section) {
  state.activeSection = section;
  document.querySelectorAll(".page-section").forEach((node) => {
    node.classList.toggle("active", node.id === section);
  });
  document.querySelectorAll(".nav-button").forEach((node) => {
    node.classList.toggle("active", node.dataset.section === section);
  });

  const activeButton = document.querySelector(`.nav-button[data-section="${section}"]`);
  els.pageTitle.textContent = activeButton ? activeButton.textContent : "Visao geral";
}

async function saveProduct(event) {
  event.preventDefault();
  const id = els.productId.value;
  const payload = {
    nome: els.productName.value.trim(),
    descricao: els.productDescription.value.trim() || null,
  };

  await request(id ? endpoints.productUpdate(id) : endpoints.productCreate, {
    method: id ? "PUT" : "POST",
    body: JSON.stringify(payload),
  });
  resetProductForm();
  notify("Produto salvo.");
  await loadData();
}

function editProduct(id) {
  const product = byId(state.products, id);
  if (!product) return;
  els.productId.value = product.id;
  els.productName.value = product.nome;
  els.productDescription.value = product.descricao || "";
  els.productFormTitle.textContent = "Editar produto";
  els.cancelProductEdit.classList.remove("hidden");
  switchSection("products");
}

function resetProductForm() {
  els.productForm.reset();
  els.productId.value = "";
  els.productFormTitle.textContent = "Novo produto";
  els.cancelProductEdit.classList.add("hidden");
}

async function savePurchase(event) {
  event.preventDefault();
  const id = els.purchaseId.value;

  if (id) {
    const existingPurchase = byId(state.purchases, id);
    const payload = {
      datadecompra: els.purchaseDate.value,
      dataderecebimento: els.purchaseReceivedDate.value || null,
      para_estoque: els.purchaseForStock.value === "true",
      valor_imposto: valueOrNull(els.purchaseTax.value),
      valor: existingPurchase ? purchaseTotalFromItems(existingPurchase) : 0,
    };

    await request(endpoints.purchaseUpdate(id), {
      method: "PUT",
      body: JSON.stringify(payload),
    });
  } else {
    if (!state.purchaseDraftItems.length) {
      throw new Error("Adicione pelo menos um item antes de salvar a compra.");
    }

    const payload = {
      datadecompra: els.purchaseDate.value,
      dataderecebimento: els.purchaseReceivedDate.value || null,
      para_estoque: els.purchaseForStock.value === "true",
      valor_imposto: valueOrNull(els.purchaseTax.value),
      itens: state.purchaseDraftItems,
    };

    await request(endpoints.purchaseCreateWithItems, {
      method: "POST",
      body: JSON.stringify(payload),
    });
  }

  resetPurchaseForm();
  notify("Compra salva.");
  await loadData();
}

function editPurchase(id) {
  const purchase = byId(state.purchases, id);
  if (!purchase) return;
  els.purchaseId.value = purchase.id;
  els.purchaseDate.value = purchase.datadecompra || "";
  els.purchaseReceivedDate.value = purchase.dataderecebimento || "";
  els.purchaseForStock.value = purchase.para_estoque !== false ? "true" : "false";
  els.purchaseTax.value = purchase.valor_imposto || "";
  state.purchaseDraftItems = [];
  renderPurchaseDraft();
  els.purchaseItemBuilder.classList.add("hidden");
  els.purchaseDraftList.classList.add("hidden");
  els.purchaseFormTitle.textContent = "Editar compra";
  els.cancelPurchaseEdit.classList.remove("hidden");
  switchSection("purchases");
}

function resetPurchaseForm() {
  els.purchaseForm.reset();
  els.purchaseForStock.value = "true";
  els.purchaseTax.value = "";
  els.purchaseId.value = "";
  state.purchaseDraftItems = [];
  renderPurchaseDraft();
  els.purchaseItemBuilder.classList.remove("hidden");
  els.purchaseDraftList.classList.remove("hidden");
  els.purchaseFormTitle.textContent = "Nova compra";
  els.cancelPurchaseEdit.classList.add("hidden");
  setTodayDefaults();
}

function addPurchaseDraftItem() {
  const payload = {
    produto_id: Number(els.purchaseItemProduct.value),
    quantidade: Number(els.purchaseItemQuantity.value),
    valor_unitario: valueOrNull(els.purchaseItemPrice.value) || 0,
  };

  if (!payload.produto_id) {
    throw new Error("Escolha um produto para adicionar.");
  }
  if (!payload.quantidade || payload.quantidade < 1) {
    throw new Error("Informe uma quantidade valida.");
  }

  state.purchaseDraftItems.push(payload);
  els.purchaseItemQuantity.value = "";
  els.purchaseItemPrice.value = "";
  renderPurchaseDraft();
}

async function saveSale(event) {
  event.preventDefault();
  const id = els.saleId.value;

  if (id) {
    const existingSale = byId(state.sales, id);
    const payload = {
      datadevenda: els.saleDate.value,
      venda_direta: els.saleDirect.value === "true",
      valor: existingSale ? saleTotalFromItems(existingSale) : 0,
    };

    await request(endpoints.saleUpdate(id), {
      method: "PUT",
      body: JSON.stringify(payload),
    });
  } else {
    if (!state.saleDraftItems.length) {
      throw new Error("Adicione pelo menos um item antes de salvar a venda.");
    }

    const payload = {
      datadevenda: els.saleDate.value,
      venda_direta: els.saleDirect.value === "true",
      itens: state.saleDraftItems,
    };

    await request(endpoints.saleCreateWithItems, {
      method: "POST",
      body: JSON.stringify(payload),
    });
  }

  resetSaleForm();
  notify("Venda salva.");
  await loadData();
}

function editSale(id) {
  const sale = byId(state.sales, id);
  if (!sale) return;
  els.saleId.value = sale.id;
  els.saleDate.value = sale.datadevenda || "";
  els.saleDirect.value = sale.venda_direta === true ? "true" : "false";
  state.saleDraftItems = [];
  renderSaleDraft();
  els.saleItemBuilder.classList.add("hidden");
  els.saleDraftList.classList.add("hidden");
  els.saleFormTitle.textContent = "Editar venda";
  els.cancelSaleEdit.classList.remove("hidden");
  switchSection("sales");
}

function resetSaleForm() {
  els.saleForm.reset();
  els.saleDirect.value = "false";
  els.saleId.value = "";
  state.saleDraftItems = [];
  renderSaleDraft();
  els.saleItemBuilder.classList.remove("hidden");
  els.saleDraftList.classList.remove("hidden");
  els.saleFormTitle.textContent = "Nova venda";
  els.cancelSaleEdit.classList.add("hidden");
  setTodayDefaults();
}

function addSaleDraftItem() {
  const payload = {
    produto_id: Number(els.saleItemProduct.value),
    quantidade: Number(els.saleItemQuantity.value),
    valor_unitario: valueOrNull(els.saleItemPrice.value) || 0,
  };

  if (!payload.produto_id) {
    throw new Error("Escolha um produto para adicionar.");
  }
  if (!payload.quantidade || payload.quantidade < 1) {
    throw new Error("Informe uma quantidade valida.");
  }

  state.saleDraftItems.push(payload);
  els.saleItemQuantity.value = "";
  els.saleItemPrice.value = "";
  renderSaleDraft();
}

async function deleteResource(kind, id) {
  const labels = {
    product: "produto",
    purchase: "compra",
    sale: "venda",
  };
  const paths = {
    product: endpoints.productDelete(id),
    purchase: endpoints.purchaseDelete(id),
    sale: endpoints.saleDelete(id),
  };

  const confirmed = window.confirm(`Excluir ${labels[kind]} #${id}?`);
  if (!confirmed) return;

  await request(paths[kind], { method: "DELETE" });
  notify(`${labels[kind][0].toUpperCase()}${labels[kind].slice(1)} excluido.`);
  await loadData();
}

async function handleTableClick(event) {
  const button = event.target.closest("button[data-action]");
  if (!button) return;

  const id = button.dataset.id;
  const action = button.dataset.action;

  const actions = {
    "edit-product": () => editProduct(id),
    "delete-product": () => deleteResource("product", id),
    "edit-purchase": () => editPurchase(id),
    "delete-purchase": () => deleteResource("purchase", id),
    "edit-sale": () => editSale(id),
    "delete-sale": () => deleteResource("sale", id),
    "remove-purchase-draft-item": () => {
      state.purchaseDraftItems.splice(Number(button.dataset.index), 1);
      renderPurchaseDraft();
    },
    "remove-sale-draft-item": () => {
      state.saleDraftItems.splice(Number(button.dataset.index), 1);
      renderSaleDraft();
    },
  };

  if (actions[action]) {
    await actions[action]();
  }
}

function setTodayDefaults() {
  const today = new Date().toISOString().slice(0, 10);
  if (!els.purchaseDate.value) els.purchaseDate.value = today;
  if (!els.saleDate.value) els.saleDate.value = today;
}

function bindEvents() {
  document.querySelectorAll(".nav-button").forEach((button) => {
    button.addEventListener("click", () => switchSection(button.dataset.section));
  });

  els.refreshButton.addEventListener("click", loadData);
  els.stockSearch.addEventListener("input", () => renderStockTable(stockRows()));
  els.productSearch.addEventListener("input", () => renderProductsTable(stockRows()));
  els.productForm.addEventListener("submit", withErrorHandling(saveProduct));
  els.cancelProductEdit.addEventListener("click", resetProductForm);
  els.purchaseForm.addEventListener("submit", withErrorHandling(savePurchase));
  els.cancelPurchaseEdit.addEventListener("click", resetPurchaseForm);
  els.addPurchaseItem.addEventListener("click", withErrorHandling(addPurchaseDraftItem));
  els.saleForm.addEventListener("submit", withErrorHandling(saveSale));
  els.cancelSaleEdit.addEventListener("click", resetSaleForm);
  els.addSaleItem.addEventListener("click", withErrorHandling(addSaleDraftItem));
  document.body.addEventListener("click", withErrorHandling(handleTableClick));
}

function withErrorHandling(handler) {
  return async (event) => {
    try {
      await handler(event);
    } catch (error) {
      notify(error.message, "error");
    }
  };
}

bindEvents();
setTodayDefaults();
loadData();

;
loadData();
