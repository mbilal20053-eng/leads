// Lead Engine PRO - Client Application Logic
// State Management
let currentDataset = "all_global";
let currentPage = 1;
let currentPageSize = 50;
let currentSearch = "";
let currentTier = "all";
let currentState = "all";
let currentCountry = "all";
let currentMajorCategory = "all";
let currentCategory = "all";
let currentCrmStatus = "all";
let currentExportFormat = "xlsx";
let selectedLeadIds = new Set();
let activeCategoriesList = [];
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
  document.querySelectorAll(".tab-btn").forEach(function (b) { b.classList.remove("active"); });
  document.querySelectorAll(".tab-panel").forEach(function (p) { p.classList.remove("active"); });

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

  tbody.innerHTML = '<tr><td colspan="14" style="text-align:center;padding:48px 20px;"><div class="skeleton" style="width:260px;margin:0 auto 12px;height:18px;"></div><span style="color:var(--text-dim);font-weight:500;">Loading leads database...</span></td></tr>';
  const metaStatus = document.getElementById("metaStatus");
  if (metaStatus) metaStatus.textContent = "Loading...";

  const catParam = (activeCategoriesList.length > 0) ? activeCategoriesList.join(",") : currentCategory;
  const params = new URLSearchParams({
    dataset: currentDataset,
    page: currentPage,
    page_size: currentPageSize,
    search: currentSearch,
    tier: currentTier,
    state: currentState,
    country: currentCountry,
    major_category: currentMajorCategory,
    category: catParam,
    crm_status: currentCrmStatus,
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

    if (data.sources_breakdown && data.sources_breakdown.length > 0) { window.cachedBreakdown = data.sources_breakdown; }
    renderKPIs(data.stats, data.sources_breakdown || window.cachedBreakdown, data.dataset_name);
    renderTable(data.leads, data.total);
    renderPagination(data.total, data.page, data.page_size);
    if (data.states) updateStatesFilter(data.states);
    if (data.major_categories) updateMajorCategoriesDropdown(data.major_categories);
    if (data.categories_hierarchy) categoriesHierarchyCache = data.categories_hierarchy;
    if (data.categories) updateCategoriesFilter(data.categories);
    updateActiveMajorPill();
    updateActiveCategoryPill();
    if (metaStatus) metaStatus.textContent = "Up to date";
  } catch (err) {
    console.error("Error loading leads:", err);
    tbody.innerHTML = '<tr><td colspan="14" style="text-align:center;padding:40px;color:var(--accent-rose);font-size:14px;">' +
      '<div>⚠️ Error loading leads: ' + escapeHtml(err.message) + '</div>' +
      '<button class="btn btn-secondary" style="margin-top:12px;" onclick="loadLeads()">Try Again</button>' +
      '</td></tr>';
    if (metaStatus) metaStatus.textContent = "Error";
  }
}

function renderKPIs(stats, breakdown, datasetName) {
  if (!stats) return;
  const total = Number(stats.total || 0);
  const tierA = Number(stats.tier_a || 0);
  const tierB = Number(stats.tier_b || 0);
  const phone = Number(stats.with_phone || 0);
  const website = Number(stats.with_website !== undefined ? stats.with_website : Math.max(0, total - Number(stats.no_website || 0)));
  const email = Number(stats.with_email !== undefined ? stats.with_email : 0);

  const kTotal = document.getElementById("kpiTotal");
  const kTierA = document.getElementById("kpiTierA");
  const kTierB = document.getElementById("kpiTierB");
  const kPhone = document.getElementById("kpiWithPhone");
  const kWebsite = document.getElementById("kpiWithWebsite");
  const kEmail = document.getElementById("kpiWithEmail");

  if (kTotal) kTotal.textContent = total.toLocaleString();

  const tierAPct = total > 0 ? Math.min(100, (tierA / total) * 100).toFixed(1) : "0.0";
  const tierBPct = total > 0 ? Math.min(100, (tierB / total) * 100).toFixed(1) : "0.0";
  const phonePct = total > 0 ? Math.min(100, (phone / total) * 100).toFixed(1) : "0.0";
  const websitePct = total > 0 ? Math.min(100, (website / total) * 100).toFixed(1) : "0.0";
  const emailPct = total > 0 ? Math.min(100, (email / total) * 100).toFixed(1) : "0.0";

  if (kPhone) {
    kPhone.innerHTML = phone.toLocaleString() + ' <span style="font-size:12px;font-weight:700;padding:2px 8px;border-radius:12px;background:rgba(99,102,241,0.18);color:#818cf8;border:1px solid rgba(99,102,241,0.35);vertical-align:middle;margin-left:6px;">' + phonePct + '%</span>';
    const sub = document.getElementById("kpiPhoneSub");
    if (sub) sub.textContent = phone.toLocaleString() + ' of ' + total.toLocaleString() + ' leads (' + phonePct + '%)';
    const badge = document.getElementById("kpiPhoneBadge");
    if (badge) badge.textContent = phonePct + "% REACH";
  }

  if (kWebsite) {
    kWebsite.innerHTML = website.toLocaleString() + ' <span style="font-size:12px;font-weight:700;padding:2px 8px;border-radius:12px;background:rgba(6,182,212,0.18);color:#22d3ee;border:1px solid rgba(6,182,212,0.35);vertical-align:middle;margin-left:6px;">' + websitePct + '%</span>';
    const sub = document.getElementById("kpiWebsiteSub");
    if (sub) sub.textContent = website.toLocaleString() + ' of ' + total.toLocaleString() + ' leads (' + websitePct + '%)';
    const badge = document.getElementById("kpiWebsiteBadge");
    if (badge) badge.textContent = websitePct + "% SITES";
  }

  if (kEmail) {
    kEmail.innerHTML = email.toLocaleString() + ' <span style="font-size:12px;font-weight:700;padding:2px 8px;border-radius:12px;background:rgba(16,185,129,0.18);color:#34d399;border:1px solid rgba(16,185,129,0.35);vertical-align:middle;margin-left:6px;">' + emailPct + '%</span>';
    const sub = document.getElementById("kpiEmailSub");
    if (sub) sub.textContent = email.toLocaleString() + ' of ' + total.toLocaleString() + ' leads (' + emailPct + '%)';
    const badge = document.getElementById("kpiEmailBadge");
    if (badge) badge.textContent = emailPct + "% INBOX";
  }

  if (kTierA) {
    kTierA.innerHTML = tierA.toLocaleString() + ' <span style="font-size:12px;font-weight:700;padding:2px 8px;border-radius:12px;background:rgba(16,185,129,0.18);color:#34d399;border:1px solid rgba(16,185,129,0.35);vertical-align:middle;margin-left:6px;">' + tierAPct + '%</span>';
  }
  if (kTierB) {
    kTierB.innerHTML = tierB.toLocaleString() + ' <span style="font-size:12px;font-weight:700;padding:2px 8px;border-radius:12px;background:rgba(245,158,11,0.18);color:#fbbf24;border:1px solid rgba(245,158,11,0.35);vertical-align:middle;margin-left:6px;">' + tierBPct + '%</span>';
  }

  // Update table header meta badges if present
  const metaPhoneCoverage = document.getElementById("metaPhoneCoverage");
  if (metaPhoneCoverage) metaPhoneCoverage.textContent = phonePct + "%";
  const metaWebsiteCoverage = document.getElementById("metaWebsiteCoverage");
  if (metaWebsiteCoverage) metaWebsiteCoverage.textContent = websitePct + "%";
  const metaEmailCoverage = document.getElementById("metaEmailCoverage");
  if (metaEmailCoverage) metaEmailCoverage.textContent = emailPct + "%";

  // Update banner total count to exact number of current filtered source!
  const bannerTotal = document.getElementById("bannerTotalCount");
  if (bannerTotal) bannerTotal.textContent = total.toLocaleString();

  const kDatasetLabel = document.getElementById("kpiDatasetLabel");
  if (kDatasetLabel) {
    if (datasetName) {
      kDatasetLabel.textContent = datasetName;
    } else {
      const activeChip = document.querySelector(".source-chip.active");
      kDatasetLabel.textContent = activeChip ? activeChip.innerText.trim() : currentDataset;
    }
  }

  const metaCount = document.getElementById("metaCount");
  if (metaCount) metaCount.textContent = total.toLocaleString();

  const bannerShare = document.getElementById("bannerSharePct");
  if (bannerShare) {
    if (currentDataset === "all_global") {
      bannerShare.textContent = "100% (All Sources - 215.7M Leads)";
    } else if (breakdown) {
      const item = breakdown.find(function (b) { return b.id === currentDataset; });
      if (item) {
        bannerShare.textContent = item.pct + "% of Total (" + Number(item.count).toLocaleString() + " leads)";
      }
    }
  }

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
  currentSearch = "";
  const sInput = document.getElementById("searchInput");
  if (sInput) sInput.value = "";

  // 1. Immediately highlight clicked chip visually
  document.querySelectorAll(".source-chip").forEach(function (b) {
    b.classList.remove("active");
  });
  const chips = document.querySelectorAll(".source-chip");
  for (let i = 0; i < chips.length; i++) {
    const attr = chips[i].getAttribute("onclick");
    if (attr && attr.indexOf("'" + id + "'") !== -1) {
      chips[i].classList.add("active");
      break;
    }
  }

  // 2. Sync with dataset select dropdown
  const sel = document.getElementById("datasetSelect");
  if (sel) {
    let opt = sel.querySelector("option[value='" + id + "']");
    if (!opt) {
      opt = document.createElement("option");
      opt.value = id;
      opt.textContent = id;
      sel.appendChild(opt);
    }
    sel.value = id;
  }

  // 3. Immediately display skeleton in table
  const tbody = document.getElementById("leadsTbody");
  if (tbody) {
    tbody.innerHTML = '<tr><td colspan="14" style="text-align:center;padding:48px 20px;"><div class="skeleton" style="width:260px;margin:0 auto 12px;height:18px;"></div><span style="color:var(--text-dim);font-weight:500;">Loading ' + escapeHtml(id) + ' leads database...</span></td></tr>';
  }

  // 4. Fetch the leads for this source
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
    tbody.innerHTML = '<tr><td colspan="14" style="text-align:center;padding:60px 20px;color:var(--text-dim);font-size:14px;">' +
      '<div style="font-size:32px;margin-bottom:12px;">🔍</div>' +
      '<div>No matching leads found for current search/filters.</div>' +
      '<button class="btn btn-secondary" style="margin-top:14px;" onclick="resetFilters()">Reset All Filters</button>' +
      '</td></tr>';
    syncMasterCheckbox();
    updateBulkActionBar();
    return;
  }

  const freeWebmails = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "aol.com", "icloud.com", "mail.com", "zoho.com", "protonmail.com", "yandex.com", "gmx.com", "live.com"];
  let rowsHtml = "";
  for (let idx = 0; idx < leads.length; idx++) {
    const lead = leads[idx];
    const safeId = String(lead.id || ("lead_" + idx));
    window.leadDataMap[safeId] = lead;

    const rowNum = (currentPage - 1) * currentPageSize + idx + 1;
    const isChecked = selectedLeadIds.has(safeId) ? ' checked' : '';
    const checkboxHtml = '<input type="checkbox" class="lead-checkbox lead-row-checkbox" data-id="' + safeId + '" onchange="onLeadCheckChange(\'' + safeId + '\', this.checked)"' + isChecked + '>';

    // 1. Business Name
    let bizNameHtml = '<span class="empty-box">-</span>';
    if (lead.name && String(lead.name).trim() && String(lead.name) !== "None") {
      const nm = String(lead.name).trim();
      const badgeHtml = lead.source_badge ? ' <span style="font-size:10px;font-weight:600;opacity:0.85;background:' + (lead.source_color || '#3b82f6') + '20;color:' + (lead.source_color || '#3b82f6') + ';padding:1px 6px;border-radius:10px;margin-left:4px;">' + escapeHtml(lead.source_badge) + '</span>' : '';
      bizNameHtml = '<div class="biz-name" title="' + escapeHtml(nm) + '">' + escapeHtml(nm) + badgeHtml + '</div>';
    }

    // 2. Category (Major Category + Minor Category)
    let catHtml = '<span class="empty-box">-</span>';
    const catVal = (lead.category && String(lead.category).trim() && String(lead.category) !== "None") ? String(lead.category).trim() : "";
    const majorVal = (lead.major_category && String(lead.major_category).trim() && String(lead.major_category) !== "None") ? String(lead.major_category).trim() : "";
    const majorIcon = lead.major_icon || "🏢";
    const majorId = lead.major_id || "";

    if (catVal || majorVal) {
      let parts = '<div class="table-category-cell">';
      if (majorVal) {
        parts += '<span class="table-major-badge" title="Filter by Major Group: ' + escapeHtml(majorVal) + '" onclick="event.stopPropagation(); filterByMajorCategory(\'' + escapeHtml(majorId || majorVal).replace(/'/g, "\\'") + '\')">' + majorIcon + ' ' + escapeHtml(majorVal) + '</span>';
      }
      if (catVal && catVal.toLowerCase() !== majorVal.toLowerCase()) {
        parts += '<span class="table-cat-pill" title="Add Minor Category Filter: ' + escapeHtml(catVal) + '" onclick="event.stopPropagation(); addCategoryTag(\'' + escapeHtml(catVal).replace(/'/g, "\\'") + '\')">🏷️ ' + escapeHtml(catVal) + '</span>';
      } else if (!majorVal && catVal) {
        parts += '<span class="table-cat-pill" title="Add Minor Category Filter: ' + escapeHtml(catVal) + '" onclick="event.stopPropagation(); addCategoryTag(\'' + escapeHtml(catVal).replace(/'/g, "\\'") + '\')">🏷️ ' + escapeHtml(catVal) + '</span>';
      }
      parts += '</div>';
      catHtml = parts;
    }

    // 3. Owner / Contact
    let contactHtml = '<span class="empty-box">-</span>';
    if (lead.contact_name && String(lead.contact_name).trim() && String(lead.contact_name) !== "None") {
      contactHtml = '<div class="contact-name" title="' + escapeHtml(lead.contact_name) + '"><b>' + escapeHtml(lead.contact_name) + '</b></div>';
    }

    // 4. Role & Notes
    let roleHtml = '<span class="empty-box">-</span>';
    const roleVal = lead.job_title || lead.notes || "";
    if (roleVal && String(roleVal).trim() && String(roleVal) !== "None") {
      roleHtml = '<div class="role-text" title="' + escapeHtml(roleVal) + '">' + escapeHtml(roleVal) + '</div>';
    }

    // 5. Email + Deliverability Badge
    let emailHtml = '<span class="empty-box">-</span>';
    if (lead.email && String(lead.email).trim() && String(lead.email).indexOf("@") !== -1 && String(lead.email) !== "None") {
      const em = String(lead.email).trim();
      const emDomain = (em.split("@")[1] || "").toLowerCase();
      const isFree = freeWebmails.indexOf(emDomain) !== -1;
      const deliverBadge = isFree
        ? '<span class="badge-webmail" title="Free Webmail Provider (gmail/yahoo/etc)">📧 Webmail</span>'
        : '<span class="badge-corp-mail" title="Verified Corporate Domain: High Value Deliverability">🏢 Corporate</span>';
      emailHtml = '<div style="display:flex;align-items:center;gap:4px;flex-wrap:wrap;">' +
        '<a href="mailto:' + escapeHtml(em) + '" class="email-link" title="' + escapeHtml(em) + '">✉️ ' + escapeHtml(em) + '</a>' +
        deliverBadge +
        '<button class="copy-cell-btn" data-val="' + escapeHtml(em) + '" onclick="copyDirectVal(this.dataset.val, \'Email copied!\')" title="Copy email">📋</button>' +
        '</div>';
    }

    // 6. Phone + Direct Dial Badge
    let phoneHtml = '<span class="empty-box">-</span>';
    if (lead.phone && String(lead.phone).trim() && String(lead.phone) !== "None") {
      const ph = String(lead.phone).trim();
      phoneHtml = '<div style="display:flex;align-items:center;gap:4px;flex-wrap:wrap;">' +
        '<a href="tel:' + escapeHtml(ph) + '" class="phone-link" title="' + escapeHtml(ph) + '">📞 ' + escapeHtml(ph) + '</a>' +
        '<span class="badge-direct-dial" title="Direct Phone Line Available">Direct</span>' +
        '<button class="copy-cell-btn" data-val="' + escapeHtml(ph) + '" onclick="copyDirectVal(this.dataset.val, \'Phone copied!\')" title="Copy phone">📋</button>' +
        '</div>';
    }

    // 7. Website
    let webHtml = '<span class="empty-box">-</span>';
    if (lead.website && String(lead.website).indexOf("None") === -1 && String(lead.website).trim() !== "") {
      const rawWeb = String(lead.website).trim();
      const url = rawWeb.indexOf("http") === 0 ? rawWeb : "https://" + rawWeb;
      webHtml = '<a href="' + escapeHtml(url) + '" target="_blank" rel="noopener noreferrer" class="web-badge has-site" title="' + escapeHtml(url) + '">🌐 Visit</a>';
    }

    // 8. Address
    let addrHtml = '<span class="empty-box">-</span>';
    if (lead.address && String(lead.address).trim() && String(lead.address) !== "None") {
      addrHtml = '<div class="cell-text" title="' + escapeHtml(lead.address) + '">' + escapeHtml(lead.address) + '</div>';
    }

    // 9. City
    let cityHtml = '<span class="empty-box">-</span>';
    if (lead.city && String(lead.city).trim() && String(lead.city) !== "None") {
      cityHtml = '<span class="cell-text" title="' + escapeHtml(lead.city) + '">' + escapeHtml(lead.city) + '</span>';
    }

    // 10. State / Region
    let stateHtml = '<span class="empty-box">-</span>';
    if (lead.state && String(lead.state).trim() && String(lead.state) !== "None") {
      stateHtml = '<span class="cell-text" title="' + escapeHtml(lead.state) + '">' + escapeHtml(lead.state) + '</span>';
    }

    // 11. Country
    let countryHtml = '<span class="empty-box">-</span>';
    const ctry = lead.country || (lead.city || lead.state ? "United States" : "");
    if (ctry && String(ctry).trim() && String(ctry) !== "None") {
      countryHtml = '<span class="cell-text" title="' + escapeHtml(ctry) + '">' + escapeHtml(ctry) + '</span>';
    }

    // 12. Socials
    let socialsHtml = '<span class="empty-box">-</span>';
    if (lead.socials && String(lead.socials).trim() && String(lead.socials).indexOf("None") === -1) {
      const rawSoc = String(lead.socials).trim();
      const socUrl = rawSoc.indexOf("http") === 0 ? rawSoc : "https://" + rawSoc;
      socialsHtml = '<a href="' + escapeHtml(socUrl) + '" target="_blank" rel="noopener noreferrer" class="social-badge" title="' + escapeHtml(socUrl) + '">🔗 LinkedIn</a>';
    }

    // 13. Actions
    const actionHtml = '<button class="btn btn-secondary" style="padding:4px 10px;font-size:11px;" data-id="' + safeId + '" onclick="openDrawerById(this.dataset.id)">View</button>';

    rowsHtml += '<tr id="row_' + safeId + '">' +
      '<td style="text-align:center;">' + checkboxHtml + '</td>' +
      '<td style="color:var(--text-dim);font-size:12px;text-align:center;">' + rowNum + '</td>' +
      '<td>' + bizNameHtml + '</td>' +
      '<td>' + catHtml + '</td>' +
      '<td>' + contactHtml + '</td>' +
      '<td>' + roleHtml + '</td>' +
      '<td>' + emailHtml + '</td>' +
      '<td>' + phoneHtml + '</td>' +
      '<td>' + webHtml + '</td>' +
      '<td>' + addrHtml + '</td>' +
      '<td>' + cityHtml + '</td>' +
      '<td>' + stateHtml + '</td>' +
      '<td>' + countryHtml + '</td>' +
      '<td>' + socialsHtml + '</td>' +
      '<td style="text-align:center;">' + actionHtml + '</td>' +
      '</tr>';
  }
  tbody.innerHTML = rowsHtml;
  syncMasterCheckbox();
  updateBulkActionBar();
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

let allCategoriesCache = [];
let categoriesHierarchyCache = [];
let majorCategoriesCache = [];

function updateMajorCategoriesDropdown(majors) {
  if (!majors || majors.length === 0) return;
  majorCategoriesCache = majors;
  const select = document.getElementById("majorCatFilter");
  if (select) {
    const curr = currentMajorCategory || "all";
    let html = '<option value="all">🏢 All Major Groups (' + majors.length + ')</option>';
    for (let i = 0; i < majors.length; i++) {
      const m = majors[i];
      const isSel = (m.id.toLowerCase() === curr.toLowerCase() || m.name.toLowerCase() === curr.toLowerCase());
      html += '<option value="' + escapeHtml(m.id) + '"' + (isSel ? ' selected' : '') + '>' + (m.icon ? m.icon + ' ' : '') + escapeHtml(m.name) + '</option>';
    }
    select.innerHTML = html;
  }
}

function updateCategoriesFilter(categories) {
  if (!categories || categories.length === 0) return;
  allCategoriesCache = categories;
  updateMinorCategoryDropdown();

  const browseBtn = document.getElementById("browseCategoriesBtn");
  if (browseBtn) {
    const textEl = browseBtn.querySelector(".browse-btn-text");
    if (textEl) textEl.textContent = 'Browse All (' + categories.length + ')';
  }

  updateActiveCategoryPill();
  updateActiveMajorPill();
}

function updateMinorCategoryDropdown() {
  const select = document.getElementById("catFilter");
  if (!select) return;

  let cats = allCategoriesCache;
  if (currentMajorCategory && currentMajorCategory !== "all") {
    const normM = currentMajorCategory.toLowerCase();
    cats = allCategoriesCache.filter(function (c) {
      const mid = (c.major_id || "").toLowerCase();
      const mname = (c.major_name || "").toLowerCase();
      return mid === normM || mname === normM;
    });
  }

  const curr = currentCategory || "all";
  let title = currentMajorCategory !== "all"
    ? '🏷️ All in Selected Major (' + cats.length + ' Minors)'
    : '🏷️ All Categories (' + allCategoriesCache.length + ' Verticals)';

  let html = '<option value="all">' + escapeHtml(title) + '</option>';
  for (let i = 0; i < cats.length; i++) {
    const c = cats[i];
    const val = typeof c === 'object' ? c.id : c;
    const countSuffix = typeof c === 'object' ? ' (' + (c.badge || c.count_str) + ')' : '';
    const label = typeof c === 'object' ? c.label : c;
    const isSel = (val === curr || (curr !== "all" && val.toLowerCase() === curr.toLowerCase()));
    html += '<option value="' + escapeHtml(val) + '"' + (isSel ? ' selected' : '') + '>' + escapeHtml(label + countSuffix) + '</option>';
  }
  select.innerHTML = html;
}

function onMajorCatChange(val) {
  filterByMajorCategory(val);
}

function filterByMajorCategory(val) {
  currentMajorCategory = val || "all";
  currentPage = 1;

  const select = document.getElementById("majorCatFilter");
  if (select) {
    select.value = currentMajorCategory;
  }

  // Update minor categories dropdown to reflect this major category
  updateMinorCategoryDropdown();
  updateActiveMajorPill();
  loadLeads();
}

function clearMajorCategoryFilter() {
  filterByMajorCategory("all");
}

function updateActiveMajorPill() {
  const pill = document.getElementById("activeMajorPill");
  const text = document.getElementById("activeMajorText");
  if (!pill) return;

  if (currentMajorCategory && currentMajorCategory !== "all") {
    let displayName = currentMajorCategory;
    const found = majorCategoriesCache.find(function (m) {
      return m.id.toLowerCase() === currentMajorCategory.toLowerCase() || m.name.toLowerCase() === currentMajorCategory.toLowerCase();
    });
    if (found) {
      displayName = (found.icon ? found.icon + " " : "") + found.name;
    }
    if (text) text.textContent = displayName;
    pill.style.display = "inline-flex";
  } else {
    pill.style.display = "none";
  }
}

function updateActiveCategoryPill() {
  const pill = document.getElementById("activeCatPill");
  const text = document.getElementById("activeCatText");
  if (!pill) return;

  if (currentCategory && currentCategory !== "all") {
    let displayName = currentCategory;
    const found = allCategoriesCache.find(function (c) {
      const id = typeof c === 'object' ? c.id.toLowerCase() : c.toLowerCase();
      return id === currentCategory.toLowerCase();
    });
    if (found && typeof found === 'object') {
      displayName = found.label;
    }
    if (text) text.textContent = displayName;
    pill.style.display = "inline-flex";
  } else {
    pill.style.display = "none";
  }
}

function applyCustomCategoryInput() {
  const inp = document.getElementById("catQuickAddInput");
  if (!inp) return;
  const val = inp.value.trim();
  if (!val) {
    filterByCategory("all");
    return;
  }
  filterByCategory(val);
}

function filterByCategory(val) {
  currentCategory = val || "all";
  currentPage = 1;

  const inp = document.getElementById("catQuickAddInput");
  if (inp) {
    inp.value = (val === "all" ? "" : val);
  }

  const select = document.getElementById("catFilter");
  if (select) {
    if (val === "all") {
      select.value = "all";
    } else {
      let matched = false;
      for (let i = 0; i < select.options.length; i++) {
        if (select.options[i].value.toLowerCase() === val.toLowerCase()) {
          select.selectedIndex = i;
          matched = true;
          break;
        }
      }
      if (!matched) {
        const opt = document.createElement("option");
        opt.value = val;
        opt.textContent = "🏷️ " + val + " (Active Filter)";
        opt.selected = true;
        select.appendChild(opt);
      }
    }
  }

  // If minor category belongs to a major category, sync it if needed
  if (val !== "all") {
    const norm = val.toLowerCase();
    const found = allCategoriesCache.find(function (c) {
      return (typeof c === 'object' && c.id && c.id.toLowerCase() === norm);
    });
    if (found && found.major_id && currentMajorCategory !== "all" && currentMajorCategory !== found.major_id) {
      currentMajorCategory = found.major_id;
      const mSel = document.getElementById("majorCatFilter");
      if (mSel) mSel.value = currentMajorCategory;
      updateActiveMajorPill();
    }
  }

  updateActiveCategoryPill();
  loadLeads();
}

function clearCategoryFilter() {
  filterByCategory("all");
}

function onCatChange(val) {
  filterByCategory(val);
}

function resetAllCategoryFilters() {
  currentMajorCategory = "all";
  currentCategory = "all";
  const mSel = document.getElementById("majorCatFilter"); if (mSel) mSel.value = "all";
  const cSel = document.getElementById("catFilter"); if (cSel) cSel.value = "all";
  const cInp = document.getElementById("catQuickAddInput"); if (cInp) cInp.value = "";
  updateMinorCategoryDropdown();
  updateActiveMajorPill();
  updateActiveCategoryPill();
  loadLeads();
}

// Categories Browser Modal
function openCategoriesModal() {
  const modal = document.getElementById("categoriesModal");
  if (!modal) return;
  modal.style.display = "flex";

  const pills = document.querySelectorAll("#catQuickPills .cat-quick-pill");
  pills.forEach(function (p, i) { p.classList.toggle("active", i === 0); });

  renderCategoriesHierarchyInModal(categoriesHierarchyCache);
  const searchInput = document.getElementById("catModalSearch");
  if (searchInput) {
    searchInput.value = "";
    setTimeout(function () { searchInput.focus(); }, 80);
  }
}

function closeCategoriesModal() {
  const modal = document.getElementById("categoriesModal");
  if (modal) modal.style.display = "none";
}

function clearCatModalSearch() {
  const searchInput = document.getElementById("catModalSearch");
  if (searchInput) {
    searchInput.value = "";
    renderCategoriesHierarchyInModal(categoriesHierarchyCache);
    searchInput.focus();
  }
}

function filterCategoriesInModal(query) {
  if (!query) {
    renderCategoriesHierarchyInModal(categoriesHierarchyCache);
    return;
  }
  const q = query.toLowerCase().trim();

  // Filter hierarchy by checking minor categories or major names
  const filtered = [];
  for (let i = 0; i < categoriesHierarchyCache.length; i++) {
    const node = categoriesHierarchyCache[i];
    const majorMatches = (node.name.toLowerCase().indexOf(q) !== -1 || node.id.toLowerCase().indexOf(q) !== -1);
    const matchingMinors = (node.minors || []).filter(function (c) {
      const id = typeof c === 'object' ? c.id.toLowerCase() : c.toLowerCase();
      const lbl = typeof c === 'object' ? c.label.toLowerCase() : c.toLowerCase();
      return id.indexOf(q) !== -1 || lbl.indexOf(q) !== -1;
    });

    if (majorMatches || matchingMinors.length > 0) {
      filtered.push({
        ...node,
        minors: majorMatches && matchingMinors.length === 0 ? node.minors : matchingMinors
      });
    }
  }
  renderCategoriesHierarchyInModal(filtered, q);
}

function quickFilterMajorModal(majorId) {
  const pills = document.querySelectorAll("#catQuickPills .cat-quick-pill");
  pills.forEach(function (p) { p.classList.remove("active"); });
  if (window.event && window.event.target) {
    window.event.target.classList.add("active");
  }

  const searchInput = document.getElementById("catModalSearch");
  if (searchInput) searchInput.value = "";

  if (majorId === 'all') {
    renderCategoriesHierarchyInModal(categoriesHierarchyCache);
  } else {
    const filtered = categoriesHierarchyCache.filter(function (m) {
      return m.id.toLowerCase() === majorId.toLowerCase();
    });
    renderCategoriesHierarchyInModal(filtered);
  }
}

function selectCategoryFromModal(val) {
  filterByCategory(val);
  closeCategoriesModal();
}

function selectMajorFromModal(val) {
  filterByMajorCategory(val);
  closeCategoriesModal();
}

function renderCategoriesHierarchyInModal(hierarchyList, searchQuery) {
  const grid = document.getElementById("categoriesGrid");
  const countEl = document.getElementById("catResultsCount");
  if (!grid) return;

  const nodes = hierarchyList || [];
  let totalMinors = 0;
  for (let i = 0; i < nodes.length; i++) {
    totalMinors += (nodes[i].minors ? nodes[i].minors.length : 0);
  }

  if (countEl) {
    if (searchQuery) {
      countEl.textContent = 'Found ' + totalMinors + ' minor categories matching "' + searchQuery + '" across ' + nodes.length + ' Major Groups';
    } else {
      countEl.textContent = 'Showing ' + nodes.length + ' Major Groups with ' + totalMinors + ' Minor Verticals';
    }
  }

  if (nodes.length === 0 || totalMinors === 0) {
    grid.innerHTML = '<div class="no-categories-found">No categories matching your search. Try searching for "hotel", "cafe", "restaurant", "health", "tech", or "construction".</div>';
    return;
  }

  let html = '';
  for (let i = 0; i < nodes.length; i++) {
    const node = nodes[i];
    const isMajorActive = (currentMajorCategory && (currentMajorCategory.toLowerCase() === node.id.toLowerCase() || currentMajorCategory.toLowerCase() === node.name.toLowerCase()));
    const minors = node.minors || [];

    html += '<div class="major-cat-section">' +
      '<div class="major-section-header">' +
      '<div class="major-section-title" onclick="selectMajorFromModal(\'' + escapeHtml(node.id).replace(/'/g, "\\'") + '\')">' +
      '<span style="font-size:18px;">' + (node.icon || '🏢') + '</span>' +
      '<span>' + escapeHtml(node.name) + '</span>' +
      '<span class="major-section-badge">' + (node.badge || node.total_count_str) + ' leads</span>' +
      '</div>' +
      '<button type="button" class="major-filter-btn" onclick="selectMajorFromModal(\'' + escapeHtml(node.id).replace(/'/g, "\\'") + '\')">' +
      (isMajorActive ? '✓ Group Active' : 'Filter Major Group →') +
      '</button>' +
      '</div>' +
      '<div class="minor-chips-grid">';

    for (let j = 0; j < minors.length; j++) {
      const c = minors[j];
      const val = typeof c === 'object' ? c.id : c;
      const label = typeof c === 'object' ? c.label : c;
      const countBadge = typeof c === 'object' ? (c.badge || c.count_str) : '';
      const isMinorActive = (val === currentCategory || (currentCategory !== 'all' && val.toLowerCase() === currentCategory.toLowerCase()));

      html += '<div class="minor-chip ' + (isMinorActive ? 'active' : '') + '" onclick="selectCategoryFromModal(\'' + escapeHtml(val).replace(/'/g, "\\'") + '\')" title="Filter leads by ' + escapeHtml(label) + '">' +
        '<span>' + escapeHtml(label) + '</span>' +
        (countBadge ? '<span class="minor-chip-count">' + escapeHtml(countBadge) + '</span>' : '') +
        '</div>';
    }

    html += '</div></div>';
  }

  grid.innerHTML = html;
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
  searchTimer = setTimeout(function () {
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
  document.querySelectorAll(".tier-pill-btn").forEach(function (b) {
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

function onCountryChange(val) {
  currentCountry = val || "all";
  currentPage = 1;
  const cSel = document.getElementById("countryFilter");
  if (cSel) cSel.value = currentCountry;
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
  currentCountry = "all";
  const cSel = document.getElementById("countryFilter"); if (cSel) cSel.value = "all";
  currentMajorCategory = "all";
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

  document.querySelectorAll(".tier-pill-btn").forEach(function (b) {
    b.classList.toggle("active", b.getAttribute("data-tier") === "all");
  });

  const phoneBtn = document.getElementById("hasPhoneToggle");
  if (phoneBtn) phoneBtn.classList.remove("active");

  const stateSel = document.getElementById("stateFilter");
  if (stateSel) stateSel.value = "all";

  const majorSel = document.getElementById("majorCatFilter");
  if (majorSel) majorSel.value = "all";

  const catSel = document.getElementById("catFilter");
  if (catSel) catSel.value = "all";
  const catInp = document.getElementById("catQuickAddInput");
  if (catInp) catInp.value = "";

  const oppSel = document.getElementById("oppFilter");
  if (oppSel) oppSel.value = "all";

  updateMinorCategoryDropdown();
  updateActiveMajorPill();
  updateActiveCategoryPill();
  loadLeads();
}

function copyDirectVal(val, msg) {
  if (val) copyText(val, msg || "Copied to clipboard!");
}

// Slide-Out Drawer
function openDrawer(lead) {
  activeLead = lead;

  document.getElementById("drawerName").textContent = lead.name || "Unknown Business";
  const catEl = document.getElementById("drawerCat");
  if (catEl) {
    const cName = lead.category || "General Business";
    catEl.textContent = cName;
    catEl.title = "Click to filter leads by " + cName;
    catEl.style.cursor = "pointer";
    catEl.onclick = function () {
      if (lead.category) {
        filterByCategory(lead.category);
        closeDrawer();
      }
    };
  }

  const tierBadge = document.getElementById("drawerTier");
  if (tierBadge) {
    tierBadge.textContent = "Tier " + (lead.tier || "A");
    tierBadge.className = "tier-badge tier-" + (lead.tier || "A");
  }

  document.getElementById("drawerPitch").textContent = lead.pitch || "No pitch script available.";
  document.getElementById("drawerWhy").textContent = lead.why || "Active business lead identified.";

  // Populate the 11 Verified Columns in Drawer
  const setDrawerFld = function (id, valHtml) {
    const el = document.getElementById(id);
    if (el) el.innerHTML = valHtml || '<span class="empty-box">-</span>';
  };

  setDrawerFld("drawerBizName", lead.name ? escapeHtml(lead.name) : "");
  setDrawerFld("drawerContact", lead.contact_name ? escapeHtml(lead.contact_name) : "");
  setDrawerFld("drawerRoleNotes", (lead.job_title || lead.notes) ? escapeHtml(lead.job_title || lead.notes) : "");

  let emVal = "";
  if (lead.email && String(lead.email).trim() && String(lead.email).indexOf("@") !== -1 && String(lead.email) !== "None") {
    emVal = '<a href="mailto:' + escapeHtml(lead.email) + '" style="color:var(--accent-blue);font-family:var(--font-mono);">' + escapeHtml(lead.email) + '</a>';
  }
  setDrawerFld("drawerEmail", emVal);

  let phVal = "";
  if (lead.phone && String(lead.phone).trim() && String(lead.phone) !== "None") {
    phVal = '<a href="tel:' + escapeHtml(lead.phone) + '" style="color:var(--accent-emerald);font-family:var(--font-mono);">' + escapeHtml(lead.phone) + '</a>';
  }
  setDrawerFld("drawerPhone", phVal);

  let webVal = "";
  if (lead.website && String(lead.website).indexOf("None") === -1 && String(lead.website).trim() !== "") {
    const url = lead.website.indexOf("http") === 0 ? lead.website : "https://" + lead.website;
    webVal = '<a href="' + escapeHtml(url) + '" target="_blank" style="color:var(--accent-blue);">🌐 ' + escapeHtml(lead.website) + '</a>';
  }
  setDrawerFld("drawerWebsite", webVal);

  setDrawerFld("drawerAddress", lead.address ? escapeHtml(lead.address) : "");
  setDrawerFld("drawerCity", lead.city ? escapeHtml(lead.city) : "");
  setDrawerFld("drawerState", lead.state ? escapeHtml(lead.state) : "");
  setDrawerFld("drawerCountry", (lead.country || (lead.city || lead.state ? "United States" : "")) ? escapeHtml(lead.country || "United States") : "");

  let socVal = "";
  if (lead.socials && String(lead.socials).trim() && String(lead.socials).indexOf("None") === -1) {
    const socUrl = lead.socials.indexOf("http") === 0 ? lead.socials : "https://" + lead.socials;
    socVal = '<a href="' + escapeHtml(socUrl) + '" target="_blank" class="social-badge">🔗 ' + escapeHtml(lead.socials) + '</a>';
  }
  setDrawerFld("drawerSocials", socVal);

  const callBtn = document.getElementById("drawerCallBtn");
  if (callBtn) {
    if (lead.phone) {
      callBtn.href = "tel:" + lead.phone;
      callBtn.style.display = "inline-flex";
    } else {
      callBtn.style.display = "none";
    }
  }

  const emailBtn = document.getElementById("drawerEmailBtn");
  if (emailBtn) {
    if (lead.email) {
      emailBtn.href = "mailto:" + lead.email;
      emailBtn.style.display = "inline-flex";
    } else {
      emailBtn.style.display = "none";
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

// ==================== Pipeline Status & Multi-Category Filters ====================
function onPipelineStatusChange(status) {
  currentCrmStatus = status || "all";
  currentPage = 1;
  loadLeads();
}

function addCategoryTag(catName) {
  if (!catName || catName.toLowerCase() === "all") return;
  const clean = catName.trim();
  if (!activeCategoriesList.includes(clean)) {
    activeCategoriesList.push(clean);
  }
  currentCategory = "all";
  const catSel = document.getElementById("catFilter");
  if (catSel) catSel.value = "all";
  renderActiveCategoryTags();
  currentPage = 1;
  loadLeads();
}

function removeCategoryTag(catName) {
  activeCategoriesList = activeCategoriesList.filter(function (c) { return c !== catName; });
  renderActiveCategoryTags();
  currentPage = 1;
  loadLeads();
}

function clearAllCategoryTags() {
  activeCategoriesList = [];
  renderActiveCategoryTags();
  currentPage = 1;
  loadLeads();
}

function renderActiveCategoryTags() {
  const container = document.getElementById("activeCatTagsRow");
  if (!container) return;
  if (activeCategoriesList.length === 0) {
    container.style.display = "none";
    container.innerHTML = "";
    return;
  }
  container.style.display = "flex";
  let html = '<span style="font-size:11px;font-weight:700;color:var(--text-dim);margin-right:4px;">Active Tags (' + activeCategoriesList.length + '):</span>';
  for (let i = 0; i < activeCategoriesList.length; i++) {
    const cat = activeCategoriesList[i];
    html += '<span class="cat-tag-chip">' +
      '<span>🏷️ ' + escapeHtml(cat) + '</span>' +
      '<span class="cat-tag-chip-x" onclick="removeCategoryTag(\'' + escapeHtml(cat).replace(/'/g, "\\'") + '\')" title="Remove ' + escapeHtml(cat) + '">✕</span>' +
      '</span>';
  }
  html += '<button type="button" class="btn btn-secondary" style="padding:2px 8px;font-size:11px;border-radius:12px;margin-left:6px;" onclick="clearAllCategoryTags()">Clear All Tags</button>';
  container.innerHTML = html;
}

// ==================== Checkbox Selection & Bulk Actions ====================
function toggleSelectAllRows(checked) {
  const checkboxes = document.querySelectorAll(".lead-row-checkbox");
  checkboxes.forEach(function (cb) {
    cb.checked = checked;
    const lid = cb.dataset.id;
    if (checked) {
      selectedLeadIds.add(lid);
    } else {
      selectedLeadIds.delete(lid);
    }
  });
  updateBulkActionBar();
}

function onLeadCheckChange(lid, checked) {
  if (checked) {
    selectedLeadIds.add(lid);
  } else {
    selectedLeadIds.delete(lid);
  }
  syncMasterCheckbox();
  updateBulkActionBar();
}

function syncMasterCheckbox() {
  const master = document.getElementById("selectAllCheckbox");
  if (!master) return;
  const checkboxes = document.querySelectorAll(".lead-row-checkbox");
  if (checkboxes.length === 0) {
    master.checked = false;
    return;
  }
  let allChecked = true;
  checkboxes.forEach(function (cb) {
    if (!cb.checked) allChecked = false;
  });
  master.checked = allChecked;
}

function updateBulkActionBar() {
  const bar = document.getElementById("bulkActionBar");
  const countBadge = document.getElementById("bulkCountBadge");
  if (!bar) return;
  const count = selectedLeadIds.size;
  if (count > 0) {
    if (countBadge) countBadge.textContent = count.toLocaleString();
    bar.classList.add("visible");
  } else {
    bar.classList.remove("visible");
  }
}

function clearSelection() {
  selectedLeadIds.clear();
  document.querySelectorAll(".lead-row-checkbox").forEach(function (cb) { cb.checked = false; });
  const master = document.getElementById("selectAllCheckbox");
  if (master) master.checked = false;
  updateBulkActionBar();
}

function getSelectedLeadObjects() {
  const list = [];
  selectedLeadIds.forEach(function (lid) {
    const l = window.leadDataMap[lid];
    if (l) list.push(l);
  });
  return list;
}

function copySelectedEmails() {
  const leads = getSelectedLeadObjects();
  const emails = leads.map(function (l) { return (l.email || "").trim(); }).filter(function (e) { return e && e.indexOf("@") !== -1 && e !== "None"; });
  if (emails.length === 0) {
    toast("No valid emails found among selected leads");
    return;
  }
  const text = emails.join(", ");
  copyText(text, "Copied " + emails.length + " selected emails to clipboard!");
}

function copySelectedPhones() {
  const leads = getSelectedLeadObjects();
  const phones = leads.map(function (l) { return (l.phone || "").trim(); }).filter(function (p) { return p && p !== "None"; });
  if (phones.length === 0) {
    toast("No phone numbers found among selected leads");
    return;
  }
  const text = phones.join(", ");
  copyText(text, "Copied " + phones.length + " selected phone numbers to clipboard!");
}

async function batchTagSelected() {
  const sel = document.getElementById("bulkTagStatusSelect");
  const status = sel ? sel.value : "contacted";
  const leads = getSelectedLeadObjects();
  if (leads.length === 0) {
    toast("Please select at least one lead");
    return;
  }
  const tagKeys = leads.map(function (l) { return l.tag_key || (l.source_id + ":" + l.id + ":" + l.name); });
  try {
    const res = await fetch("/api/leads/batch_tag", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ tag_keys: tagKeys, status: status })
    });
    if (!res.ok) throw new Error("Failed to batch tag leads");
    const data = await res.json();
    toast("Successfully updated " + data.count + " leads to: " + status.toUpperCase());
    loadLeads();
  } catch (err) {
    console.error("Batch tag error:", err);
    toast("Error updating leads status: " + err.message);
  }
}

async function exportSelectedLeads() {
  const leads = getSelectedLeadObjects();
  if (leads.length === 0) {
    toast("Please select at least one lead to export");
    return;
  }
  const fmtSelect = document.getElementById("bulkExportFormatSelect");
  const fmt = fmtSelect ? fmtSelect.value : "xlsx";
  toast("Exporting " + leads.length + " selected leads as " + fmt.toUpperCase() + "...");

  try {
    const res = await fetch("/api/export_selected", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ leads: leads, format: fmt })
    });
    if (!res.ok) throw new Error("Export failed");
    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.style.display = "none";
    a.href = url;
    a.download = "selected_leads_" + leads.length + "_rows." + (fmt === "xlsx" ? "xlsx" : (fmt === "json" ? "json" : "csv"));
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    toast("Download complete: " + a.download);
  } catch (err) {
    console.error("Selected export error:", err);
    toast("Error exporting selected leads: " + err.message);
  }
}

// ==================== Export Range Controls & Multi-Format Engine ====================
function onExportFormatChange(fmt) {
  currentExportFormat = fmt;
  updateExportRangePreview();
}

function updateExportRangePreview() {
  const fromInput = document.getElementById("exportFromInput");
  const toInput = document.getElementById("exportToInput");
  const badge = document.getElementById("exportCountBadge");
  const btn = document.getElementById("exportRangeBtn");
  const fmtSelect = document.getElementById("exportFormatSelect");
  if (fmtSelect) currentExportFormat = fmtSelect.value;
  if (!fromInput || !toInput) return;

  let fromVal = parseInt(fromInput.value, 10);
  let toVal = parseInt(toInput.value, 10);

  if (isNaN(fromVal) || fromVal < 1) fromVal = 1;
  if (isNaN(toVal) || toVal < fromVal) toVal = fromVal;

  const count = toVal - fromVal + 1;
  if (badge) badge.textContent = count.toLocaleString();
  const fmtLabel = currentExportFormat === "xlsx" ? "Excel (.xlsx)" : (currentExportFormat === "json" ? "JSON (.json)" : "CSV (.csv)");
  if (btn) btn.innerHTML = '<span>📥</span> Download Range ' + fmtLabel + ' (' + count.toLocaleString() + ' Leads)';
}

function setExportRange(fromNum, toNum) {
  const fromInput = document.getElementById("exportFromInput");
  const toInput = document.getElementById("exportToInput");
  if (fromInput) fromInput.value = fromNum;
  if (toInput) toInput.value = toNum;

  // Highlight active preset button
  document.querySelectorAll(".btn-preset").forEach(function (btn) {
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

  document.querySelectorAll(".btn-preset").forEach(function (b) { b.classList.remove("active"); });
  updateExportRangePreview();

  toast("Export range advanced: Lead #" + newFrom.toLocaleString() + " to #" + newTo.toLocaleString());
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
  const fmtSelect = document.getElementById("exportFormatSelect");
  const fmt = fmtSelect ? fmtSelect.value : currentExportFormat;

  if (btn) {
    btn.disabled = true;
    btn.innerHTML = '<span>⏳</span> Downloading ' + count.toLocaleString() + ' Leads...';
    setTimeout(function () {
      btn.disabled = false;
      updateExportRangePreview();
    }, 3000);
  }

  const catParam = (activeCategoriesList.length > 0) ? activeCategoriesList.join(",") : (currentCategory || "all");
  const params = new URLSearchParams({
    dataset: currentDataset || "all_global",
    search: currentSearch || "",
    tier: currentTier || "all",
    state: currentState || "all",
    country: currentCountry || "all",
    major_category: currentMajorCategory || "all",
    category: catParam,
    opportunity: currentOpportunity || "all",
    has_phone: currentHasPhone ? "true" : "false",
    format: fmt,
    export_from: String(fromVal),
    export_to: String(toVal)
  });

  const exportUrl = "/api/export?" + params.toString();
  toast("Downloading " + count.toLocaleString() + " leads as " + fmt.toUpperCase() + " (" + currentDataset + ")...");

  // Direct native browser download - leaves page intact while downloading file
  window.location.href = exportUrl;
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

  const sources = Array.from(document.querySelectorAll("input[name='src']:checked")).map(function (c) { return c.value; });
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
  pollTimer = setInterval(async function () {
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
      sel.innerHTML = datasets.map(function (d) {
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
    container.innerHTML = Object.entries(data).map(function (entry) {
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
    grid.innerHTML = datasets.map(function (d) {
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
    navigator.clipboard.writeText(textToCopy).then(function () { toast(feedbackMsg); });
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

function showToast(msg) { toast(msg); }

function toast(msg) {
  const el = document.getElementById("toast");
  if (!el) return;
  el.textContent = msg;
  el.style.display = "block";
  clearTimeout(el.timer);
  el.timer = setTimeout(function () { el.style.display = "none"; }, 2500);
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
document.addEventListener("DOMContentLoaded", function () {
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
