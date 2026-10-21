// Lead Engine PRO - Client Application Logic
// State Management
let currentDataset = "all_global";
let currentPage = 1;
let currentPageSize = 50;
let currentSearch = "";
let currentTier = "all";
let currentState = "all";
let currentCategory = "all";
let currentOpportunity = "all";
let currentHasPhone = false;
let currentSortCol = "";
let currentSortDir = "asc";
let searchTimer = null;
let activeLead = null;
let currentJobId = null;
let pollTimer = null;
window.leadDataMap = {};

// Tab Switching
function switchTab(tabId) {
  document.querySelectorAll(".tab-btn").forEach(function(b) { b.classList.remove("active"); });
  document.querySelectorAll(".tab-panel").forEach(function(p) { p.classList.remove("active"); });
  
  const buttons = document.querySelectorAll(".tab-btn");
  for (let i = 0; i < buttons.length; i++) {
    const attr = buttons[i].getAttribute("onclick");
    if (attr && attr.indexOf(tabId) !== -1) {
      buttons[i].classList.add("active");
      break;
    }
  }
  
  const targetPanel = document.getElementById("tab-" + tabId);
  if (targetPanel) targetPanel.classList.add("active");

  if (tabId === "sources") runConnectivityCheck();
  if (tabId === "datasets") loadDatasetCatalog();
}

// Fetch and render leads
async function loadLeads() {
  const tbody = document.getElementById("leadsTbody");
  if (!tbody) return;
  
  tbody.innerHTML = '<tr><td colspan="9" style="text-align:center;padding:48px 20px;"><div class="skeleton" style="width:260px;margin:0 auto 12px;height:18px;"></div><span style="color:var(--text-dim);font-weight:500;">Loading leads database...</span></td></tr>';
  const metaStatus = document.getElementById("metaStatus");
  if (metaStatus) metaStatus.textContent = "Loading...";

  const params = new URLSearchParams({
    dataset: currentDataset,
    page: currentPage,
    page_size: currentPageSize,
    search: currentSearch,
    tier: currentTier,
    state: currentState,
    category: currentCategory,
    opportunity: currentOpportunity,
    has_phone: currentHasPhone ? "true" : "false",
    sort_by: currentSortCol,
    sort_dir: currentSortDir
  });

  try {
    const res = await fetch("/api/leads?" + params.toString());
    if (!res.ok) {
      throw new Error("Failed to load leads (HTTP " + res.status + ")");
    }
    const data = await res.json();
    
    renderKPIs(data.stats, data.sources_breakdown);
    renderTable(data.leads, data.total);
    renderPagination(data.total, data.page, data.page_size);
    if (data.states) updateStatesFilter(data.states);
    if (data.categories) updateCategoriesFilter(data.categories);
    if (metaStatus) metaStatus.textContent = "Up to date";
  } catch (err) {
    console.error("Error loading leads:", err);
    tbody.innerHTML = '<tr><td colspan="9" style="text-align:center;padding:40px;color:var(--accent-rose);font-size:14px;">' +
      '<div>⚠️ Error loading leads: ' + escapeHtml(err.message) + '</div>' +
      '<button class="btn btn-secondary" style="margin-top:12px;" onclick="loadLeads()">Try Again</button>' +
      '</td></tr>';
    if (metaStatus) metaStatus.textContent = "Error";
  }
}

function renderKPIs(stats, breakdown) {
  if (!stats) return;
  const total = Number(stats.total || 0);
  const tierA = Number(stats.tier_a || 0);
  const tierB = Number(stats.tier_b || 0);
  const phone = Number(stats.with_phone || 0);

  const kTotal = document.getElementById("kpiTotal");
  const kTierA = document.getElementById("kpiTierA");
  const kTierB = document.getElementById("kpiTierB");
  const kPhone = document.getElementById("kpiWithPhone");

  if (kTotal) kTotal.textContent = total.toLocaleString();

  const tierAPct = total > 0 ? ((tierA / total) * 100).toFixed(1) : "72.0";
  const tierBPct = total > 0 ? ((tierB / total) * 100).toFixed(1) : "28.0";
  const phonePct = total > 0 ? ((phone / total) * 100).toFixed(1) : "23.0";

  if (kTierA) {
    kTierA.innerHTML = tierA.toLocaleString() + ' <span style="font-size:12px;font-weight:600;opacity:0.85;">(' + tierAPct + '%)</span>';
  }
  if (kTierB) {
    kTierB.innerHTML = tierB.toLocaleString() + ' <span style="font-size:12px;font-weight:600;opacity:0.85;">(' + tierBPct + '%)</span>';
  }
  if (kPhone) {
    kPhone.innerHTML = phone.toLocaleString() + ' <span style="font-size:12px;font-weight:600;opacity:0.85;">(' + phonePct + '%)</span>';
  }

  // Update banner if present
  const bannerTotal = document.getElementById("bannerTotalCount");
  if (bannerTotal) bannerTotal.textContent = total.toLocaleString();

  if (breakdown && breakdown.length > 0) {
    renderSourceDistribution(breakdown);
  }
}

function renderSourceDistribution(breakdown) {
  const bar = document.getElementById("portfolioProgressBar");
  const chipsRow = document.getElementById("sourceChipsRow");
  if (!bar || !chipsRow) return;

  // Render multi-segment bar
  let barHtml = "";
  for (let i = 0; i < breakdown.length; i++) {
    const item = breakdown[i];
    if (item.id === "all_global" || item.pct <= 0) continue;
    barHtml += '<div class="portfolio-segment" style="width:' + item.pct + '%;background:' + item.color + ';" ' +
      'title="' + escapeHtml(item.label) + ': ' + Number(item.count).toLocaleString() + ' leads (' + item.pct + '%)" ' +
      'onclick="selectSourceChip(\'' + item.id + '\')"></div>';
  }
  bar.innerHTML = barHtml;

  // Render clickable source chips
  let chipsHtml = "";
  for (let i = 0; i < breakdown.length; i++) {
    const item = breakdown[i];
    const isActive = (currentDataset === item.id) ? " active" : "";
    chipsHtml += '<button class="source-chip' + isActive + '" onclick="selectSourceChip(\'' + item.id + '\')">' +
      '<span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:' + item.color + ';"></span>' +
      '<span>' + escapeHtml(item.badge || item.label) + '</span>' +
      '<span class="chip-pct" style="color:' + item.color + ';">' + item.pct + '%</span>' +
      '<span style="color:var(--text-dim);font-size:11px;">(' + formatNumberCompact(item.count) + ')</span>' +
      '</button>';
  }
  chipsRow.innerHTML = chipsHtml;
}

function selectSourceChip(id) {
  currentDataset = id;
  currentPage = 1;
  const sel = document.getElementById("datasetSelect");
  if (sel) sel.value = id;
  
  const bannerShare = document.getElementById("bannerSharePct");
  if (bannerShare) {
    bannerShare.textContent = (id === "all_global") ? "100% (All Sources)" : "Filtered Dataset";
  }
  
  loadLeads();
}

function formatNumberCompact(num) {
  const n = Number(num || 0);
  if (n >= 1000000) return (n / 1000000).toFixed(1) + "M";
  if (n >= 1000) return (n / 1000).toFixed(0) + "k";
  return n.toLocaleString();
}


function renderTable(leads, total) {
  const tbody = document.getElementById("leadsTbody");
  if (!tbody) return;
  const metaCount = document.getElementById("metaCount");
  if (metaCount) metaCount.textContent = Number(total || 0).toLocaleString();
  window.leadDataMap = {};
  
  if (!leads || leads.length === 0) {
    tbody.innerHTML = '<tr><td colspan="9" style="text-align:center;padding:60px 20px;color:var(--text-dim);font-size:14px;">' +
      '<div style="font-size:32px;margin-bottom:12px;">🔍</div>' +
      '<div>No matching leads found for current search/filters.</div>' +
      '<button class="btn btn-secondary" style="margin-top:14px;" onclick="resetFilters()">Reset All Filters</button>' +
      '</td></tr>';
    return;
  }

  let rowsHtml = "";
  for (let idx = 0; idx < leads.length; idx++) {
    const lead = leads[idx];
    const safeId = String(lead.id || ("lead_" + idx));
    window.leadDataMap[safeId] = lead;

    const rowNum = (currentPage - 1) * currentPageSize + idx + 1;
    const tier = lead.tier || "A";
    const tierClass = tier === "A" ? "tier-A" : (tier === "B" ? "tier-B" : "tier-C");
    
    let phoneHtml = '<span style="color:var(--text-dim);font-size:12px;">No phone</span>';
    if (lead.phone) {
      phoneHtml = '<a href="tel:' + escapeHtml(lead.phone) + '" class="phone-link">📞 ' + escapeHtml(lead.phone) + '</a>' +
        '<button class="copy-btn" data-id="' + safeId + '" onclick="copyPhoneById(this.dataset.id)" title="Copy phone">Copy</button>';
    }

    let webHtml = '<span class="web-badge no-site">⚠️ No Website</span>';
    if (lead.website && String(lead.website).indexOf("None") === -1 && String(lead.website).trim() !== "") {
      const rawWeb = String(lead.website).trim();
      const url = rawWeb.indexOf("http") === 0 ? rawWeb : "https://" + rawWeb;
      webHtml = '<a href="' + escapeHtml(url) + '" target="_blank" rel="noopener noreferrer" class="web-badge has-site">🌐 Visit Site</a>';
    }

    let locText = "";
    if (lead.city && lead.state) {
      locText = lead.city + ", " + lead.state;
    } else if (lead.city) {
      locText = lead.city;
    } else if (lead.state) {
      locText = lead.state;
    }

    const leadStatus = lead.status || "new";

    const srcBadge = lead.source_badge || "🌟 Curated";
    const srcColor = lead.source_color || "#3b82f6";
    const sourceHtml = '<span class="source-pill" style="background:' + srcColor + '18;color:' + srcColor + ';border:1px solid ' + srcColor + '40;">' + escapeHtml(srcBadge) + '</span>';

    rowsHtml += '<tr id="row_' + safeId + '">' +
      '<td style="color:var(--text-dim);font-size:12px;text-align:center;">' + rowNum + '</td>' +
      '<td style="white-space:nowrap;">' + sourceHtml + '</td>' +
      '<td><span class="tier-badge ' + tierClass + '">Tier ' + escapeHtml(tier) + '</span></td>' +
      '<td>' +
        '<div class="biz-name">' + escapeHtml(lead.name || "Unknown Business") + '</div>' +
        '<div class="cat-pill" title="' + escapeHtml(lead.category || "") + '">' + escapeHtml(lead.category || "General") + '</div>' +
        (locText ? '<div class="loc-pill">📍 ' + escapeHtml(locText) + '</div>' : '') +
      '</td>' +
      '<td>' + phoneHtml + '</td>' +
      '<td>' + webHtml + '</td>' +
      '<td>' +
        '<div class="pitch-snippet" title="' + escapeHtml(lead.pitch || "") + '">' + escapeHtml(lead.pitch || "Ready for outreach.") + '</div>' +
        '<button class="copy-btn" data-id="' + safeId + '" onclick="copyPitchById(this.dataset.id)">Copy Script</button>' +
      '</td>' +
      '<td>' +
        '<select class="status-select ' + leadStatus + '" data-id="' + safeId + '" onchange="updateRowStatusById(this.dataset.id, this.value, this)">' +
          '<option value="new"' + (leadStatus === 'new' ? ' selected' : '') + '>New</option>' +
          '<option value="contacted"' + (leadStatus === 'contacted' ? ' selected' : '') + '>Contacted</option>' +
          '<option value="interested"' + (leadStatus === 'interested' ? ' selected' : '') + '>Interested</option>' +
          '<option value="meeting"' + (leadStatus === 'meeting' ? ' selected' : '') + '>Meeting</option>' +
          '<option value="won"' + (leadStatus === 'won' ? ' selected' : '') + '>Won</option>' +
          '<option value="not_interested"' + (leadStatus === 'not_interested' ? ' selected' : '') + '>Not Int.</option>' +
        '</select>' +
      '</td>' +
      '<td style="text-align:center;">' +
        '<button class="btn btn-secondary" style="padding:5px 12px;font-size:12px;" data-id="' + safeId + '" onclick="openDrawerById(this.dataset.id)">View</button>' +
      '</td>' +
    '</tr>';
  }
  tbody.innerHTML = rowsHtml;
}

function copyPhoneById(id) {
  const lead = window.leadDataMap[id];
  if (lead && lead.phone) copyText(lead.phone, "Phone number copied!");
}

function copyPitchById(id) {
  const lead = window.leadDataMap[id];
  if (lead && lead.pitch) copyText(lead.pitch, "Cold pitch script copied!");
}

function openDrawerById(id) {
  const lead = window.leadDataMap[id];
  if (lead) openDrawer(lead);
}

async function updateRowStatusById(id, status, el) {
  const lead = window.leadDataMap[id];
  if (!lead) return;
  lead.status = status;
  el.className = "status-select " + status;
  try {
    await fetch("/api/leads/tag", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ tag_key: lead.tag_key || lead.id, status: status })
    });
    toast("Lead marked as " + status);
  } catch (err) {
    console.error("Status update error:", err);
  }
}

function renderPagination(total, page, pageSize) {
  const container = document.getElementById("pageBtnGroup");
  const infoEl = document.getElementById("paginationInfo");
  if (!container) return;

  const totalPages = Math.max(1, Math.ceil(total / pageSize));
  const start = Math.min(total, (page - 1) * pageSize + 1);
  const end = Math.min(total, page * pageSize);
  
  if (infoEl) {
    infoEl.textContent = "Showing " + start.toLocaleString() + " to " + end.toLocaleString() + " of " + total.toLocaleString() + " leads";
  }

  let html = "";
  html += '<button class="page-btn" ' + (page <= 1 ? "disabled" : "") + ' onclick="goToPage(1)">«</button>';
  html += '<button class="page-btn" ' + (page <= 1 ? "disabled" : "") + ' onclick="goToPage(' + (page - 1) + ')">‹</button>';

  let pStart = Math.max(1, page - 2);
  let pEnd = Math.min(totalPages, page + 2);
  for (let p = pStart; p <= pEnd; p++) {
    html += '<button class="page-btn ' + (p === page ? "active" : "") + '" onclick="goToPage(' + p + ')">' + p + '</button>';
  }

  html += '<button class="page-btn" ' + (page >= totalPages ? "disabled" : "") + ' onclick="goToPage(' + (page + 1) + ')">›</button>';
  html += '<button class="page-btn" ' + (page >= totalPages ? "disabled" : "") + ' onclick="goToPage(' + totalPages + ')">»</button>';
  
  container.innerHTML = html;
}

function goToPage(p) {
  currentPage = p;
  loadLeads();
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function updateStatesFilter(states) {
  const select = document.getElementById("stateFilter");
  if (!select || !states || states.length === 0) return;
  const curr = select.value;
  let html = '<option value="all">All States / Regions</option>';
  for (let i = 0; i < states.length; i++) {
    const s = states[i];
    html += '<option value="' + escapeHtml(s) + '"' + (s === curr ? ' selected' : '') + '>' + escapeHtml(s) + '</option>';
  }
  select.innerHTML = html;
}

function updateCategoriesFilter(categories) {
  const select = document.getElementById("catFilter");
  if (!select || !categories || categories.length === 0) return;
  const curr = select.value;
  let html = '<option value="all">All Categories</option>';
  for (let i = 0; i < categories.length; i++) {
    const c = categories[i];
    html += '<option value="' + escapeHtml(c) + '"' + (c === curr ? ' selected' : '') + '>' + escapeHtml(c) + '</option>';
  }
  select.innerHTML = html;
}

// Handlers
function onDatasetChange(val) {
  currentDataset = val;
  currentPage = 1;
  const sel = document.getElementById("datasetSelect");
  if (sel && sel.selectedOptions.length > 0) {
    const opt = sel.selectedOptions[0];
    const lbl = document.getElementById("kpiDatasetLabel");
    if (lbl) lbl.textContent = opt.text;
  }
  loadLeads();
}

function handleSearchInput(val) {
  const clearBtn = document.getElementById("searchClear");
  if (clearBtn) clearBtn.style.display = val ? "block" : "none";
  clearTimeout(searchTimer);
  searchTimer = setTimeout(function() {
    currentSearch = val.trim();
    currentPage = 1;
    loadLeads();
  }, 250);
}

function clearSearch() {
  const inp = document.getElementById("searchInput");
  if (inp) inp.value = "";
  handleSearchInput("");
}

function setTierFilter(tier) {
  currentTier = tier;
  document.querySelectorAll(".tier-pill-btn").forEach(function(b) {
    b.classList.toggle("active", b.getAttribute("data-tier") === tier);
  });
  currentPage = 1;
  loadLeads();
}

function onFilterChange() {
  const s = document.getElementById("stateFilter");
  if (s) currentState = s.value;
  currentPage = 1;
  loadLeads();
}

function onCatChange(val) {
  currentCategory = val;
  currentPage = 1;
  loadLeads();
}

function onOppChange(val) {
  currentOpportunity = val;
  currentPage = 1;
  loadLeads();
}

function toggleHasPhone() {
  currentHasPhone = !currentHasPhone;
  const t = document.getElementById("hasPhoneToggle");
  if (t) t.classList.toggle("active", currentHasPhone);
  currentPage = 1;
  loadLeads();
}

function onPageSizeChange(val) {
  currentPageSize = parseInt(val, 10) || 50;
  currentPage = 1;
  loadLeads();
}

function setSort(col) {
  if (currentSortCol === col) {
    currentSortDir = currentSortDir === "asc" ? "desc" : "asc";
  } else {
    currentSortCol = col;
    currentSortDir = "asc";
  }
  loadLeads();
}

function resetFilters() {
  currentSearch = "";
  currentTier = "all";
  currentState = "all";
  currentCategory = "all";
  currentOpportunity = "all";
  currentHasPhone = false;
  currentSortCol = "";
  currentSortDir = "asc";
  currentPage = 1;
  
  const inp = document.getElementById("searchInput");
  if (inp) inp.value = "";
  const clr = document.getElementById("searchClear");
  if (clr) clr.style.display = "none";
  
  document.querySelectorAll(".tier-pill-btn").forEach(function(b) {
    b.classList.toggle("active", b.getAttribute("data-tier") === "all");
  });
  
  const phoneBtn = document.getElementById("hasPhoneToggle");
  if (phoneBtn) phoneBtn.classList.remove("active");
  
  const stateSel = document.getElementById("stateFilter");
  if (stateSel) stateSel.value = "all";
  
  const catSel = document.getElementById("catFilter");
  if (catSel) catSel.value = "all";
  
  const oppSel = document.getElementById("oppFilter");
  if (oppSel) oppSel.value = "all";
  
  loadLeads();
}

// Slide-Out Drawer
function openDrawer(lead) {
  activeLead = lead;
  
  document.getElementById("drawerName").textContent = lead.name || "Unknown Business";
  document.getElementById("drawerCat").textContent = lead.category || "General Business";
  
  const tierBadge = document.getElementById("drawerTier");
  if (tierBadge) {
    tierBadge.textContent = "Tier " + (lead.tier || "A");
    tierBadge.className = "tier-badge tier-" + (lead.tier || "A");
  }
  
  document.getElementById("drawerPitch").textContent = lead.pitch || "No pitch script available.";
  document.getElementById("drawerWhy").textContent = lead.why || "Active business lead identified.";
  document.getElementById("drawerPhone").textContent = lead.phone || "No phone listed";
  document.getElementById("drawerAddress").textContent = lead.address || "Address not specified";
  
  const cityStateZip = [lead.city, lead.state, lead.zip].filter(Boolean).join(" ");
  document.getElementById("drawerCityState").textContent = cityStateZip || "Location not specified";
  document.getElementById("drawerOpp").textContent = lead.opportunity || "Standard Lead";

  const callBtn = document.getElementById("drawerCallBtn");
  if (callBtn) {
    if (lead.phone) {
      callBtn.href = "tel:" + lead.phone;
      callBtn.style.display = "inline-flex";
    } else {
      callBtn.style.display = "none";
    }
  }

  const mapBtn = document.getElementById("drawerMapBtn");
  if (mapBtn) {
    const mapQuery = encodeURIComponent((lead.name || "") + " " + (lead.address || "") + " " + (lead.city || "") + " " + (lead.state || ""));
    mapBtn.href = "https://www.google.com/maps/search/?api=1&query=" + mapQuery;
  }

  const webBtn = document.getElementById("drawerWebBtn");
  if (webBtn) {
    if (lead.website && String(lead.website).indexOf("None") === -1 && String(lead.website).trim() !== "") {
      const rawWeb = String(lead.website).trim();
      webBtn.href = rawWeb.indexOf("http") === 0 ? rawWeb : "https://" + rawWeb;
      webBtn.style.display = "inline-flex";
    } else {
      webBtn.style.display = "none";
    }
  }

  const statusSel = document.getElementById("drawerStatusSelect");
  if (statusSel) statusSel.value = lead.status || "new";
  
  const notesArea = document.getElementById("drawerNotes");
  if (notesArea) notesArea.value = lead.notes || "";

  document.getElementById("drawerBackdrop").classList.add("open");
  document.getElementById("leadDrawer").classList.add("open");
}

function closeDrawer() {
  document.getElementById("drawerBackdrop").classList.remove("open");
  document.getElementById("leadDrawer").classList.remove("open");
}

async function saveDrawerStatus(val) {
  if (!activeLead) return;
  activeLead.status = val;
  await fetch("/api/leads/tag", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ tag_key: activeLead.tag_key || activeLead.id, status: val, notes: activeLead.notes || "" })
  });
  toast("Status saved: " + val);
}

async function saveDrawerNotes(val) {
  if (!activeLead) return;
  activeLead.notes = val;
  await fetch("/api/leads/tag", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ tag_key: activeLead.tag_key || activeLead.id, status: activeLead.status || "new", notes: val })
  });
  toast("Notes saved.");
}

function copyDrawerPhone() {
  if (activeLead && activeLead.phone) copyText(activeLead.phone, "Phone copied!");
}

function copyDrawerPitch() {
  if (activeLead && activeLead.pitch) copyText(activeLead.pitch, "Cold pitch script copied!");
}

// ==================== Export Range Controls & CSV Engine ====================
function updateExportRangePreview() {
  const fromInput = document.getElementById("exportFromInput");
  const toInput = document.getElementById("exportToInput");
  const badge = document.getElementById("exportCountBadge");
  const btn = document.getElementById("exportRangeBtn");
  if (!fromInput || !toInput) return;

  let fromVal = parseInt(fromInput.value, 10);
  let toVal = parseInt(toInput.value, 10);

  if (isNaN(fromVal) || fromVal < 1) fromVal = 1;
  if (isNaN(toVal) || toVal < fromVal) toVal = fromVal;

  const count = toVal - fromVal + 1;
  if (badge) badge.textContent = count.toLocaleString();
  if (btn) btn.innerHTML = '<span>📥</span> Download Range CSV (' + count.toLocaleString() + ' Leads)';
}

function setExportRange(fromNum, toNum) {
  const fromInput = document.getElementById("exportFromInput");
  const toInput = document.getElementById("exportToInput");
  if (fromInput) fromInput.value = fromNum;
  if (toInput) toInput.value = toNum;

  // Highlight active preset button
  document.querySelectorAll(".btn-preset").forEach(function(btn) {
    btn.classList.remove("active");
    const txt = btn.textContent.trim();
    if (toNum === 1000 && txt.indexOf("1K") !== -1) btn.classList.add("active");
    else if (toNum === 5000 && txt.indexOf("5K") !== -1) btn.classList.add("active");
    else if (toNum === 10000 && txt.indexOf("10K") !== -1) btn.classList.add("active");
    else if (toNum === 25000 && txt.indexOf("25K") !== -1) btn.classList.add("active");
    else if (toNum === 50000 && txt.indexOf("50K") !== -1) btn.classList.add("active");
  });

  updateExportRangePreview();
}

function setExportNextBatch() {
  const fromInput = document.getElementById("exportFromInput");
  const toInput = document.getElementById("exportToInput");
  if (!fromInput || !toInput) return;

  let fromVal = parseInt(fromInput.value, 10) || 1;
  let toVal = parseInt(toInput.value, 10) || 5000;
  const batchSize = Math.max(1, toVal - fromVal + 1);

  const newFrom = toVal + 1;
  const newTo = toVal + batchSize;

  fromInput.value = newFrom;
  toInput.value = newTo;

  document.querySelectorAll(".btn-preset").forEach(function(b) { b.classList.remove("active"); });
  updateExportRangePreview();

  showToast("Export range advanced: Lead #" + newFrom.toLocaleString() + " to #" + newTo.toLocaleString());
}

function triggerRangeExport() {
  const fromInput = document.getElementById("exportFromInput");
  const toInput = document.getElementById("exportToInput");
  const btn = document.getElementById("exportRangeBtn");

  let fromVal = 1;
  let toVal = 5000;
  if (fromInput && toInput) {
    fromVal = Math.max(1, parseInt(fromInput.value, 10) || 1);
    toVal = Math.max(fromVal, parseInt(toInput.value, 10) || fromVal + 4999);
  }

  const count = toVal - fromVal + 1;

  if (btn) {
    btn.disabled = true;
    btn.innerHTML = '<span>⏳</span> Preparing ' + count.toLocaleString() + ' Leads...';
    setTimeout(function() {
      btn.disabled = false;
      updateExportRangePreview();
    }, 3500);
  }

  const params = new URLSearchParams({
    dataset: currentDataset,
    search: currentSearch,
    tier: currentTier,
    state: currentState,
    category: currentCategory,
    opportunity: currentOpportunity,
    has_phone: currentHasPhone ? "true" : "false",
    export: "csv",
    export_from: String(fromVal),
    export_to: String(toVal)
  });

  showToast("Downloading " + count.toLocaleString() + " leads (rows " + fromVal.toLocaleString() + " to " + toVal.toLocaleString() + ")...");
  window.location.href = "/api/leads?" + params.toString();
}

function exportCurrentLeads() {
  triggerRangeExport();
}

// Prospecting Pipeline Runner
async function startProspecting(e) {
  e.preventDefault();
  const runBtn = document.getElementById("runBtn");
  if (runBtn) {
    runBtn.disabled = true;
    runBtn.textContent = "⏳ Running Prospecting Engine...";
  }

  const sources = Array.from(document.querySelectorAll("input[name='src']:checked")).map(function(c) { return c.value; });
  const payload = {
    vertical: document.getElementById("runVertical").value,
    city: document.getElementById("runCity").value.trim(),
    state: document.getElementById("runState").value.trim(),
    country: document.getElementById("runCountry").value.trim(),
    sources: sources,
    demo: document.getElementById("runDemo").checked,
    enrich: document.getElementById("runEnrich").checked
  };

  const term = document.getElementById("terminal");
  if (term) term.textContent = "[" + new Date().toLocaleTimeString() + "] Initializing Lead Engine pipeline for " + payload.vertical + "...\n";
  
  const statusBadge = document.getElementById("runStatusBadge");
  if (statusBadge) {
    statusBadge.textContent = "PROSPECTING";
    statusBadge.style.background = "var(--accent-blue)";
  }
  const loadBtn = document.getElementById("loadRunBtn");
  if (loadBtn) loadBtn.style.display = "none";

  try {
    const res = await fetch("/run", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const d = await res.json();
    if (!res.ok) throw new Error(d.error || "Failed to start run");
    
    currentJobId = d.job_id;
    pollJob(currentJobId);
  } catch (err) {
    if (term) term.textContent += "\nERROR: " + err.message;
    if (runBtn) {
      runBtn.disabled = false;
      runBtn.textContent = "🚀 Start Lead Generation Run";
    }
    if (statusBadge) {
      statusBadge.textContent = "FAILED";
      statusBadge.style.background = "var(--accent-rose)";
    }
  }
}

function pollJob(jid) {
  clearInterval(pollTimer);
  pollTimer = setInterval(async function() {
    try {
      const res = await fetch("/progress/" + jid);
      const d = await res.json();
      const term = document.getElementById("terminal");
      if (term && d.log) {
        term.textContent = d.log.join("\n");
        term.scrollTop = term.scrollHeight;
      }

      if (d.done) {
        clearInterval(pollTimer);
        const runBtn = document.getElementById("runBtn");
        if (runBtn) {
          runBtn.disabled = false;
          runBtn.textContent = "🚀 Start Lead Generation Run";
        }

        const statusBadge = document.getElementById("runStatusBadge");
        if (d.error) {
          if (statusBadge) {
            statusBadge.textContent = "FAILED";
            statusBadge.style.background = "var(--accent-rose)";
          }
        } else {
          if (statusBadge) {
            statusBadge.textContent = "COMPLETED";
            statusBadge.style.background = "var(--accent-emerald)";
          }
          const loadBtn = document.getElementById("loadRunBtn");
          if (loadBtn) loadBtn.style.display = "inline-flex";
          toast("Prospecting finished! " + (d.leads ? d.leads.length : 0) + " leads found.");
          refreshDatasetsList();
        }
      }
    } catch (e) {
      console.error(e);
    }
  }, 1000);
}

async function refreshDatasetsList() {
  try {
    const res = await fetch("/api/datasets");
    const datasets = await res.json();
    const sel = document.getElementById("datasetSelect");
    if (sel) {
      sel.innerHTML = datasets.map(function(d) {
        return '<option value="' + d.id + '">' + escapeHtml(d.name) + ' (' + Number(d.count).toLocaleString() + ' leads)</option>';
      }).join("");
    }
  } catch (e) {
    console.error(e);
  }
}

function loadCompletedRun() {
  if (!currentJobId) return;
  const sel = document.getElementById("datasetSelect");
  currentDataset = "job_" + currentJobId;
  if (sel) sel.value = currentDataset;
  switchTab("leads");
  loadLeads();
}

function applyPresetMarket(val) {
  if (!val) return;
  const cityInp = document.getElementById("runCity");
  const stateInp = document.getElementById("runState");
  if (cityInp) cityInp.value = val;
  if (stateInp) stateInp.value = "";
}

// Data Sources Health Check
async function runConnectivityCheck() {
  const container = document.getElementById("probeResults");
  if (!container) return;
  container.innerHTML = '<div class="skeleton" style="height:60px;"></div>';
  try {
    const res = await fetch("/check");
    const data = await res.json();
    container.innerHTML = Object.entries(data).map(function(entry) {
      const src = entry[0];
      const status = entry[1];
      const isOk = status.ok;
      return '<div style="background:var(--bg-secondary);border:1px solid ' + (isOk ? 'rgba(16,185,129,0.3)' : 'rgba(239,68,68,0.3)') + ';padding:14px;border-radius:var(--radius-md);">' +
        '<div style="display:flex;align-items:center;justify-content:space-between;">' +
          '<b style="font-size:14px;">' + escapeHtml(src) + '</b>' +
          '<span class="tier-badge ' + (isOk ? 'tier-A' : 'tier-C') + '">' + (isOk ? 'ONLINE' : 'OFFLINE') + '</span>' +
        '</div>' +
        '<div style="font-size:12px;color:var(--text-dim);margin-top:4px;">' + escapeHtml(status.detail || (isOk ? 'Available and responding' : 'Unreachable')) + '</div>' +
      '</div>';
    }).join("");
  } catch (e) {
    container.innerHTML = '<div style="color:var(--accent-rose);">Failed to probe data sources: ' + escapeHtml(e.message) + '</div>';
  }
}

// Datasets Grid in Tab 4
async function loadDatasetCatalog() {
  const grid = document.getElementById("datasetGrid");
  if (!grid) return;
  try {
    const res = await fetch("/api/datasets");
    const datasets = await res.json();
    grid.innerHTML = datasets.map(function(d) {
      return '<div style="background:var(--bg-secondary);border:1px solid var(--border);border-radius:var(--radius-md);padding:18px;">' +
        '<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:6px;">' +
          '<b style="font-size:14px;color:var(--text-main);">' + escapeHtml(d.name) + '</b>' +
          '<span class="tier-badge tier-A">' + escapeHtml(d.badge || 'DATA') + '</span>' +
        '</div>' +
        '<div style="font-size:22px;font-family:var(--font-heading);font-weight:800;color:var(--accent-blue);margin:8px 0;">' +
          Number(d.count).toLocaleString() + ' <span style="font-size:12px;color:var(--text-dim);font-weight:400;">leads</span>' +
        '</div>' +
        '<div style="display:flex;gap:8px;margin-top:12px;">' +
          '<button class="btn btn-primary" style="flex:1;font-size:12px;padding:6px 12px;" data-id="' + escapeHtml(d.id) + '" onclick="selectDatasetAndExplore(this.dataset.id)">' +
            'Explore in Table →' +
          '</button>' +
        '</div>' +
      '</div>';
    }).join("");
  } catch (e) {
    grid.innerHTML = '<div style="color:var(--accent-rose);">Error loading datasets: ' + escapeHtml(e.message) + '</div>';
  }
}

function selectDatasetAndExplore(id) {
  const sel = document.getElementById("datasetSelect");
  if (sel) sel.value = id;
  onDatasetChange(id);
  switchTab("leads");
}

async function handleFileUpload(file) {
  if (!file) return;
  const formData = new FormData();
  formData.append("file", file);
  toast("Uploading CSV...");
  try {
    const res = await fetch("/api/upload_dataset", { method: "POST", body: formData });
    const d = await res.json();
    if (!res.ok) throw new Error(d.error || "Upload failed");
    toast("CSV uploaded successfully!");
    await refreshDatasetsList();
    loadDatasetCatalog();
  } catch (err) {
    alert("Upload failed: " + err.message);
  }
}

// Utilities
function copyText(txt, msg) {
  const textToCopy = String(txt || "");
  const feedbackMsg = msg || "Copied to clipboard!";
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(textToCopy).then(function() { toast(feedbackMsg); });
  } else {
    const ta = document.createElement("textarea");
    ta.value = textToCopy;
    ta.style.position = "fixed";
    ta.style.opacity = "0";
    document.body.appendChild(ta);
    ta.focus();
    ta.select();
    try {
      document.execCommand("copy");
      toast(feedbackMsg);
    } catch (e) {
      console.error(e);
    }
    document.body.removeChild(ta);
  }
}

function toast(msg) {
  const el = document.getElementById("toast");
  if (!el) return;
  el.textContent = msg;
  el.style.display = "block";
  clearTimeout(el.timer);
  el.timer = setTimeout(function() { el.style.display = "none"; }, 2500);
}

function toggleTheme() {
  const curr = document.documentElement.getAttribute("data-theme");
  const next = curr === "dark" ? "light" : "dark";
  document.documentElement.setAttribute("data-theme", next);
  const icon = document.getElementById("themeIcon");
  if (icon) icon.textContent = next === "dark" ? "☀️" : "🌙";
  localStorage.setItem("theme", next);
}

function escapeHtml(str) {
  if (!str) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

// Initialize on Load
document.addEventListener("DOMContentLoaded", function() {
  const savedTheme = localStorage.getItem("theme") || "dark";
  document.documentElement.setAttribute("data-theme", savedTheme);
  const icon = document.getElementById("themeIcon");
  if (icon) icon.textContent = savedTheme === "dark" ? "☀️" : "🌙";
  
  const sel = document.getElementById("datasetSelect");
  if (sel) {
    if (sel.value) currentDataset = sel.value;
    if (sel.selectedOptions.length > 0) {
      const opt = sel.selectedOptions[0];
      const lbl = document.getElementById("kpiDatasetLabel");
      if (lbl) lbl.textContent = opt.text;
    }
  }
  
  loadLeads();
});
