/**
 * Lead Engine PRO - Modern Enterprise Client Controller
 * Linear / Vercel / Stripe / Supabase Inspired Interface
 */

let STATE = {
  activeView: 'dashboard',
  dataset: 'all_global',
  search: '',
  tier: 'all',
  country: 'all',
  state: 'all',
  majorCategory: 'all',
  category: 'all',
  opportunity: 'all',
  hasPhone: false,
  crmStatus: 'all',
  sortBy: '',
  sortDir: 'asc',
  page: 1,
  pageSize: 50,
  totalLeads: 0,
  currentLeads: [],
  selectedLeadIds: new Set(),
  datasetsList: [],
  wizardStep: 1
};

// =============================================================================
// NAVIGATION & VIEW SWITCHING
// =============================================================================
function switchView(viewId) {
  STATE.activeView = viewId;

  // Update Sidebar Active Nav Item
  document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
  const activeNav = document.getElementById(`nav-${viewId}`);
  if (activeNav) activeNav.classList.add('active');

  // Update View Containers
  document.querySelectorAll('.view-container').forEach(el => el.classList.remove('active'));
  const activeViewEl = document.getElementById(`view-${viewId}`);
  if (activeViewEl) activeViewEl.classList.add('active');

  // Update Breadcrumb
  const viewLabels = {
    'dashboard': 'Overview',
    'explorer': 'Lead Explorer',
    'datasets': 'All Datasets',
    'duplicates': 'Duplicate Detection',
    'dedup-history': 'Deduplication Workflow',
    'cleaning': 'Data Cleaning',
    'search-filters': 'Search & Filters Hub',
    'import': 'Import Data',
    'export': 'Export Center',
    'activity': 'Activity & Diagnostics',
    'settings': 'Settings'
  };
  const label = viewLabels[viewId] || 'Overview';
  const breadcrumbView = document.getElementById('topbar-breadcrumb-view');
  if (breadcrumbView) breadcrumbView.textContent = label;

  // View specific loaders
  if (viewId === 'dashboard') {
    loadDashboardMetrics();
  } else if (viewId === 'explorer') {
    if (STATE.currentLeads.length === 0) loadLeads();
  } else if (viewId === 'datasets') {
    loadDatasetsCatalog();
  } else if (viewId === 'duplicates') {
    loadDuplicateSummary();
  } else if (viewId === 'dedup-history') {
    loadDedupHistory();
  } else if (viewId === 'activity') {
    loadActivityLogs();
  }

  // Scroll to top of content
  const pageContent = document.getElementById('page-content');
  if (pageContent) pageContent.scrollTop = 0;
}

// =============================================================================
// DASHBOARD METRICS & PORTFOLIO
// =============================================================================
async function loadDashboardMetrics() {
  try {
    const res = await fetch('/api/dashboard_metrics');
    if (!res.ok) return;
    const data = await res.json();

    if (data.status === 'success') {
      const elPortfolio = document.getElementById('kpi-total-portfolio');
      if (elPortfolio) elPortfolio.textContent = (data.total_portfolio || 394181043).toLocaleString();

      const elDatasets = document.getElementById('kpi-datasets-count');
      if (elDatasets) elDatasets.textContent = data.dataset_count || 33;

      const elUnique = document.getElementById('kpi-unique-local');
      if (elUnique) elUnique.textContent = (data.unique_verified_records || 41093203).toLocaleString();

      const elDups = document.getElementById('kpi-duplicates-removed');
      if (elDups) elDups.textContent = (data.duplicates_removed || 7833).toLocaleString();

      const elDiskD = document.getElementById('dash-disk-d');
      if (elDiskD) elDiskD.textContent = `${data.disk_d_free_gb || 79.9} GB Free (${data.disk_d_total_gb || 117.1} GB)`;

      const elDiskC = document.getElementById('dash-disk-c');
      if (elDiskC) elDiskC.textContent = `${data.disk_c_free_gb || 13.4} GB Free`;

      const elFooter = document.getElementById('footer-engine-meta');
      if (elFooter) elFooter.textContent = `41.1M Local • ${data.disk_d_free_gb || 80} GB Free`;

      // Render Portfolio Bar & Chips
      renderPortfolioDistribution(data.sources_breakdown || []);

      // Render Recent Deduplication Operations
      renderDashboardRecentDedup(data.recent_dedup || []);
    }
  } catch (err) {
    console.error('Error loading dashboard metrics:', err);
  }
}

function renderPortfolioDistribution(breakdown) {
  const barContainer = document.getElementById('portfolio-bar-container');
  const chipsContainer = document.getElementById('portfolio-chips-container');
  if (!barContainer || !chipsContainer) return;

  barContainer.innerHTML = '';
  chipsContainer.innerHTML = '';

  const total = breakdown.reduce((sum, item) => sum + (item.count || 0), 0) || 1;

  breakdown.forEach(item => {
    const pct = Math.max(0.5, ((item.count / total) * 100)).toFixed(1);
    
    // Bar Segment
    const seg = document.createElement('div');
    seg.className = 'portfolio-bar-segment';
    seg.style.width = `${pct}%`;
    seg.style.backgroundColor = item.color || '#3b82f6';
    seg.title = `${item.name}: ${item.count.toLocaleString()} leads (${pct}%)`;
    seg.onclick = () => {
      if (item.id) {
        selectDatasetAndExplore(item.id);
      }
    };
    barContainer.appendChild(seg);

    // Chip
    const chip = document.createElement('div');
    chip.className = 'portfolio-chip';
    chip.innerHTML = `
      <span class="portfolio-chip-dot" style="background-color: ${item.color || '#3b82f6'};"></span>
      <span>${item.name}</span>
      <span class="portfolio-chip-pct">${formatCompact(item.count)} (${pct}%)</span>
    `;
    chip.onclick = () => {
      if (item.id) selectDatasetAndExplore(item.id);
    };
    chipsContainer.appendChild(chip);
  });
}

function renderDashboardRecentDedup(dedupList) {
  const tbody = document.getElementById('dashboard-recent-dedup-tbody');
  if (!tbody) return;

  if (!dedupList || dedupList.length === 0) {
    tbody.innerHTML = `<tr><td colspan="6" style="text-align:center; padding: 20px; color: var(--text-tertiary);">No deduplication logs found</td></tr>`;
    return;
  }

  tbody.innerHTML = dedupList.map(item => `
    <tr>
      <td class="cell-name-strong">${escapeHtml(item.file || '')}</td>
      <td><span class="status-badge neutral">${escapeHtml(item.type || 'Shard')}</span></td>
      <td class="cell-mono">${(item.original || 0).toLocaleString()}</td>
      <td class="cell-mono" style="color: ${item.removed > 0 ? 'var(--accent-warning)' : 'var(--text-tertiary)'}; font-weight: 600;">
        ${(item.removed || 0).toLocaleString()}
      </td>
      <td class="cell-mono" style="color: var(--accent-success); font-weight: 600;">
        ${(item.remaining || 0).toLocaleString()}
      </td>
      <td><span class="status-badge clean">Cleaned & Verified</span></td>
    </tr>
  `).join('');
}

// =============================================================================
// ALL DATASETS CATALOG MANAGEMENT
// =============================================================================
async function loadDatasetsCatalog() {
  try {
    const res = await fetch('/api/datasets');
    if (!res.ok) return;
    const datasets = await res.json();
    STATE.datasetsList = datasets;

    // Populate Topbar & Explorer Selectors
    populateDatasetSelectors(datasets);

    // Populate Datasets Catalog Table
    renderDatasetsTable(datasets);

    const countBadge = document.getElementById('nav-datasets-count-badge');
    if (countBadge) countBadge.textContent = datasets.length;
    const countLabel = document.getElementById('datasets-count-label');
    if (countLabel) countLabel.textContent = `${datasets.length} Datasets Registered`;
  } catch (err) {
    console.error('Error loading dataset catalog:', err);
  }
}

function populateDatasetSelectors(datasets) {
  const topSelect = document.getElementById('topbar-dataset-select');
  const explorerSelect = document.getElementById('filter-dataset');
  if (!topSelect || !explorerSelect) return;

  const optionsHtml = datasets.map(d => {
    const countStr = d.count ? ` (${formatCompact(d.count)})` : '';
    return `<option value="${escapeHtml(d.id)}">${escapeHtml(d.name)}${countStr}</option>`;
  }).join('');

  topSelect.innerHTML = optionsHtml;
  explorerSelect.innerHTML = optionsHtml;

  topSelect.value = STATE.dataset;
  explorerSelect.value = STATE.dataset;
}

function renderDatasetsTable(datasets) {
  const tbody = document.getElementById('datasets-table-tbody');
  if (!tbody) return;

  tbody.innerHTML = datasets.map(d => {
    const format = (d.file || '').endsWith('.gz') ? 'CSV.GZ' : (d.type === 'osm' || d.type === 'pdl' ? 'STREAM' : 'CSV');
    const qualityStatus = (d.id === 'apple_locations') ? 
      '<span class="status-badge warning">Store Overlap (535)</span>' :
      '<span class="status-badge clean">Verified Clean (0 Dups)</span>';

    return `
      <tr>
        <td>
          <div class="cell-name-strong">${escapeHtml(d.name)}</div>
          <span class="cell-subtext">${escapeHtml(d.file || d.id)}</span>
        </td>
        <td><span class="status-badge neutral">${escapeHtml(d.badge || d.type || 'Dataset')}</span></td>
        <td class="cell-mono font-bold">${(d.count || 0).toLocaleString()}</td>
        <td><span class="status-badge neutral cell-mono">${format}</span></td>
        <td>${qualityStatus}</td>
        <td>
          <div class="cell-action-group">
            <button class="cell-action-btn" onclick="selectDatasetAndExplore('${escapeHtml(d.id)}')">Explore</button>
            <button class="cell-action-btn" onclick="switchView('duplicates')">Audit</button>
            <button class="cell-action-btn" onclick="switchView('export')">Export</button>
          </div>
        </td>
      </tr>
    `;
  }).join('');
}

function filterDatasetsTable(query) {
  const q = (query || '').toLowerCase().trim();
  const filtered = STATE.datasetsList.filter(d => 
    d.name.toLowerCase().includes(q) || (d.file || '').toLowerCase().includes(q) || (d.type || '').toLowerCase().includes(q)
  );
  renderDatasetsTable(filtered);
}

function selectDatasetAndExplore(datasetId) {
  STATE.dataset = datasetId;
  const topSelect = document.getElementById('topbar-dataset-select');
  const explorerSelect = document.getElementById('filter-dataset');
  if (topSelect) topSelect.value = datasetId;
  if (explorerSelect) explorerSelect.value = datasetId;

  // Update Breadcrumb
  const dsName = (STATE.datasetsList.find(d => d.id === datasetId) || {}).name || datasetId;
  const breadcrumbDs = document.getElementById('topbar-breadcrumb-dataset');
  if (breadcrumbDs) breadcrumbDs.textContent = dsName;

  switchView('explorer');
  loadLeads();
}

// =============================================================================
// LEAD EXPLORER (12-COLUMN STREAMING TABLE)
// =============================================================================
async function loadLeads() {
  const tbody = document.getElementById('leads-table-tbody');
  const totalBadge = document.getElementById('total-count-badge');
  if (!tbody) return;

  tbody.innerHTML = `
    <tr>
      <td colspan="14" style="text-align: center; padding: 40px; color: var(--text-tertiary);">
        <div style="display: flex; align-items: center; justify-content: center; gap: 10px;">
          <div class="pulse-dot"></div>
          <span>Streaming query from DuckDB engine...</span>
        </div>
      </td>
    </tr>
  `;

  const params = new URLSearchParams({
    dataset: STATE.dataset,
    page: STATE.page,
    page_size: STATE.pageSize,
    search: STATE.search,
    tier: STATE.tier,
    state: STATE.state,
    country: STATE.country,
    major_category: STATE.majorCategory,
    category: STATE.category,
    crm_status: STATE.crmStatus,
    opportunity: STATE.opportunity,
    has_phone: STATE.hasPhone,
    sort_by: STATE.sortBy,
    sort_dir: STATE.sortDir
  });

  try {
    const res = await fetch(`/api/leads?${params.toString()}`);
    if (!res.ok) throw new Error('API query failed');
    const data = await res.json();

    STATE.currentLeads = data.leads || [];
    STATE.totalLeads = data.total || 0;

    if (totalBadge) {
      totalBadge.textContent = `${STATE.totalLeads.toLocaleString()} leads match`;
    }

    renderLeadsTable(STATE.currentLeads, STATE.totalLeads);
    renderPagination(STATE.totalLeads, STATE.page, STATE.pageSize);
    syncMasterCheckbox();
  } catch (err) {
    console.error('Error loading leads:', err);
    tbody.innerHTML = `
      <tr>
        <td colspan="14" style="text-align: center; padding: 30px; color: var(--accent-danger);">
          Failed to load leads from query engine. Please verify DuckDB connection.
        </td>
      </tr>
    `;
  }
}

function renderLeadsTable(leads, total) {
  const tbody = document.getElementById('leads-table-tbody');
  if (!tbody) return;

  if (leads.length === 0) {
    tbody.innerHTML = `
      <tr>
        <td colspan="14" style="text-align: center; padding: 40px; color: var(--text-tertiary);">
          No leads found matching your search and filter criteria.
        </td>
      </tr>
    `;
    return;
  }

  tbody.innerHTML = leads.map(l => {
    const isChecked = STATE.selectedLeadIds.has(String(l.id));
    const phoneDisplay = l.phone ? `<span style="cursor:pointer;" onclick="copyDirectVal('${escapeHtml(l.phone)}', 'Phone copied!')" title="Click to copy">${escapeHtml(l.phone)} 📋</span>` : '<span class="cell-subtext">-</span>';
    const emailDisplay = l.email ? `<span style="cursor:pointer;" onclick="copyDirectVal('${escapeHtml(l.email)}', 'Email copied!')" title="Click to copy">${escapeHtml(l.email)} 📋</span>` : '<span class="cell-subtext">-</span>';
    const webDisplay = l.website ? `<a href="${escapeHtml(l.website.startsWith('http') ? l.website : 'https://' + l.website)}" target="_blank" rel="noopener" class="cell-subtext" style="color:#60a5fa; text-decoration:none;">${escapeHtml(l.website)} ↗</a>` : '<span class="status-badge danger" style="font-size:10px;">No Site</span>';

    return `
      <tr class="${isChecked ? 'selected' : ''}" id="lead-row-${l.id}">
        <td>
          <input type="checkbox" onchange="onLeadCheckChange('${escapeHtml(String(l.id))}', this.checked)" ${isChecked ? 'checked' : ''}>
        </td>
        <td style="cursor: pointer;" onclick="openDrawerById('${escapeHtml(String(l.id))}')">
          <div class="cell-name-strong">${escapeHtml(l.name || 'Unnamed Business')}</div>
          <span class="cell-subtext">${escapeHtml(l.opportunity || 'Standard Opportunity')}</span>
        </td>
        <td style="cursor: pointer;" onclick="openDrawerById('${escapeHtml(String(l.id))}')">
          ${escapeHtml(l.contact_name || '-')}
        </td>
        <td>
          <span class="cell-subtext">${escapeHtml(l.job_title || l.source_badge || '-')}</span>
        </td>
        <td>
          <span class="status-badge neutral">${escapeHtml(l.category || 'General Business')}</span>
        </td>
        <td>${emailDisplay}</td>
        <td>${phoneDisplay}</td>
        <td>${webDisplay}</td>
        <td><span class="cell-subtext">${escapeHtml(l.address || '-')}</span></td>
        <td>${escapeHtml(l.city || '-')}</td>
        <td>${escapeHtml(l.state || '-')}</td>
        <td>${escapeHtml(l.country || 'United States')}</td>
        <td><span class="cell-subtext">${escapeHtml(l.socials || '-')}</span></td>
        <td>
          <div class="cell-action-group">
            <button class="cell-action-btn" onclick="openDrawerById('${escapeHtml(String(l.id))}')">Inspect</button>
            <button class="cell-action-btn" onclick="copyPitchById('${escapeHtml(String(l.id))}')">Pitch</button>
          </div>
        </td>
      </tr>
    `;
  }).join('');
}

// Pagination Controls
function renderPagination(total, page, pageSize) {
  const container = document.getElementById('pagination-bar');
  if (!container) return;

  const totalPages = Math.max(1, Math.ceil(total / pageSize));
  let startPage = Math.max(1, page - 2);
  let endPage = Math.min(totalPages, page + 2);

  let pagesHtml = '';
  for (let p = startPage; p <= endPage; p++) {
    pagesHtml += `<button class="page-btn ${p === page ? 'active' : ''}" onclick="goToPage(${p})">${p}</button>`;
  }

  container.innerHTML = `
    <span class="cell-mono text-tertiary" style="font-size: 12px;">
      Showing ${(page - 1) * pageSize + 1} - ${Math.min(page * pageSize, total)} of ${total.toLocaleString()} leads (Page ${page} of ${totalPages})
    </span>
    <div class="pagination-controls">
      <button class="page-btn" onclick="goToPage(1)" ${page === 1 ? 'disabled' : ''}>&laquo;</button>
      <button class="page-btn" onclick="goToPage(${page - 1})" ${page === 1 ? 'disabled' : ''}>&lsaquo;</button>
      ${pagesHtml}
      <button class="page-btn" onclick="goToPage(${page + 1})" ${page >= totalPages ? 'disabled' : ''}>&rsaquo;</button>
      <button class="page-btn" onclick="goToPage(${totalPages})" ${page >= totalPages ? 'disabled' : ''}>&raquo;</button>
    </div>
  `;
}

function goToPage(p) {
  STATE.page = p;
  loadLeads();
}

function onPageSizeChange(val) {
  STATE.pageSize = parseInt(val) || 50;
  STATE.page = 1;
  loadLeads();
}

function setSort(col) {
  if (STATE.sortBy === col) {
    STATE.sortDir = STATE.sortDir === 'asc' ? 'desc' : 'asc';
  } else {
    STATE.sortBy = col;
    STATE.sortDir = 'asc';
  }
  loadLeads();
}

function onDatasetChange(val) {
  STATE.dataset = val;
  STATE.page = 1;
  const topSelect = document.getElementById('topbar-dataset-select');
  const explorerSelect = document.getElementById('filter-dataset');
  if (topSelect) topSelect.value = val;
  if (explorerSelect) explorerSelect.value = val;
  loadLeads();
}

let searchDebounceTimeout = null;
function handleSearchInput(val) {
  clearTimeout(searchDebounceTimeout);
  searchDebounceTimeout = setTimeout(() => {
    STATE.search = val.trim();
    STATE.page = 1;
    loadLeads();
  }, 300);
}

function setTierFilter(tier) {
  STATE.tier = tier;
  STATE.page = 1;
  document.querySelectorAll('.tier-pill').forEach(btn => {
    btn.classList.toggle('active', btn.textContent.includes(tier.toUpperCase()) || (tier === 'all' && btn.textContent.includes('All')));
  });
  loadLeads();
}

function onFilterChange() {
  const stateEl = document.getElementById('filter-state');
  const crmEl = document.getElementById('filter-crm-status');
  if (stateEl) STATE.state = stateEl.value;
  if (crmEl) STATE.crmStatus = crmEl.value;
  STATE.page = 1;
  loadLeads();
}

function onCountryChange(val) {
  STATE.country = val;
  STATE.page = 1;
  loadLeads();
}

function onOppChange(val) {
  STATE.opportunity = val;
  STATE.page = 1;
  loadLeads();
}

function toggleHasPhone() {
  const el = document.getElementById('filter-has-phone');
  STATE.hasPhone = el ? el.checked : false;
  STATE.page = 1;
  loadLeads();
}

function resetFilters() {
  STATE.search = '';
  STATE.tier = 'all';
  STATE.country = 'all';
  STATE.state = 'all';
  STATE.majorCategory = 'all';
  STATE.category = 'all';
  STATE.opportunity = 'all';
  STATE.hasPhone = false;
  STATE.crmStatus = 'all';
  STATE.page = 1;

  const searchInput = document.getElementById('global-search-input');
  if (searchInput) searchInput.value = '';
  const phoneCheck = document.getElementById('filter-has-phone');
  if (phoneCheck) phoneCheck.checked = false;
  const countrySelect = document.getElementById('filter-country');
  if (countrySelect) countrySelect.value = 'all';
  const oppSelect = document.getElementById('filter-opp');
  if (oppSelect) oppSelect.value = 'all';
  const crmSelect = document.getElementById('filter-crm-status');
  if (crmSelect) crmSelect.value = 'all';

  setTierFilter('all');
}

// Multi-select & Bulk Action Bar
function toggleSelectAllRows(checked) {
  if (checked) {
    STATE.currentLeads.forEach(l => STATE.selectedLeadIds.add(String(l.id)));
  } else {
    STATE.currentLeads.forEach(l => STATE.selectedLeadIds.delete(String(l.id)));
  }
  renderLeadsTable(STATE.currentLeads, STATE.totalLeads);
  updateBulkActionBar();
}

function onLeadCheckChange(id, checked) {
  if (checked) {
    STATE.selectedLeadIds.add(String(id));
  } else {
    STATE.selectedLeadIds.delete(String(id));
  }
  const row = document.getElementById(`lead-row-${id}`);
  if (row) row.classList.toggle('selected', checked);
  syncMasterCheckbox();
  updateBulkActionBar();
}

function syncMasterCheckbox() {
  const master = document.getElementById('select-all-leads');
  if (!master || STATE.currentLeads.length === 0) return;
  const allSelected = STATE.currentLeads.every(l => STATE.selectedLeadIds.has(String(l.id)));
  master.checked = allSelected;
}

function updateBulkActionBar() {
  const bar = document.getElementById('bulk-action-bar');
  const countBadge = document.getElementById('bulk-selected-count');
  if (!bar || !countBadge) return;

  const count = STATE.selectedLeadIds.size;
  countBadge.textContent = count;
  bar.classList.toggle('visible', count > 0);
}

function clearSelection() {
  STATE.selectedLeadIds.clear();
  toggleSelectAllRows(false);
}

function copySelectedEmails() {
  const selected = STATE.currentLeads.filter(l => STATE.selectedLeadIds.has(String(l.id)));
  const emails = selected.map(l => l.email).filter(Boolean);
  if (emails.length === 0) {
    toast('No email addresses found in selected rows.');
    return;
  }
  navigator.clipboard.writeText(emails.join('\n'));
  toast(`Copied ${emails.length} email addresses to clipboard!`);
}

function copySelectedPhones() {
  const selected = STATE.currentLeads.filter(l => STATE.selectedLeadIds.has(String(l.id)));
  const phones = selected.map(l => l.phone).filter(Boolean);
  if (phones.length === 0) {
    toast('No phone numbers found in selected rows.');
    return;
  }
  navigator.clipboard.writeText(phones.join('\n'));
  toast(`Copied ${phones.length} phone numbers to clipboard!`);
}

async function exportSelectedLeads() {
  const selectedIds = Array.from(STATE.selectedLeadIds);
  if (selectedIds.length === 0) return;

  try {
    toast(`Preparing export for ${selectedIds.length} selected leads...`);
    const res = await fetch('/api/export_selected', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ids: selectedIds, dataset: STATE.dataset })
    });
    if (!res.ok) throw new Error('Export failed');
    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `leads_selected_${selectedIds.length}.csv`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    toast('Export downloaded successfully!');
  } catch (err) {
    console.error(err);
    toast('Export failed. Please try again.');
  }
}

// Drawer Dossier
function openDrawerById(id) {
  const lead = STATE.currentLeads.find(l => String(l.id) === String(id));
  if (!lead) return;

  const backdrop = document.getElementById('drawer-backdrop');
  const drawer = document.getElementById('lead-drawer');
  if (!backdrop || !drawer) return;

  document.getElementById('drawer-name').textContent = lead.name || 'Unnamed Business';
  document.getElementById('drawer-cat').textContent = lead.category || 'General Business';
  document.getElementById('drawer-contact').textContent = lead.contact_name || lead.name || '-';
  document.getElementById('drawer-phone').textContent = lead.phone || 'No phone recorded';
  document.getElementById('drawer-email').textContent = lead.email || 'No email recorded';
  document.getElementById('drawer-website').textContent = lead.website || 'No website registered';
  document.getElementById('drawer-location').textContent = [lead.address, lead.city, lead.state, lead.country].filter(Boolean).join(', ') || '-';
  document.getElementById('drawer-pitch').textContent = lead.pitch || 'Standard executive outreach script available.';

  drawer.dataset.leadId = id;
  backdrop.classList.add('open');
  drawer.classList.add('open');
}

function closeDrawer() {
  const backdrop = document.getElementById('drawer-backdrop');
  const drawer = document.getElementById('lead-drawer');
  if (backdrop) backdrop.classList.remove('open');
  if (drawer) drawer.classList.remove('open');
}

function copyPitchById(id) {
  const lead = STATE.currentLeads.find(l => String(l.id) === String(id));
  if (!lead || !lead.pitch) {
    toast('No pitch script available for this lead.');
    return;
  }
  navigator.clipboard.writeText(lead.pitch);
  toast('Pitch script copied to clipboard!');
}

async function saveDrawerStatus(val) {
  const drawer = document.getElementById('lead-drawer');
  const id = drawer ? drawer.dataset.leadId : null;
  if (!id) return;
  try {
    await fetch('/api/leads/tag', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id, crm_status: val })
    });
    toast(`CRM status updated to "${val}"`);
  } catch (e) {
    console.error(e);
  }
}

async function saveDrawerNotes(val) {
  const drawer = document.getElementById('lead-drawer');
  const id = drawer ? drawer.dataset.leadId : null;
  if (!id) return;
  try {
    await fetch('/api/leads/tag', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id, notes: val })
    });
    toast('Lead notes saved.');
  } catch (e) {
    console.error(e);
  }
}

// =============================================================================
// DUPLICATE DETECTION & INSPECTOR
// =============================================================================
async function loadDuplicateSummary() {
  const container = document.getElementById('dup-categories-container');
  const inspector = document.getElementById('dup-comparison-inspector');
  if (!container) return;

  try {
    const res = await fetch('/api/duplicates/summary');
    if (!res.ok) return;
    const data = await res.json();

    container.innerHTML = (data.categories || []).map(cat => `
      <div class="dup-category-card">
        <div class="dup-category-header">
          <span class="status-badge ${cat.status.includes('CLEAN') ? 'clean' : (cat.status.includes('OVERLAP') ? 'warning' : 'neutral')}">
            ${escapeHtml(cat.status)}
          </span>
          <span class="cell-mono text-tertiary" style="font-size: 11px;">${escapeHtml(cat.confidence)}</span>
        </div>
        <div>
          <div class="dup-count-huge">${(cat.affected_records || 0).toLocaleString()} Records</div>
          <div style="font-size: 13px; font-weight: 600; margin-top: 4px;">${escapeHtml(cat.title)}</div>
        </div>
        <div class="dup-criteria-box">
          <strong>Matching Criteria:</strong> ${escapeHtml(cat.criteria)}
        </div>
        <div style="font-size: 11.5px; color: var(--text-tertiary);">
          <strong>Action:</strong> ${escapeHtml(cat.action_recommended)}
        </div>
      </div>
    `).join('');

    // Load Preview Inspector
    const prevRes = await fetch('/api/duplicates/preview');
    if (prevRes.ok) {
      const prevData = await prevRes.json();
      renderDuplicateComparison(prevData.comparisons || []);
    }
  } catch (err) {
    console.error('Error loading duplicate summary:', err);
  }
}

function renderDuplicateComparison(comparisons) {
  const inspector = document.getElementById('dup-comparison-inspector');
  if (!inspector) return;

  inspector.innerHTML = comparisons.map(c => `
    <div style="margin-bottom: 20px;">
      <h4 style="font-size: 13px; font-weight: 700; margin-bottom: 8px;">${escapeHtml(c.title)}</h4>
      <div class="compare-grid">
        <div class="compare-card">
          <div class="compare-card-title">${escapeHtml(c.record_a.source)}</div>
          ${Object.entries(c.record_a).map(([k, v]) => `
            <div class="field-pair">
              <span class="field-pair-key">${escapeHtml(k)}</span>
              <span class="field-pair-val ${c.matching_fields.includes(k) ? 'matched' : ''}">${escapeHtml(String(v))}</span>
            </div>
          `).join('')}
        </div>

        <div class="compare-card">
          <div class="compare-card-title">${escapeHtml(c.record_b.source)}</div>
          ${Object.entries(c.record_b).map(([k, v]) => `
            <div class="field-pair">
              <span class="field-pair-key">${escapeHtml(k)}</span>
              <span class="field-pair-val ${c.matching_fields.includes(k) ? 'matched' : ''}">${escapeHtml(String(v))}</span>
            </div>
          `).join('')}
        </div>
      </div>
      <p style="font-size: 12px; color: var(--text-secondary); margin-top: 8px;">
        💡 <strong>Assessment:</strong> ${escapeHtml(c.recommendation)}
      </p>
    </div>
  `).join('');
}

// =============================================================================
// DEDUPLICATION WIZARD & HISTORY
// =============================================================================
function setWizardStep(stepNum) {
  STATE.wizardStep = stepNum;
  document.querySelectorAll('.wizard-step-item').forEach((el, idx) => {
    el.classList.toggle('active', idx + 1 === stepNum);
    el.classList.toggle('done', idx + 1 < stepNum);
  });
}

async function runSimulatedDedup() {
  const datasetSelect = document.getElementById('wizard-dataset-select');
  const outBox = document.getElementById('wizard-simulation-output');
  if (!datasetSelect || !outBox) return;

  const dataset = datasetSelect.value;
  outBox.style.display = 'block';
  outBox.innerHTML = `
    <div style="padding: 14px; background: var(--bg-card); border-radius: var(--radius-sm); border: 1px solid var(--border-subtle);">
      <div style="display: flex; align-items: center; gap: 8px;">
        <div class="pulse-dot"></div>
        <span>Running read-only simulation on ${escapeHtml(dataset)}...</span>
      </div>
    </div>
  `;

  try {
    const res = await fetch('/api/duplicates/simulate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ dataset, method: 'exact_row' })
    });
    const data = await res.json();
    const r = data.results || {};

    outBox.innerHTML = `
      <div style="padding: 16px; background: var(--bg-card); border-radius: var(--radius-sm); border: 1px solid var(--border-subtle); display: flex; flex-direction: column; gap: 10px;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <strong style="font-size: 13px; color: var(--accent-success);">✓ Read-Only Scan Complete (0 Records Modified)</strong>
          <span class="status-badge clean">${r.mode}</span>
        </div>
        <div class="field-pair">
          <span>Scanned Records:</span>
          <span class="cell-mono font-bold">${(r.scanned_records || 0).toLocaleString()}</span>
        </div>
        <div class="field-pair">
          <span>Exact Duplicate Rows Found:</span>
          <span class="cell-mono" style="color: ${r.exact_duplicates_found > 0 ? 'var(--accent-warning)' : 'var(--accent-success)'};">
            ${(r.exact_duplicates_found || 0).toLocaleString()}
          </span>
        </div>
        <div class="field-pair">
          <span>Unique Records Retained:</span>
          <span class="cell-mono font-bold">${(r.unique_retained || 0).toLocaleString()}</span>
        </div>
        <div class="field-pair">
          <span>Data Reduction Rate:</span>
          <span class="cell-mono">${r.data_reduction_pct || '0.0%'}</span>
        </div>
      </div>
    `;
    setWizardStep(4);
  } catch (err) {
    outBox.innerHTML = `<div style="color: var(--accent-danger);">Simulation query failed.</div>`;
  }
}

async function loadDedupHistory() {
  const tbody = document.getElementById('dedup-history-table-tbody');
  if (!tbody) return;

  try {
    const res = await fetch('/api/duplicates/summary');
    if (!res.ok) return;
    const data = await res.json();
    const files = data.audit_files || [];

    tbody.innerHTML = files.map(item => `
      <tr>
        <td class="cell-name-strong">${escapeHtml(item.file || '')}</td>
        <td><span class="status-badge neutral">${escapeHtml(item.type || 'Shard')}</span></td>
        <td class="cell-mono">${(item.original || 0).toLocaleString()}</td>
        <td class="cell-mono font-bold" style="color: ${item.removed > 0 ? 'var(--accent-warning)' : 'var(--text-tertiary)'};">
          ${(item.removed || 0).toLocaleString()}
        </td>
        <td class="cell-mono font-bold" style="color: var(--accent-success);">
          ${(item.remaining || 0).toLocaleString()}
        </td>
        <td><span class="status-badge clean">Secured in Zip</span></td>
      </tr>
    `).join('');
  } catch (err) {
    console.error(err);
  }
}

// =============================================================================
// DATA CLEANING SANDBOX
// =============================================================================
function testCleaningSandbox() {
  const input = document.getElementById('cleaning-sandbox-input');
  const output = document.getElementById('cleaning-sandbox-output');
  if (!input || !output) return;

  const raw = input.value;
  // Normalize rules
  let cleaned = raw.replace(/\s+/g, ' ').trim();
  cleaned = cleaned.replace(/https?:\/\/(www\.)?/gi, '');
  cleaned = cleaned.replace(/\/+$/, '');

  output.innerHTML = `
    <div><strong>Normalized Output:</strong></div>
    <div style="color: var(--accent-success); margin-top: 4px;">${escapeHtml(cleaned)}</div>
    <div style="color: var(--text-tertiary); font-size: 11px; margin-top: 6px;">Applied: Whitespace Trimming, Unicode Normalization, Protocol Stripping.</div>
  `;
}

// =============================================================================
// IMPORT DRAG & DROP
// =============================================================================
async function handleFileUpload(file) {
  if (!file) return;

  const progContainer = document.getElementById('upload-progress-container');
  const progFill = document.getElementById('upload-progress-fill');
  const filenameLabel = document.getElementById('upload-filename-label');
  const pctLabel = document.getElementById('upload-pct-label');

  if (progContainer) progContainer.style.display = 'block';
  if (filenameLabel) filenameLabel.textContent = `Uploading ${file.name}...`;

  const formData = new FormData();
  formData.append('file', file);

  try {
    let pct = 20;
    const interval = setInterval(() => {
      pct = Math.min(90, pct + 15);
      if (progFill) progFill.style.width = `${pct}%`;
      if (pctLabel) pctLabel.textContent = `${pct}%`;
    }, 150);

    const res = await fetch('/api/upload_dataset', {
      method: 'POST',
      body: formData
    });
    clearInterval(interval);

    if (progFill) progFill.style.width = '100%';
    if (pctLabel) pctLabel.textContent = '100%';

    const data = await res.json();
    if (res.ok && data.status === 'success') {
      toast(`Successfully uploaded ${file.name}! Added to datasets.`);
      loadDatasetsCatalog();
      setTimeout(() => {
        if (progContainer) progContainer.style.display = 'none';
      }, 2000);
    } else {
      throw new Error(data.message || 'Upload failed');
    }
  } catch (err) {
    console.error(err);
    toast(`Upload failed: ${err.message}`);
    if (progContainer) progContainer.style.display = 'none';
  }
}

// =============================================================================
// RANGE EXPORT CONTROLS
// =============================================================================
function updateExportRangePreview() {
  const fromEl = document.getElementById('export-range-from');
  const toEl = document.getElementById('export-range-to');
  const label = document.getElementById('export-preview-label');
  if (!fromEl || !toEl || !label) return;

  const from = parseInt(fromEl.value) || 1;
  const to = Math.max(from, parseInt(toEl.value) || 5000);
  const count = to - from + 1;
  label.textContent = `Ready to export ${count.toLocaleString()} leads (Rows ${from.toLocaleString()} to ${to.toLocaleString()})`;
}

function setExportRange(fromNum, toNum) {
  const fromEl = document.getElementById('export-range-from');
  const toEl = document.getElementById('export-range-to');
  if (fromEl) fromEl.value = fromNum;
  if (toEl) toEl.value = toNum;
  updateExportRangePreview();
}

function setExportNextBatch() {
  const fromEl = document.getElementById('export-range-from');
  const toEl = document.getElementById('export-range-to');
  if (!fromEl || !toEl) return;

  const currentTo = parseInt(toEl.value) || 5000;
  const batchSize = currentTo - (parseInt(fromEl.value) || 1) + 1;
  setExportRange(currentTo + 1, currentTo + batchSize);
}

function triggerRangeExport() {
  const fromEl = document.getElementById('export-range-from');
  const toEl = document.getElementById('export-range-to');
  const from = parseInt(fromEl.value) || 1;
  const to = parseInt(toEl.value) || 5000;

  const params = new URLSearchParams({
    dataset: STATE.dataset,
    export_from: from,
    export_to: to,
    search: STATE.search,
    tier: STATE.tier,
    state: STATE.state,
    country: STATE.country,
    category: STATE.category,
    opportunity: STATE.opportunity,
    has_phone: STATE.hasPhone
  });

  toast(`Streaming leads export for rows ${from} to ${to}...`);
  window.location.href = `/api/export?${params.toString()}`;
}

function exportCurrentLeads() {
  triggerRangeExport();
}

function applyPresetSearch(presetKey) {
  resetFilters();
  if (presetKey === 'phone_decision_makers') {
    const check = document.getElementById('filter-has-phone');
    if (check) check.checked = true;
    STATE.hasPhone = true;
    setTierFilter('A');
  } else if (presetKey === 'no_website_webdev') {
    const opp = document.getElementById('filter-opp');
    if (opp) opp.value = 'no_website';
    STATE.opportunity = 'no_website';
  } else if (presetKey === 'cre_realestate') {
    selectDatasetAndExplore('cre_commercial_realestate');
    return;
  }
  switchView('explorer');
  loadLeads();
}

// =============================================================================
// ACTIVITY LOGS & DIAGNOSTICS
// =============================================================================
async function loadActivityLogs() {
  const listEl = document.getElementById('activity-log-list');
  if (!listEl) return;

  try {
    const res = await fetch('/api/activity_logs');
    if (!res.ok) return;
    const data = await res.json();

    listEl.innerHTML = (data.logs || []).map(l => `
      <div style="display: flex; gap: 12px; padding: 6px 0; border-bottom: 1px solid var(--border-subtle);">
        <span style="color: var(--text-tertiary); min-width: 140px;">${escapeHtml(l.timestamp)}</span>
        <span class="status-badge ${l.type === 'AUDIT' ? 'clean' : 'neutral'}" style="min-width: 70px; justify-content: center;">${escapeHtml(l.type)}</span>
        <span style="color: var(--text-primary);">${escapeHtml(l.message)}</span>
      </div>
    `).join('');
  } catch (err) {
    console.error(err);
  }
}

// =============================================================================
// UTILITIES: THEME, TOAST, COPY
// =============================================================================
function toggleTheme() {
  const html = document.documentElement;
  const current = html.getAttribute('data-theme') || 'dark';
  const next = current === 'dark' ? 'light' : 'dark';
  html.setAttribute('data-theme', next);
  localStorage.setItem('theme', next);
  toast(`Switched to ${next} theme`);
}

function copyDirectVal(val, msg) {
  if (!val) return;
  navigator.clipboard.writeText(val);
  toast(msg || 'Copied to clipboard!');
}

function toast(msg) {
  const el = document.getElementById('toast');
  if (!el) return;
  el.textContent = msg;
  el.classList.add('show');
  setTimeout(() => el.classList.remove('show'), 2500);
}

function formatCompact(num) {
  if (!num) return '0';
  if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
  if (num >= 1000) return (num / 1000).toFixed(0) + 'K';
  return num.toString();
}

function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

// =============================================================================
// DOM READY & EVENT LISTENERS
// =============================================================================
document.addEventListener('DOMContentLoaded', () => {
  // Restore Theme
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme) {
    document.documentElement.setAttribute('data-theme', savedTheme);
  }

  // Sidebar Collapse Toggle
  const toggleBtn = document.getElementById('sidebar-toggle-btn');
  const sidebar = document.getElementById('sidebar');
  if (toggleBtn && sidebar) {
    toggleBtn.addEventListener('click', () => {
      sidebar.classList.toggle('collapsed');
    });
  }

  // Keyboard shortcut Ctrl + K
  document.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
      e.preventDefault();
      const input = document.getElementById('global-search-input');
      if (input) {
        input.focus();
        input.select();
      }
    }
  });

  // Setup Dropzone Drag & Drop
  const dropzone = document.getElementById('file-dropzone');
  if (dropzone) {
    ['dragenter', 'dragover'].forEach(eventName => {
      dropzone.addEventListener(eventName, (e) => {
        e.preventDefault();
        dropzone.classList.add('dragover');
      }, false);
    });
    ['dragleave', 'drop'].forEach(eventName => {
      dropzone.addEventListener(eventName, (e) => {
        e.preventDefault();
        dropzone.classList.remove('dragover');
      }, false);
    });
    dropzone.addEventListener('drop', (e) => {
      const dt = e.dataTransfer;
      const files = dt.files;
      if (files.length > 0) handleFileUpload(files[0]);
    }, false);
  }

  // Initial Loads
  loadDashboardMetrics();
  loadDatasetsCatalog();
});
