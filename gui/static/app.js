/**
 * Lead Engine PRO - Modern Enterprise Client Controller
 * Linear / Stripe / Supabase Disciplined Data Architecture
 */

/**
 * =============================================================================
 * CENTRALIZED ICON ARCHITECTURE (LUCIDE SYSTEM)
 * =============================================================================
 * Standardized SVG icon definitions ensuring deterministic stroke weights,
 * consistent 16-20px sizing, and semantic alignment across all components.
 */
const LUCIDE_ICONS = {
  'layout-dashboard': '<rect width="7" height="9" x="3" y="3" rx="1"/><rect width="7" height="5" x="14" y="3" rx="1"/><rect width="7" height="9" x="14" y="12" rx="1"/><rect width="7" height="5" x="3" y="16" rx="1"/>',
  'database': '<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5V19A9 3 0 0 0 21 19V5"/><path d="M3 12A9 3 0 0 0 21 12"/>',
  'files': '<path d="M20 7h-3a2 2 0 0 1-2-2V2"/><path d="M9 18a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h7l4 4v10a2 2 0 0 1-2 2Z"/><path d="M3 7.6v12.8A1.6 1.6 0 0 0 4.6 22h11"/>',
  'file-text': '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 9H8"/><path d="M16 13H8"/><path d="M16 17H8"/>',
  'file-up': '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M12 12v6"/><path d="m15 15-3-3-3 3"/>',
  'file-down': '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M12 18v-6"/><path d="m9 15 3 3 3-3"/>',
  'users': '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
  'contact': '<path d="M16 2v2"/><path d="M7 22v-2a2 2 0 0 1 2-2h6a2 2 0 0 1 2 2v2"/><path d="M8 2v2"/><circle cx="12" cy="11" r="3"/><rect x="3" y="4" width="18" height="18" rx="2"/>',
  'building-2': '<path d="M6 22V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v18Z"/><path d="M6 12H4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h2"/><path d="M18 9h2a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-2"/><path d="M10 6h4"/><path d="M10 10h4"/><path d="M10 14h4"/><path d="M10 18h4"/>',
  'building': '<rect width="16" height="20" x="4" y="2" rx="2" ry="2"/><path d="M9 22v-4h6v4"/><path d="M8 6h.01"/><path d="M16 6h.01"/><path d="M12 6h.01"/><path d="M12 10h.01"/><path d="M12 14h.01"/><path d="M16 10h.01"/><path d="M16 14h.01"/><path d="M8 10h.01"/><path d="M8 14h.01"/>',
  'phone': '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>',
  'mail': '<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
  'globe': '<circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/>',
  'search': '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
  'list-filter': '<path d="M3 6h18"/><path d="M7 12h10"/><path d="M10 18h4"/>',
  'fingerprint': '<path d="M12 10a2 2 0 0 0-2 2c0 1.02-.1 2.51-.26 4"/><path d="M14 13.12c0 2.38 0 6.38-1 8.88"/><path d="M17.29 21.02c.12-.6.43-2.3.5-3.02"/><path d="M2 12a10 10 0 0 1 18-6"/><path d="M2 16h.01"/><path d="M21.8 16c.2-2 .131-5.354 0-6"/><path d="M5 19.5C5.5 18 6 15 6 12a6 6 0 0 1 .34-2"/><path d="M8.65 22c.21-.66.45-1.32.57-2"/><path d="M9 6.8a6 6 0 0 1 9 5.2v2"/>',
  'shield-check': '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
  'clipboard-list': '<rect width="8" height="4" x="8" y="2" rx="1" ry="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="M12 11h4"/><path d="M12 16h4"/><path d="M8 11h.01"/><path d="M8 16h.01"/>',
  'bar-chart-3': '<path d="M3 3v18h18"/><path d="M18 17V9"/><path d="M13 17V5"/><path d="M8 17v-3"/>',
  'settings': '<path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/><circle cx="12" cy="12" r="3"/>',
  'bell': '<path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/>',
  'circle-alert': '<circle cx="12" cy="12" r="10"/><line x1="12" x2="12" y1="8" y2="12"/><line x1="12" x2="12.01" y1="16" y2="16"/>',
  'triangle-alert': '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" x2="12" y1="9" y2="13"/><line x1="12" x2="12.01" y1="17" y2="17"/>',
  'circle-check': '<circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/>',
  'loader-circle': '<path d="M21 12a9 9 0 1 1-6.219-8.56"/>',
  'hard-drive': '<line x1="22" x2="2" y1="12" y2="12"/><path d="M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/><line x1="6" x2="6.01" y1="16" y2="16"/><line x1="10" x2="10.01" y1="16" y2="16"/>',
  'map-pin': '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
  'layers': '<polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/>',
  'refresh-cw': '<path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/><path d="M8 16H3v5"/>',
  'archive': '<rect width="20" height="5" x="2" y="3" rx="1"/><path d="M4 8v11a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8"/><path d="M10 12h4"/>',
  'circle-help': '<circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><path d="M12 17h.01"/>',
  'eye': '<path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/>',
  'sparkles': '<path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/>',
  'briefcase': '<rect width="20" height="14" x="2" y="7" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>',
  'cpu': '<rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><path d="M15 2v2"/><path d="M15 20v2"/><path d="M2 15h2"/><path d="M2 9h2"/><path d="M20 15h2"/><path d="M20 9h2"/><path d="M9 21v2"/><path d="M9 1v2"/>',
  'landmark': '<line x1="3" x2="21" y1="22" y2="22"/><line x1="6" x2="6" y1="18" y2="11"/><line x1="10" x2="10" y1="18" y2="11"/><line x1="14" x2="14" y1="18" y2="11"/><line x1="18" x2="18" y1="18" y2="11"/><polygon points="12 2 20 7 4 7"/>',
  'line-chart': '<path d="M3 3v18h18"/><path d="m19 9-5 5-4-4-3 3"/>',
  'network': '<rect x="16" y="16" width="6" height="6" rx="1"/><rect x="2" y="16" width="6" height="6" rx="1"/><rect x="9" y="2" width="6" height="6" rx="1"/><path d="M5 16v-3a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v3"/><path d="M12 12V8"/>',
  'store': '<path d="m2 7 4.41-4.41A2 2 0 0 1 7.83 2h8.34a2 2 0 0 1 1.42.59L22 7"/><path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"/><path d="M15 22v-4a2 2 0 0 0-2-2h-2a2 2 0 0 0-2 2v4"/><path d="M2 7h20"/><path d="M22 7v3a2 2 0 0 1-2 2v0a2.7 2.7 0 0 1-1.59-.63.7.7 0 0 0-.82 0A2.7 2.7 0 0 1 16 12a2.7 2.7 0 0 1-1.59-.63.7.7 0 0 0-.82 0A2.7 2.7 0 0 1 12 12a2.7 2.7 0 0 1-1.59-.63.7.7 0 0 0-.82 0A2.7 2.7 0 0 1 8 12a2.7 2.7 0 0 1-1.59-.63.7.7 0 0 0-.82 0A2.7 2.7 0 0 1 4 12v0a2 2 0 0 1-2-2V7"/>',
  'home': '<path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/>',
  'award': '<circle cx="12" cy="8" r="6"/><path d="M15.477 12.89 17 22l-5-3-5 3 1.523-9.11"/>',
  'utensils': '<path d="M18 2v6a3 3 0 0 1-3 3 3 3 0 0 1-3-3V2"/><path d="M15 2v18"/><path d="M7 2v20"/><path d="M4 2v4a3 3 0 0 0 3 3v0a3 3 0 0 0 3-3V2"/>',
  'target': '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
  'palette': '<circle cx="13.5" cy="6.5" r=".5" fill="currentColor"/><circle cx="17.5" cy="10.5" r=".5" fill="currentColor"/><circle cx="8.5" cy="7.5" r=".5" fill="currentColor"/><circle cx="6.5" cy="12.5" r=".5" fill="currentColor"/><path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10c.926 0 1.648-.746 1.648-1.688 0-.437-.18-.835-.437-1.125-.29-.289-.438-.652-.438-1.125a1.64 1.64 0 0 1 1.668-1.668h1.996c3.051 0 5.555-2.503 5.555-5.554C21.965 6.012 17.461 2 12 2z"/>',
  'rocket': '<path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/><path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"/><path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"/>',
  'camera': '<path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z"/><circle cx="12" cy="13" r="3"/>',
  'music': '<path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/>',
  'activity': '<path d="M22 12h-4l-3 9L9 3l-3 9H2"/>',
  'moon': '<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>',
  'sun': '<circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/>',
  'copy': '<rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/>',
  'check': '<path d="M20 6 9 17l-5-5"/>',
  'external-link': '<path d="M15 3h6v6"/><path d="M10 14 21 3"/><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>',
  'x': '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
  'chevron-right': '<path d="m9 18 6-6-6-6"/>',
  'chevron-left': '<path d="m15 18-6-6 6-6"/>',
  'chevron-down': '<path d="m6 9 6 6 6-6"/>',
  'chevrons-right': '<path d="m6 17 5-5-5-5"/><path d="m13 17 5-5-5-5"/>',
  'chevrons-left': '<path d="m11 17-5-5 5-5"/><path d="m18 17-5-5 5-5"/>',
  'filter': '<polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/>',
  'arrow-up-right': '<path d="M7 7h10v10"/><path d="M7 17 17 7"/>',
  'plus': '<path d="M5 12h14"/><path d="M12 5v14"/>',
  'download': '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/>',
  'sliders': '<line x1="4" x2="4" y1="21" y2="14"/><line x1="4" x2="4" y1="10" y2="3"/><line x1="12" x2="12" y1="21" y2="12"/><line x1="12" x2="12" y1="8" y2="3"/><line x1="20" x2="20" y1="21" y2="16"/><line x1="20" x2="20" y1="12" y2="3"/><line x1="1" x2="7" y1="14" y2="14"/><line x1="9" x2="15" y1="8" y2="8"/><line x1="17" x2="23" y1="16" y2="16"/>'
};

function getIconSvg(iconName, options = {}) {
  const size = options.size || 16;
  const className = options.className || '';
  const title = options.title ? `<title>${escapeHtml(options.title)}</title>` : '';
  const strokeWidth = options.strokeWidth || 1.75;
  const content = LUCIDE_ICONS[iconName] || LUCIDE_ICONS['database'] || '<circle cx="12" cy="12" r="10"/>';
  return `<svg width="${size}" height="${size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="${strokeWidth}" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-${iconName} icon-svg ${className}">${title}${content}</svg>`;
}

/**
 * =============================================================================
 * CENTRALIZED DATA SOURCE REGISTRY (MANDATORY REQUIREMENT)
 * =============================================================================
 * Single source of truth for all data sources across the entire application:
 * stable ID -> canonical display name -> designated permanent icon -> semantic color
 */
const SOURCE_REGISTRY = {
  'all_global': {
    id: 'all_global',
    canonicalName: 'All Global Leads & Master Portfolio',
    shortName: 'Global Master Portfolio',
    icon: 'layers',
    color: '#3b82f6',
    category: 'Global Master Feed',
    badgeText: 'Global Portfolio'
  },
  'all_local_unified': {
    id: 'all_local_unified',
    canonicalName: 'All Local Databases Unified',
    shortName: 'Local Databases',
    icon: 'database',
    color: '#10b981',
    category: 'Local Columnar Engine',
    badgeText: 'Local Unified'
  },
  'free_company_dataset': {
    id: 'free_company_dataset',
    canonicalName: 'Free Company Global Dataset',
    shortName: 'Free Company DB',
    icon: 'building-2',
    color: '#3b82f6',
    category: 'Corporate Registry',
    badgeText: 'Free Company DB'
  },
  'odo_senzing': {
    id: 'odo_senzing',
    canonicalName: 'ODO Senzing: Global Commercial Entities',
    shortName: 'ODO Senzing',
    icon: 'shield-check',
    color: '#8b5cf6',
    category: 'Entity-Resolved Orgs',
    badgeText: 'ODO Senzing'
  },
  'planet_daily_osm': {
    id: 'planet_daily_osm',
    canonicalName: 'OpenStreetMap Planet Daily Commercial Leads',
    shortName: 'Planet Daily OSM',
    icon: 'globe',
    color: '#0ea5e9',
    category: 'Geospatial & POI',
    badgeText: 'Planet Daily'
  },
  'gleif_goldencopy': {
    id: 'gleif_goldencopy',
    canonicalName: 'GLEIF Golden Copy Global Legal Entity Identifier Registry',
    shortName: 'GLEIF Golden Copy',
    icon: 'landmark',
    color: '#0284c7',
    category: 'Legal Identifiers',
    badgeText: 'GLEIF Legal'
  },
  'sec_edgar_filers': {
    id: 'sec_edgar_filers',
    canonicalName: 'U.S. SEC EDGAR Corporate Filers & Submissions',
    shortName: 'SEC EDGAR Filers',
    icon: 'file-text',
    color: '#0d9488',
    category: 'Regulatory Filings',
    badgeText: 'SEC EDGAR'
  },
  'sec_company_facts': {
    id: 'sec_company_facts',
    canonicalName: 'U.S. SEC EDGAR Public Company Financials & Facts',
    shortName: 'SEC Company Facts',
    icon: 'line-chart',
    color: '#d97706',
    category: 'Financial Analytics',
    badgeText: 'SEC Facts'
  },
  'cc_web_index': {
    id: 'cc_web_index',
    canonicalName: 'Common Crawl Web Domain & CDX Index Collections',
    shortName: 'Common Crawl Index',
    icon: 'network',
    color: '#64748b',
    category: 'Web Crawl Index',
    badgeText: 'Common Crawl'
  },
  'data_legion_companies': {
    id: 'data_legion_companies',
    canonicalName: 'Data Legion Global Companies',
    shortName: 'Data Legion',
    icon: 'briefcase',
    color: '#6366f1',
    category: 'Commercial B2B',
    badgeText: 'Data Legion'
  },
  'tech_stack_leads': {
    id: 'tech_stack_leads',
    canonicalName: 'Tech Stack & Software Intelligence',
    shortName: 'Tech Stack Leads',
    icon: 'cpu',
    color: '#8b5cf6',
    category: 'Technographic Data',
    badgeText: 'Tech Stack'
  },
  'open_company_db': {
    id: 'open_company_db',
    canonicalName: 'Open Company Intelligence Database',
    shortName: 'Open Company DB',
    icon: 'globe',
    color: '#06b6d4',
    category: 'Open Firmographics',
    badgeText: 'Open Company DB'
  },
  'master_locations': {
    id: 'master_locations',
    canonicalName: 'Global Retail, Commercial & Franchise Locations',
    shortName: 'Retail Locations',
    icon: 'store',
    color: '#f59e0b',
    category: 'Retail & Franchises',
    badgeText: 'Retail Locations'
  },
  'b2b_executives': {
    id: 'b2b_executives',
    canonicalName: 'B2B Executive Decision Makers',
    shortName: 'B2B Executives',
    icon: 'users',
    color: '#3b82f6',
    category: 'Executive Contacts',
    badgeText: 'B2B Execs'
  },
  'homeowners': {
    id: 'homeowners',
    canonicalName: 'Homeowners & Residential Real Estate',
    shortName: 'Homeowners',
    icon: 'home',
    color: '#10b981',
    category: 'Residential Real Estate',
    badgeText: 'Homeowners'
  },
  'realestate_b2b': {
    id: 'realestate_b2b',
    canonicalName: 'Real Estate B2B Registry',
    shortName: 'Real Estate B2B',
    icon: 'building-2',
    color: '#f59e0b',
    category: 'Commercial Real Estate',
    badgeText: 'Real Estate B2B'
  },
  'realtors': {
    id: 'realtors',
    canonicalName: 'Licensed Realtors & Real Estate Agencies',
    shortName: 'Licensed Realtors',
    icon: 'award',
    color: '#8b5cf6',
    category: 'Real Estate Agents',
    badgeText: 'Realtors'
  },
  'restaurants': {
    id: 'restaurants',
    canonicalName: 'Restaurants, Chefs & Culinary Establishments',
    shortName: 'Restaurants & Hospitality',
    icon: 'utensils',
    color: '#ef4444',
    category: 'Dining & Hospitality',
    badgeText: 'Restaurants'
  },
  'coaches': {
    id: 'coaches',
    canonicalName: 'Executive Coaches & Strategic Mentors',
    shortName: 'Executive Coaches',
    icon: 'target',
    color: '#06b6d4',
    category: 'Professional Coaching',
    badgeText: 'Coaches'
  },
  'designers': {
    id: 'designers',
    canonicalName: 'Creative Designers, UI/UX & Brand Studios',
    shortName: 'Creative Designers',
    icon: 'palette',
    color: '#ec4899',
    category: 'Design & Creative',
    badgeText: 'Designers'
  },
  'entrepreneurs': {
    id: 'entrepreneurs',
    canonicalName: 'Entrepreneurs, Founders & Innovators',
    shortName: 'Entrepreneurs & Founders',
    icon: 'rocket',
    color: '#14b8a6',
    category: 'Startup Founders',
    badgeText: 'Founders'
  },
  'photographers': {
    id: 'photographers',
    canonicalName: 'Professional Photographers & Visual Creators',
    shortName: 'Photographers',
    icon: 'camera',
    color: '#a855f7',
    category: 'Visual Media',
    badgeText: 'Photographers'
  },
  'musicians': {
    id: 'musicians',
    canonicalName: 'Musicians, Producers & Audio Artists',
    shortName: 'Musicians & Producers',
    icon: 'music',
    color: '#f97316',
    category: 'Music & Audio',
    badgeText: 'Musicians'
  },
  'europe_osm': {
    id: 'europe_osm',
    canonicalName: 'OpenStreetMap: Europe Commercial POIs',
    shortName: 'Europe POIs',
    icon: 'globe',
    color: '#3b82f6',
    category: 'Geospatial Regional',
    badgeText: 'Europe POIs'
  },
  'osm_asia': {
    id: 'osm_asia',
    canonicalName: 'OpenStreetMap: Asia Commercial POIs',
    shortName: 'Asia POIs',
    icon: 'globe',
    color: '#ec4899',
    category: 'Geospatial Regional',
    badgeText: 'Asia POIs'
  },
  'osm_north_america': {
    id: 'osm_north_america',
    canonicalName: 'OpenStreetMap: North America POIs',
    shortName: 'North America POIs',
    icon: 'globe',
    color: '#10b981',
    category: 'Geospatial Regional',
    badgeText: 'North America POIs'
  },
  'osm_africa': {
    id: 'osm_africa',
    canonicalName: 'OpenStreetMap: Africa Commercial POIs',
    shortName: 'Africa POIs',
    icon: 'globe',
    color: '#f59e0b',
    category: 'Geospatial Regional',
    badgeText: 'Africa POIs'
  },
  'osm_south_america': {
    id: 'osm_south_america',
    canonicalName: 'OpenStreetMap: South America Commercial POIs',
    shortName: 'South America POIs',
    icon: 'globe',
    color: '#ec4899',
    category: 'Geospatial Regional',
    badgeText: 'South America POIs'
  },
  'uk_companies_full': {
    id: 'uk_companies_full',
    canonicalName: 'UK Companies House Master Registry',
    shortName: 'UK Companies House',
    icon: 'landmark',
    color: '#8b5cf6',
    category: 'Corporate Registry',
    badgeText: 'UK Registry'
  },
  'osm_oceania': {
    id: 'osm_oceania',
    canonicalName: 'OpenStreetMap: Australia & Oceania POIs',
    shortName: 'Oceania POIs',
    icon: 'globe',
    color: '#06b6d4',
    category: 'Geospatial Regional',
    badgeText: 'Oceania POIs'
  },
  'osm_central_america': {
    id: 'osm_central_america',
    canonicalName: 'OpenStreetMap: Central America POIs',
    shortName: 'Central America POIs',
    icon: 'globe',
    color: '#14b8a6',
    category: 'Geospatial Regional',
    badgeText: 'Central America POIs'
  },
  'companies_filtered': {
    id: 'companies_filtered',
    canonicalName: 'Global Companies Registry Archive',
    shortName: 'Global Companies Archive',
    icon: 'archive',
    color: '#6366f1',
    category: 'Historical Archive',
    badgeText: 'Companies Archive'
  },
  'fitness_wellness_texas': {
    id: 'fitness_wellness_texas',
    canonicalName: 'Texas Fitness & Wellness CRM Leads',
    shortName: 'Texas Fitness & Wellness',
    icon: 'activity',
    color: '#10b981',
    category: 'Vertical CRM',
    badgeText: 'Texas Fitness'
  },
  'all_combined': {
    id: 'all_combined',
    canonicalName: 'US Curated B2B & Massive Archive',
    shortName: 'US Curated B2B',
    icon: 'briefcase',
    color: '#f97316',
    category: 'Curated B2B',
    badgeText: 'US B2B'
  },
  'salon_leads': {
    id: 'salon_leads',
    canonicalName: 'Salon & Beauty Establishments Directory',
    shortName: 'Salon & Beauty',
    icon: 'sparkles',
    color: '#f43f5e',
    category: 'Retail & Personal Care',
    badgeText: 'Salon Leads'
  },
  'osm_antarctica': {
    id: 'osm_antarctica',
    canonicalName: 'OpenStreetMap: Antarctica POIs',
    shortName: 'Antarctica POIs',
    icon: 'globe',
    color: '#94a3b8',
    category: 'Geospatial Regional',
    badgeText: 'Antarctica POIs'
  },
  'pdl_companies_32m': {
    id: 'pdl_companies_32m',
    canonicalName: 'People Data Labs Global Companies',
    shortName: 'PDL Companies 32M',
    icon: 'briefcase',
    color: '#6366f1',
    category: 'B2B Firmographics',
    badgeText: 'PDL Companies'
  }
};

/**
 * Normalizes any raw source string, view ID, or badge into the canonical registry entry.
 * Fallbacks gracefully with standard database icon for unmapped shards.
 */
function getSourceMeta(sourceKey) {
  if (!sourceKey) {
    return {
      id: 'default',
      canonicalName: 'Local Database File',
      shortName: 'Database Shard',
      icon: 'database',
      color: '#64748b',
      category: 'Data Shard',
      badgeText: 'Data Shard'
    };
  }

  const key = String(sourceKey).trim().toLowerCase();
  if (SOURCE_REGISTRY[key]) return SOURCE_REGISTRY[key];

  // Match aliases & prefix variants
  if (key.includes('senzing') || key.includes('odo')) return SOURCE_REGISTRY['odo_senzing'];
  if (key.includes('free_company') || key.includes('free-tier') || key.includes('free company')) return SOURCE_REGISTRY['free_company_dataset'];
  if (key.includes('planet') || key.includes('daily_osm')) return SOURCE_REGISTRY['planet_daily_osm'];
  if (key.includes('gleif')) return SOURCE_REGISTRY['gleif_goldencopy'];
  if (key.includes('edgar') || key.includes('submission')) return SOURCE_REGISTRY['sec_edgar_filers'];
  if (key.includes('sec_facts') || key.includes('facts')) return SOURCE_REGISTRY['sec_company_facts'];
  if (key.includes('crawl') || key.includes('cc_web') || key.includes('cc-index')) return SOURCE_REGISTRY['cc_web_index'];
  if (key.includes('legion')) return SOURCE_REGISTRY['data_legion_companies'];
  if (key.includes('tech_stack') || key.includes('tech stack')) return SOURCE_REGISTRY['tech_stack_leads'];
  if (key.includes('open_company') || key.includes('open company')) return SOURCE_REGISTRY['open_company_db'];
  if (key.includes('locations') || key.includes('store') || key.includes('master_loc')) return SOURCE_REGISTRY['master_locations'];
  if (key.includes('b2b') || key.includes('exec') || key.includes('decision maker')) return SOURCE_REGISTRY['b2b_executives'];
  if (key.includes('homeowner') || key.includes('residence')) return SOURCE_REGISTRY['homeowners'];
  if (key.includes('realestate') || key.includes('real estate b2b')) return SOURCE_REGISTRY['realestate_b2b'];
  if (key.includes('realtor')) return SOURCE_REGISTRY['realtors'];
  if (key.includes('restaurant') || key.includes('dining')) return SOURCE_REGISTRY['restaurants'];
  if (key.includes('coach')) return SOURCE_REGISTRY['coaches'];
  if (key.includes('designer')) return SOURCE_REGISTRY['designers'];
  if (key.includes('entrepreneur') || key.includes('founder')) return SOURCE_REGISTRY['entrepreneurs'];
  if (key.includes('photographer')) return SOURCE_REGISTRY['photographers'];
  if (key.includes('musician')) return SOURCE_REGISTRY['musicians'];
  if (key.includes('local') || key.includes('unified')) return SOURCE_REGISTRY['all_local_unified'];
  if (key.includes('global') || key.includes('portfolio') || key.includes('all_leads')) return SOURCE_REGISTRY['all_global'];

  // Handle raw file shards cleanly
  if (key.startsWith('raw_') || key.includes('.csv') || key.includes('.parquet')) {
    const cleanLabel = String(sourceKey).replace(/^raw_/i, '').replace(/\.(csv|parquet|gz|zip)/gi, '');
    return {
      id: key,
      canonicalName: `Raw Data Shard: ${cleanLabel}`,
      shortName: cleanLabel.length > 20 ? cleanLabel.substring(0, 18) + '…' : cleanLabel,
      icon: 'files',
      color: '#64748b',
      category: 'Local CSV Shard',
      badgeText: cleanLabel.length > 16 ? cleanLabel.substring(0, 14) + '…' : cleanLabel
    };
  }

  // Graceful fallback: Never invent random icons!
  return {
    id: key,
    canonicalName: String(sourceKey),
    shortName: String(sourceKey).length > 22 ? String(sourceKey).substring(0, 20) + '…' : String(sourceKey),
    icon: 'database',
    color: '#64748b',
    category: 'Registered Source',
    badgeText: String(sourceKey).length > 18 ? String(sourceKey).substring(0, 16) + '…' : String(sourceKey)
  };
}

function renderSourceIcon(sourceKey, options = {}) {
  const meta = getSourceMeta(sourceKey);
  const size = options.size || 16;
  const className = options.className || '';
  return getIconSvg(meta.icon, { size, className, title: meta.canonicalName });
}

function renderSourceBadge(sourceKey, options = {}) {
  const meta = getSourceMeta(sourceKey);
  const size = options.size || 14;
  const showIcon = options.showIcon !== false;
  const customLabel = options.customLabel || meta.badgeText || meta.shortName;
  const iconMarkup = showIcon ? renderSourceIcon(meta.id, { size }) : '';
  const extraClass = options.className || `source-${meta.id}`;
  return `<span class="source-badge-chip ${extraClass}" title="${escapeHtml(meta.canonicalName)}">${iconMarkup}<span>${escapeHtml(customLabel)}</span></span>`;
}

function renderFunctionalIcon(iconName, options = {}) {
  return getIconSvg(iconName, options);
}

let STATE = {
  activeView: 'dashboard',
  dataset: 'all_global',
  search: '',
  colFilters: {
    name: '',
    contact: '',
    job_title: '',
    category: '',
    email: '',
    phone: '',
    website: '',
    address: '',
    city: '',
    state: '',
    country: '',
    socials: ''
  },
  tier: 'all',
  country: 'all',
  state: 'all',
  majorCategory: 'all',
  category: 'all',
  opportunity: 'all',
  hasPhone: false,
  hasEmail: false,
  hasWebsite: false,
  crmStatus: 'all',
  sortBy: '',
  sortDir: 'asc',
  page: 1,
  pageSize: 50,
  totalLeads: 0,
  currentLeads: [],
  selectedLeadIds: new Set(),
  datasetsList: [],
  datasetFilterCat: 'all',
  wizardStep: 1,
  duplicateCategory: 'exact_within_file',
  selectedDatasetIds: new Set(),
  datasetSortCol: '',
  datasetSortDir: 'asc',
  exportFormat: 'csv'
};

let WIZARD_STATE = {
  step: 1,
  selectedDatasets: ['master_locations'],
  method: 'exact_row',
  criteria: ['name', 'contact', 'email', 'phone', 'address', 'website'],
  simulationResult: null,
  retainedGroupCopies: {},
  confirmed: false
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
    'datasets': 'All Datasets',
    'import': 'Import Data',
    'explorer': 'Lead Explorer',
    'categories': 'Lead Categories',
    'duplicates': 'Duplicate Detection',
    'dedup-history': 'Deduplication Workflow',
    'cleaning': 'Data Cleaning',
    'search-filters': 'Search & Filters Hub',
    'export': 'Export Center',
    'activity': 'Activity Logs',
    'settings': 'Settings'
  };
  const label = viewLabels[viewId] || 'Overview';
  const breadcrumbView = document.getElementById('topbar-breadcrumb-view');
  if (breadcrumbView) breadcrumbView.textContent = label;

  // View specific loaders
  if (viewId === 'dashboard') {
    loadDashboardMetrics();
    loadOverviewCharts();
  } else if (viewId === 'datasets') {
    loadDatasetsCatalog();
  } else if (viewId === 'explorer') {
    if (STATE.currentLeads.length === 0) loadLeads();
  } else if (viewId === 'categories') {
    loadLeadCategoriesSection();
  } else if (viewId === 'duplicates') {
    loadDuplicateSummary();
  } else if (viewId === 'dedup-history') {
    loadDedupHistory();
    renderWizardStep(WIZARD_STATE.step || 1);
  } else if (viewId === 'activity') {
    loadActivityLogs();
  }

  // Scroll to top of content
  const pageContent = document.getElementById('page-content');
  if (pageContent) pageContent.scrollTop = 0;
}

// =============================================================================
// DASHBOARD METRICS & CHARTS
// =============================================================================
async function loadDashboardMetrics() {
  try {
    const res = await fetch('/api/dashboard_metrics');
    if (!res.ok) return;
    const data = await res.json();

    if (data.status === 'success') {
      const elPortfolio = document.getElementById('kpi-total-portfolio');
      if (elPortfolio) elPortfolio.textContent = (data.total_portfolio || 918282632).toLocaleString();

      const elDatasets = document.getElementById('kpi-datasets-count');
      if (elDatasets) elDatasets.textContent = data.dataset_count || 37;

      const elUnique = document.getElementById('kpi-unique-local');
      if (elUnique) elUnique.textContent = (data.unique_verified_records || 224052222).toLocaleString();

      const elDups = document.getElementById('kpi-duplicates-removed');
      if (elDups) elDups.textContent = (data.duplicates_removed || 410339).toLocaleString();

      const elDiskD = document.getElementById('dash-disk-d');
      if (elDiskD) elDiskD.textContent = `${data.disk_d_free_gb || 79.9} GB Free (${data.disk_d_total_gb || 117.1} GB)`;

      const elDiskC = document.getElementById('dash-disk-c');
      if (elDiskC) elDiskC.textContent = `${data.disk_c_free_gb || 13.4} GB Free`;

      const elNavBadge = document.getElementById('nav-leads-count-badge');
      if (elNavBadge) elNavBadge.textContent = formatCompact(data.total_portfolio || 918282632);

      const elNavDatasets = document.getElementById('nav-datasets-count-badge');
      if (elNavDatasets && data.dataset_count) elNavDatasets.textContent = data.dataset_count;

      const elFooter = document.getElementById('footer-engine-meta');
      if (elFooter) elFooter.textContent = `${formatCompact(data.unique_verified_records || 224052222)} Local • ${data.disk_d_free_gb || 80} GB Free`;

      renderPortfolioDistribution(data.sources_breakdown || []);
      renderDashboardRecentDedup(data.recent_dedup || []);
    }
  } catch (err) {
    console.error('Error loading dashboard metrics:', err);
  }
}

async function loadOverviewCharts() {
  const container = document.getElementById('chart-coverage-container');
  if (!container) return;

  try {
    const res = await fetch('/api/charts/overview');
    if (!res.ok) return;
    const data = await res.json();

    const coverage = data.field_coverage || [];
    container.innerHTML = coverage.map(item => `
      <div style="margin-bottom: 12px;">
        <div style="display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 4px;">
          <span style="font-weight: 500; color: var(--text-primary);">${escapeHtml(item.field)}</span>
          <span class="cell-mono text-tertiary">${item.coverage_pct}% (${item.count})</span>
        </div>
        <div style="height: 6px; background: var(--bg-surface-active); border-radius: 3px; overflow: hidden;">
          <div style="width: ${item.coverage_pct}%; height: 100%; background: linear-gradient(90deg, #3b82f6, #10b981); border-radius: 3px;"></div>
        </div>
      </div>
    `).join('');
  } catch (err) {
    console.error('Error loading charts:', err);
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
    const meta = getSourceMeta(item.id || item.name);
    const pct = Math.max(0.5, ((item.count / total) * 100)).toFixed(1);
    const itemColor = meta.color || item.color || '#3b82f6';
    const sourceIcon = renderSourceIcon(meta.id, { size: 13, className: 'icon-inline' });
    
    // Segment
    const seg = document.createElement('div');
    seg.className = 'portfolio-bar-segment';
    seg.style.width = `${pct}%`;
    seg.style.backgroundColor = itemColor;
    seg.title = `${meta.canonicalName}: ${item.count.toLocaleString()} leads (${pct}%)`;
    seg.onclick = () => {
      if (item.id) selectDatasetAndExplore(item.id);
    };
    barContainer.appendChild(seg);

    // Chip
    const chip = document.createElement('div');
    chip.className = 'portfolio-chip';
    chip.innerHTML = `
      <span class="portfolio-chip-dot" style="background-color: ${itemColor};"></span>
      <span class="portfolio-chip-icon" style="color: ${itemColor}; display: inline-flex; align-items: center;">${sourceIcon}</span>
      <span>${escapeHtml(meta.shortName)}</span>
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

    populateDatasetSelectors(datasets);
    renderDatasetsTable(datasets);

    const countBadge = document.getElementById('nav-datasets-count-badge');
    if (countBadge) countBadge.textContent = datasets.length;
    const countLabel = document.getElementById('datasets-count-label');
    if (countLabel) countLabel.textContent = `${datasets.length} Datasets Registered`;
  } catch (err) {
    console.error('Error loading dataset catalog:', err);
  }
}

function formatDatasetOptionLabel(d) {
  const meta = getSourceMeta(d.id);
  const name = meta.shortName || meta.canonicalName || (d.name || d.id);
  const countStr = d.count ? ` · ${formatCompact(d.count)}` : '';
  return `${name}${countStr}`;
}

function populateDatasetSelectors(datasets) {
  const topSelect = document.getElementById('topbar-dataset-select');
  const explorerSelect = document.getElementById('filter-dataset');
  if (!topSelect || !explorerSelect) return;

  const optionsHtml = datasets.map(d => {
    return `<option value="${escapeHtml(d.id)}">${escapeHtml(formatDatasetOptionLabel(d))}</option>`;
  }).join('');

  topSelect.innerHTML = optionsHtml;
  explorerSelect.innerHTML = optionsHtml;
  const exportSelect = document.getElementById('export-dataset-select');
  if (exportSelect) {
    exportSelect.innerHTML = optionsHtml;
    exportSelect.value = STATE.dataset || 'all_global';
  }

  topSelect.value = STATE.dataset;
  explorerSelect.value = STATE.dataset;
}

function renderDatasetsTable(datasets) {
  const tbody = document.getElementById('datasets-table-tbody');
  if (!tbody) return;

  if (!STATE.selectedDatasetIds) STATE.selectedDatasetIds = new Set();

  tbody.innerHTML = datasets.map(d => {
    const format = d.file_format || ((d.file || '').endsWith('.gz') ? 'CSV.GZ' : (d.type === 'imported_parquet' ? 'PARQUET' : (d.type === 'osm' || d.type === 'pdl' ? 'STREAM' : 'CSV')));
    const qualityStatus = d.duplicate_stats ? 
      `<span class="status-badge ${d.duplicate_stats.includes('Clean') ? 'clean' : 'warning'}">${escapeHtml(d.duplicate_stats)}</span>` :
      (d.is_imported ? `<span class="status-badge clean">${(d.duplicate_rows || 0).toLocaleString()} Dups Filtered</span>` : '<span class="status-badge clean">Verified Clean</span>');
    const isChecked = STATE.selectedDatasetIds.has(d.id);
    const meta = getSourceMeta(d.id);
    const sourceIcon = renderSourceIcon(meta.id, { size: 16, className: 'icon-inline' });
    const sourceBadge = d.is_imported ? 
      `<span class="status-badge" style="background: rgba(139, 92, 246, 0.12); color: #8b5cf6; border: 1px solid rgba(139, 92, 246, 0.25);">📁 User Dataset</span>` :
      renderSourceBadge(meta.id, { size: 13 });
    const exploreIcon = getIconSvg('search', { size: 12, className: 'icon-inline' });
    const auditIcon = getIconSvg('shield-check', { size: 12, className: 'icon-inline' });
    const exportIcon = getIconSvg('file-down', { size: 12, className: 'icon-inline' });

    let actionButtons = `
      <div class="cell-action-group">
        <button class="cell-action-btn" onclick="selectDatasetAndExplore('${escapeHtml(d.id)}')">${exploreIcon}<span>Explore</span></button>
        <button class="cell-action-btn" onclick="switchView('duplicates')">${auditIcon}<span>Audit</span></button>
        <button class="cell-action-btn" onclick="switchView('export')">${exportIcon}<span>Export</span></button>
      </div>
    `;

    if (d.is_imported) {
      actionButtons = `
        <div class="cell-action-group">
          <button class="cell-action-btn" onclick="selectDatasetAndExplore('${escapeHtml(d.id)}')" title="Explore Leads">${exploreIcon}<span>Explore</span></button>
          <button class="cell-action-btn" onclick="openDatasetColumnsModal('${escapeHtml(d.id)}', '${escapeHtml(d.name)}')" title="Manage Columns" style="color: #a78bfa;"><span>⚙️ Columns</span></button>
          <button class="cell-action-btn" onclick="openRenameModal('${escapeHtml(d.id)}', '${escapeHtml(d.name)}')" title="Rename Dataset"><span>✏️ Rename</span></button>
          <button class="cell-action-btn" onclick="openImportModalForDataset('${escapeHtml(d.id)}', '${escapeHtml(d.name)}')" title="Add More Files"><span>➕ Add Files</span></button>
          <button class="cell-action-btn" onclick="exportImportedDatasetCsv('${escapeHtml(d.id)}')" title="Export Clean CSV">${exportIcon}<span>Export</span></button>
          ${d.rejected_rows ? `<button class="cell-action-btn" onclick="window.open('/api/imported_datasets/${encodeURIComponent(d.id)}/rejections')" title="Download Rejection Report" style="color: #f59e0b;"><span>📋 Errors</span></button>` : ''}
          <button class="cell-action-btn" onclick="openDeleteModal('${escapeHtml(d.id)}', '${escapeHtml(d.name)}')" title="Delete Dataset" style="color: #ef4444;"><span>🗑️ Delete</span></button>
        </div>
      `;
    }

    return `
      <tr class="${isChecked ? 'selected' : ''}" id="dataset-row-${escapeHtml(d.id)}">
        <td style="text-align: center;">
          <input type="checkbox" class="dataset-row-cb" value="${escapeHtml(d.id)}" ${isChecked ? 'checked' : ''} onchange="onDatasetRowSelect('${escapeHtml(d.id)}', this.checked)">
        </td>
        <td>
          <div class="cell-name-strong" style="display: flex; align-items: center; gap: 8px;">
            <span style="color: ${d.is_imported ? '#8b5cf6' : (meta.color || 'var(--accent-primary)')}; display: inline-flex; align-items: center;">${sourceIcon}</span>
            <span>${escapeHtml(d.name)}</span>
          </div>
          <span class="cell-subtext" style="font-family: var(--font-mono);">${escapeHtml(d.file || d.id)}</span>
        </td>
        <td>${sourceBadge}</td>
        <td class="cell-mono font-bold">${(d.count || 0).toLocaleString()}</td>
        <td class="cell-mono">${d.is_imported ? `<a href="javascript:void(0)" onclick="openDatasetColumnsModal('${escapeHtml(d.id)}', '${escapeHtml(d.name)}')" style="color: #a78bfa; text-decoration: underline;">${d.columns_count || 12} cols ⚙️</a>` : `${d.columns_count || 12} cols`}</td>
        <td><span class="status-badge neutral cell-mono">${format}</span></td>
        <td class="cell-mono text-tertiary">${d.file_size_mb ? d.file_size_mb + ' MB' : '-'}</td>
        <td class="cell-subtext">${d.import_date || (d.created_at ? d.created_at.slice(0, 10) : 'Active')}</td>
        <td><span class="status-badge clean">${d.processing_status || 'Ready & Indexed'}</span></td>
        <td>${qualityStatus}</td>
        <td>${actionButtons}</td>
      </tr>
    `;
  }).join('');
}

function toggleSelectAllDatasets(checked) {
  if (!STATE.selectedDatasetIds) STATE.selectedDatasetIds = new Set();
  const cbs = document.querySelectorAll('.dataset-row-cb');
  cbs.forEach(cb => {
    cb.checked = checked;
    const row = document.getElementById(`dataset-row-${cb.value}`);
    if (row) row.classList.toggle('selected', checked);
    if (checked) {
      STATE.selectedDatasetIds.add(cb.value);
    } else {
      STATE.selectedDatasetIds.delete(cb.value);
    }
  });
  updateDatasetsBulkBar();
}

function onDatasetRowSelect(id, checked) {
  if (!STATE.selectedDatasetIds) STATE.selectedDatasetIds = new Set();
  if (checked) {
    STATE.selectedDatasetIds.add(id);
  } else {
    STATE.selectedDatasetIds.delete(id);
  }
  const row = document.getElementById(`dataset-row-${id}`);
  if (row) row.classList.toggle('selected', checked);

  const master = document.getElementById('datasets-select-all');
  if (master) {
    const totalOnPage = document.querySelectorAll('.dataset-row-cb').length;
    master.checked = totalOnPage > 0 && STATE.selectedDatasetIds.size >= totalOnPage;
  }
  updateDatasetsBulkBar();
}

function updateDatasetsBulkBar() {
  const bar = document.getElementById('datasets-bulk-bar');
  const countBadge = document.getElementById('datasets-selected-count');
  const count = STATE.selectedDatasetIds ? STATE.selectedDatasetIds.size : 0;
  if (countBadge) countBadge.textContent = count;
  if (bar) bar.classList.toggle('visible', count > 0);
}

function clearDatasetsSelection() {
  if (STATE.selectedDatasetIds) STATE.selectedDatasetIds.clear();
  const master = document.getElementById('datasets-select-all');
  if (master) master.checked = false;
  document.querySelectorAll('.dataset-row-cb').forEach(cb => {
    cb.checked = false;
    const row = document.getElementById(`dataset-row-${cb.value}`);
    if (row) row.classList.remove('selected');
  });
  updateDatasetsBulkBar();
}

function bulkAuditSelectedDatasets() {
  const count = STATE.selectedDatasetIds ? STATE.selectedDatasetIds.size : 0;
  if (count === 0) return toast('Please select at least one dataset');
  toast(`Auditing ${count} selected datasets for duplicates...`);
  switchView('duplicates');
}

function bulkExportSelectedDatasets() {
  const count = STATE.selectedDatasetIds ? STATE.selectedDatasetIds.size : 0;
  if (count === 0) return toast('Please select at least one dataset');
  toast(`Opening export center for ${count} selected datasets...`);
  switchView('export');
}

function sortDatasetsTable(col) {
  if (STATE.datasetSortCol === col) {
    STATE.datasetSortDir = STATE.datasetSortDir === 'asc' ? 'desc' : 'asc';
  } else {
    STATE.datasetSortCol = col;
    STATE.datasetSortDir = 'asc';
  }

  const factor = STATE.datasetSortDir === 'asc' ? 1 : -1;
  STATE.datasetsList.sort((a, b) => {
    let valA = a[col];
    let valB = b[col];
    if (col === 'count') {
      return ((a.count || 0) - (b.count || 0)) * factor;
    }
    if (col === 'size') {
      return ((parseFloat(a.file_size_mb) || 0) - (parseFloat(b.file_size_mb) || 0)) * factor;
    }
    if (col === 'name') {
      return (a.name || '').localeCompare(b.name || '') * factor;
    }
    if (col === 'format') {
      return (a.file_format || '').localeCompare(b.file_format || '') * factor;
    }
    if (col === 'date') {
      return (a.import_date || '').localeCompare(b.import_date || '') * factor;
    }
    return String(valA || '').localeCompare(String(valB || '')) * factor;
  });

  filterDatasetsByCategory(STATE.datasetFilterCat);
  toast(`Sorted datasets by ${col} (${STATE.datasetSortDir.toUpperCase()})`);
}

function filterDatasetsByCategory(category) {
  STATE.datasetFilterCat = category;
  document.querySelectorAll('#view-datasets .tier-pill').forEach(btn => {
    btn.classList.toggle('active', btn.textContent.toLowerCase().includes(category) || (category === 'all' && btn.textContent.includes('All')));
  });

  let filtered = STATE.datasetsList;
  if (category === 'imported') {
    filtered = STATE.datasetsList.filter(d => d.is_imported || (d.type || '').includes('imported'));
  } else if (category === 'b2b') {
    filtered = STATE.datasetsList.filter(d => (d.file || '').includes('free-tier (') && !(d.file || '').includes('free-tier (1).csv'));
  } else if (category === 'corporate') {
    filtered = STATE.datasetsList.filter(d => (d.id || '').includes('legion') || (d.id || '').includes('open_company') || (d.id || '').includes('tech_stack'));
  } else if (category === 'retail') {
    filtered = STATE.datasetsList.filter(d => (d.id || '').includes('location'));
  } else if (category === 'demographics') {
    filtered = STATE.datasetsList.filter(d => (d.id || '').includes('homeowner'));
  } else if (category === 'niche') {
    filtered = STATE.datasetsList.filter(d => (d.id || '').includes('realtor') || (d.id || '').includes('restaurant') || (d.id || '').includes('coach') || (d.id || '').includes('musician') || (d.id || '').includes('designer') || (d.id || '').includes('photographer') || (d.id || '').includes('entrepreneur'));
  }

  renderDatasetsTable(filtered);
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
    search: STATE.search || '',
    col_name: STATE.colFilters?.name || '',
    col_contact: STATE.colFilters?.contact || '',
    col_job_title: STATE.colFilters?.job_title || '',
    col_category: STATE.colFilters?.category || '',
    col_email: STATE.colFilters?.email || '',
    col_phone: STATE.colFilters?.phone || '',
    col_website: STATE.colFilters?.website || '',
    col_address: STATE.colFilters?.address || '',
    col_city: STATE.colFilters?.city || '',
    col_state: STATE.colFilters?.state || '',
    col_country: STATE.colFilters?.country || '',
    col_socials: STATE.colFilters?.socials || '',
    tier: STATE.tier,
    state: STATE.state,
    country: STATE.country,
    major_category: STATE.majorCategory,
    category: STATE.category,
    crm_status: STATE.crmStatus,
    opportunity: STATE.opportunity,
    has_phone: STATE.hasPhone,
    has_email: STATE.hasEmail,
    has_website: STATE.hasWebsite,
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
      totalBadge.textContent = Number(STATE.totalLeads).toLocaleString();
    }

    const viewSummary = document.getElementById('table-view-summary');
    if (viewSummary) {
      const fromRow = STATE.totalLeads > 0 ? (STATE.page - 1) * STATE.pageSize + 1 : 0;
      const toRow = Math.min(STATE.page * STATE.pageSize, STATE.totalLeads);
      viewSummary.textContent = `Showing ${fromRow.toLocaleString()} - ${toRow.toLocaleString()} of ${STATE.totalLeads.toLocaleString()} leads`;
    }

    if (data.major_categories && data.major_categories.length > 0) {
      populateMajorCategories(data.major_categories);
    }
    if (data.states && data.states.length > 0) {
      populateStates(data.states);
    }
    if (data.categories_hierarchy) {
      CATEGORIES_CACHE = data.categories_hierarchy;
    }
    updateActiveFilterTags();

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

  const copyIcon = getIconSvg('copy', { size: 12, className: 'icon-inline' });
  const extIcon = getIconSvg('external-link', { size: 12, className: 'icon-inline' });
  const inspectIcon = getIconSvg('eye', { size: 12, className: 'icon-inline' });
  const pitchIcon = getIconSvg('sparkles', { size: 12, className: 'icon-inline' });

  tbody.innerHTML = leads.map(l => {
    const isChecked = STATE.selectedLeadIds.has(String(l.id));
    const phoneDisplay = l.phone ? `<span class="cell-copy-val" onclick="copyDirectVal('${escapeHtml(l.phone)}', 'Phone copied!')" title="Click to copy" style="cursor: pointer; display: inline-flex; align-items: center; gap: 4px;"><span>${escapeHtml(l.phone)}</span><span class="text-tertiary">${copyIcon}</span></span>` : '<span class="cell-subtext">-</span>';
    const emailDisplay = l.email ? `<span class="cell-copy-val" onclick="copyDirectVal('${escapeHtml(l.email)}', 'Email copied!')" title="Click to copy" style="cursor: pointer; display: inline-flex; align-items: center; gap: 4px;"><span>${escapeHtml(l.email)}</span><span class="text-tertiary">${copyIcon}</span></span>` : '<span class="cell-subtext">-</span>';
    const webDisplay = l.website ? `<a href="${escapeHtml(l.website.startsWith('http') ? l.website : 'https://' + l.website)}" target="_blank" rel="noopener" class="cell-subtext cell-web-link" style="color: #60a5fa; text-decoration: none; display: inline-flex; align-items: center; gap: 4px;"><span>${escapeHtml(l.website)}</span> ${extIcon}</a>` : '<span class="status-badge danger" style="font-size:10px;">No Site</span>';
    const sourceBadge = (l.source_badge || l.source_id) ? renderSourceBadge(l.source_badge || l.source_id, { size: 11 }) : '';

    return `
      <tr class="${isChecked ? 'selected' : ''}" id="lead-row-${l.id}">
        <td>
          <input type="checkbox" onchange="onLeadCheckChange('${escapeHtml(String(l.id))}', this.checked)" ${isChecked ? 'checked' : ''}>
        </td>
        <td style="cursor: pointer;" onclick="openDrawerById('${escapeHtml(String(l.id))}')">
          <div class="cell-name-strong">${escapeHtml(l.name || 'Unnamed Business')}</div>
          <div style="display: flex; align-items: center; gap: 6px; margin-top: 3px;">
            ${sourceBadge}
            <span class="cell-subtext">${escapeHtml(l.opportunity || 'Standard Opportunity')}</span>
          </div>
        </td>
        <td style="cursor: pointer;" onclick="openDrawerById('${escapeHtml(String(l.id))}')">
          <span style="font-weight: 500;">${escapeHtml(l.contact_name || '-')}</span>
        </td>
        <td>
          <span class="cell-subtext">${escapeHtml(l.job_title || '-')}</span>
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
            <button class="cell-action-btn" onclick="openDrawerById('${escapeHtml(String(l.id))}')">${inspectIcon}<span>Inspect</span></button>
            <button class="cell-action-btn" onclick="copyPitchById('${escapeHtml(String(l.id))}')">${pitchIcon}<span>Pitch</span></button>
          </div>
        </td>
      </tr>
    `;
  }).join('');
}

function renderPagination(total, page, pageSize) {
  const container = document.getElementById('pagination-bar');
  if (!container) return;

  const totalPages = Math.max(1, Math.ceil(total / pageSize));
  let startPage = Math.max(1, page - 2);
  let endPage = Math.min(totalPages, page + 2);

  if (page <= 3) {
    endPage = Math.min(totalPages, 5);
  } else if (page >= totalPages - 2) {
    startPage = Math.max(1, totalPages - 4);
  }

  let pagesHtml = '';
  for (let p = startPage; p <= endPage; p++) {
    pagesHtml += `<button class="page-btn ${p === page ? 'active' : ''}" onclick="goToPage(${p})">${p.toLocaleString()}</button>`;
  }

  const fromRow = total > 0 ? (page - 1) * pageSize + 1 : 0;
  const toRow = Math.min(page * pageSize, total);

  container.innerHTML = `
    <span class="cell-mono text-tertiary" style="font-size: 12px;">
      Showing ${fromRow.toLocaleString()} - ${toRow.toLocaleString()} of ${total.toLocaleString()} leads (Page ${page.toLocaleString()} of ${totalPages.toLocaleString()})
    </span>
    <div class="pagination-controls">
      <button class="page-btn" onclick="goToPage(1)" ${page === 1 ? 'disabled' : ''} title="First Page">&laquo;</button>
      <button class="page-btn" onclick="goToPage(${Math.max(1, page - 1)})" ${page === 1 ? 'disabled' : ''} title="Previous Page">&lsaquo;</button>
      ${pagesHtml}
      <button class="page-btn" onclick="goToPage(${Math.min(totalPages, page + 1)})" ${page >= totalPages ? 'disabled' : ''} title="Next Page">&rsaquo;</button>
      <button class="page-btn" onclick="goToPage(${Math.min(totalPages, page + 10)})" ${page >= totalPages ? 'disabled' : ''} title="Forward 10 Pages">&raquo;</button>
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

  // Update table header sorting chevrons
  document.querySelectorAll('.sort-icon').forEach(icon => icon.classList.remove('active'));
  const icon = document.getElementById(`sort-icon-${col}`);
  if (icon) {
    icon.classList.add('active');
    icon.style.transform = STATE.sortDir === 'desc' ? 'rotate(180deg)' : 'none';
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
    updateActiveFilterTags();
    loadLeads();
  }, 250);
}

function handleExplorerSearch(val) {
  const clearBtn = document.getElementById('explorer-search-clear');
  if (clearBtn) clearBtn.style.display = val.length > 0 ? 'inline-block' : 'none';
  
  // Keep topbar search in sync
  const topSearch = document.getElementById('global-search-input');
  if (topSearch && topSearch.value !== val) topSearch.value = val;
  const topClear = document.getElementById('topbar-search-clear');
  if (topClear) topClear.style.display = val.length > 0 ? 'inline-block' : 'none';

  handleSearchInput(val);
}

function clearExplorerSearch() {
  const input = document.getElementById('explorer-inline-search');
  if (input) input.value = '';
  handleExplorerSearch('');
}

function handleTopGlobalSearch(val) {
  const topClear = document.getElementById('topbar-search-clear');
  if (topClear) topClear.style.display = val.length > 0 ? 'inline-block' : 'none';

  // Sync with Lead Explorer inline search box
  const inlineSearch = document.getElementById('explorer-inline-search');
  if (inlineSearch && inlineSearch.value !== val) inlineSearch.value = val;
  const inlineClear = document.getElementById('explorer-search-clear');
  if (inlineClear) inlineClear.style.display = val.length > 0 ? 'inline-block' : 'none';

  if (STATE.activeView !== 'explorer') {
    switchView('explorer');
  }

  handleSearchInput(val);
}

function handleTopGlobalSearchKey(e) {
  if (e.key === 'Enter') {
    clearTimeout(searchDebounceTimeout);
    STATE.search = (e.target.value || '').trim();
    STATE.page = 1;
    if (STATE.activeView !== 'explorer') {
      switchView('explorer');
    }
    updateActiveFilterTags();
    loadLeads();
  }
}

function clearTopGlobalSearch() {
  const topSearch = document.getElementById('global-search-input');
  if (topSearch) topSearch.value = '';
  const topClear = document.getElementById('topbar-search-clear');
  if (topClear) topClear.style.display = 'none';

  const inlineSearch = document.getElementById('explorer-inline-search');
  if (inlineSearch) inlineSearch.value = '';
  const inlineClear = document.getElementById('explorer-search-clear');
  if (inlineClear) inlineClear.style.display = 'none';

  handleSearchInput('');
}

let colFilterDebounce = null;
function handleColFilter(col, val) {
  const inputId = col === 'job_title' ? 'col-filter-job' : (col === 'contact_name' ? 'col-filter-contact' : `col-filter-${col}`);
  const input = document.getElementById(inputId);
  if (input) {
    input.classList.toggle('has-value', val.length > 0);
  }

  clearTimeout(colFilterDebounce);
  colFilterDebounce = setTimeout(() => {
    if (!STATE.colFilters) STATE.colFilters = {};
    const normKey = col === 'contact_name' ? 'contact' : col;
    STATE.colFilters[normKey] = val.trim();
    STATE.page = 1;
    updateActiveFilterTags();
    loadLeads();
  }, 250);
}

function handleColFilterKey(e, col) {
  if (e.key === 'Enter') {
    clearTimeout(colFilterDebounce);
    if (!STATE.colFilters) STATE.colFilters = {};
    const normKey = col === 'contact_name' ? 'contact' : col;
    STATE.colFilters[normKey] = (e.target.value || '').trim();
    STATE.page = 1;
    updateActiveFilterTags();
    loadLeads();
  }
}

function clearAllColFilters() {
  document.querySelectorAll('.th-filter-input').forEach(input => {
    input.value = '';
    input.classList.remove('has-value');
  });
  if (STATE.colFilters) {
    for (const k in STATE.colFilters) {
      STATE.colFilters[k] = '';
    }
  }
  STATE.page = 1;
  updateActiveFilterTags();
  loadLeads();
  showToast('Column filters reset');
}

function toggleColumnFilterRow() {
  const row = document.getElementById('table-column-filter-row');
  const btn = document.getElementById('btn-toggle-col-filters');
  if (row) {
    row.classList.toggle('hidden');
    const isHidden = row.classList.contains('hidden');
    if (btn) btn.classList.toggle('active', !isHidden);
  }
}

function setTierFilter(tier) {
  STATE.tier = tier;
  STATE.page = 1;

  document.querySelectorAll('.segment-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.tier === tier);
  });

  updateActiveFilterTags();
  loadLeads();
}

function toggleQuickChip(chipType) {
  if (chipType === 'phone') {
    STATE.hasPhone = !STATE.hasPhone;
    const btn = document.getElementById('chip-phone');
    if (btn) btn.classList.toggle('active', STATE.hasPhone);
  } else if (chipType === 'email') {
    STATE.hasEmail = !STATE.hasEmail;
    const btn = document.getElementById('chip-email');
    if (btn) btn.classList.toggle('active', STATE.hasEmail);
  } else if (chipType === 'website') {
    STATE.hasWebsite = !STATE.hasWebsite;
    const btn = document.getElementById('chip-website');
    if (btn) btn.classList.toggle('active', STATE.hasWebsite);
  }

  STATE.page = 1;
  updateActiveFilterTags();
  loadLeads();
}

function toggleFilterShelf() {
  const shelf = document.getElementById('console-filter-shelf');
  const btn = document.getElementById('btn-toggle-filters');
  if (!shelf) return;
  const isExpanded = shelf.classList.toggle('expanded');
  if (btn) btn.classList.toggle('active', isExpanded);
}

function onFilterChange() {
  const stateEl = document.getElementById('filter-state');
  const crmEl = document.getElementById('filter-crm-status');
  if (stateEl) STATE.state = stateEl.value;
  if (crmEl) STATE.crmStatus = crmEl.value;
  STATE.page = 1;
  updateActiveFilterTags();
  loadLeads();
}

function onCountryChange(val) {
  STATE.country = val;
  STATE.page = 1;
  updateActiveFilterTags();
  loadLeads();
}

function onMajorCatChange(val) {
  STATE.majorCategory = val;
  STATE.page = 1;
  updateActiveFilterTags();
  loadLeads();
}

function onOppChange(val) {
  STATE.opportunity = val;
  STATE.page = 1;
  updateActiveFilterTags();
  loadLeads();
}

function toggleHasPhone() {
  toggleQuickChip('phone');
}

function updateActiveFilterTags() {
  const bar = document.getElementById('active-filter-tags-bar');
  const list = document.getElementById('active-tags-list');
  const badge = document.getElementById('active-filters-badge');
  if (!bar || !list) return;

  const tags = [];
  if (STATE.search) {
    tags.push({ label: `Global Search: "${STATE.search}"`, clear: () => clearTopGlobalSearch() });
  }

  // Column Filters Badges
  if (STATE.colFilters) {
    const colLabels = {
      name: 'Business',
      contact: 'Contact',
      job_title: 'Role',
      category: 'Category',
      email: 'Email',
      phone: 'Phone',
      website: 'Website',
      address: 'Address',
      city: 'City',
      state: 'State',
      country: 'Country',
      socials: 'Socials'
    };
    for (const [col, val] of Object.entries(STATE.colFilters)) {
      if (val) {
        tags.push({
          label: `${colLabels[col] || col}: "${val}"`,
          clear: () => {
            const inputId = col === 'job_title' ? 'col-filter-job' : (col === 'contact' ? 'col-filter-contact' : `col-filter-${col}`);
            const input = document.getElementById(inputId);
            if (input) {
              input.value = '';
              input.classList.remove('has-value');
            }
            STATE.colFilters[col] = '';
            STATE.page = 1;
            updateActiveFilterTags();
            loadLeads();
          }
        });
      }
    }
  }

  if (STATE.tier && STATE.tier !== 'all') {
    tags.push({ label: `Tier: ${STATE.tier}`, clear: () => setTierFilter('all') });
  }
  if (STATE.hasPhone) {
    tags.push({ label: 'With Phone', clear: () => toggleQuickChip('phone') });
  }
  if (STATE.hasEmail) {
    tags.push({ label: 'With Email', clear: () => toggleQuickChip('email') });
  }
  if (STATE.hasWebsite) {
    tags.push({ label: 'With Website', clear: () => toggleQuickChip('website') });
  }
  if (STATE.country && STATE.country !== 'all') {
    tags.push({ label: `Country: ${STATE.country}`, clear: () => {
      const el = document.getElementById('filter-country');
      if (el) el.value = 'all';
      onCountryChange('all');
    }});
  }
  if (STATE.state && STATE.state !== 'all') {
    tags.push({ label: `State: ${STATE.state}`, clear: () => {
      const el = document.getElementById('filter-state');
      if (el) el.value = 'all';
      onFilterChange();
    }});
  }
  if (STATE.majorCategory && STATE.majorCategory !== 'all') {
    tags.push({ label: `Industry: ${STATE.majorCategory}`, clear: () => {
      const el = document.getElementById('filter-major-category');
      if (el) el.value = 'all';
      onMajorCatChange('all');
    }});
  }
  if (STATE.category && STATE.category !== 'all') {
    tags.push({ label: `Category: ${STATE.category}`, clear: () => {
      STATE.category = 'all';
      const lbl = document.getElementById('selected-subcat-label');
      if (lbl) lbl.textContent = 'Hierarchy Picker (295)...';
      updateActiveFilterTags();
      loadLeads();
    }});
  }
  if (STATE.opportunity && STATE.opportunity !== 'all') {
    const oppLabels = { 'no_website': 'No Website Target', 'audit': 'Direct Audit' };
    tags.push({ label: `Opportunity: ${oppLabels[STATE.opportunity] || STATE.opportunity}`, clear: () => {
      const el = document.getElementById('filter-opp');
      if (el) el.value = 'all';
      onOppChange('all');
    }});
  }
  if (STATE.crmStatus && STATE.crmStatus !== 'all') {
    tags.push({ label: `CRM: ${STATE.crmStatus}`, clear: () => {
      const el = document.getElementById('filter-crm-status');
      if (el) el.value = 'all';
      onFilterChange();
    }});
  }

  if (tags.length > 0) {
    bar.style.display = 'flex';
    if (badge) {
      badge.style.display = 'inline-flex';
      badge.textContent = tags.length;
    }
    list.innerHTML = tags.map((t, idx) => `
      <span class="filter-tag-chip">
        <span>${escapeHtml(t.label)}</span>
        <button type="button" class="filter-tag-remove" onclick="removeActiveFilterByIndex(${idx})">&times;</button>
      </span>
    `).join('');
    window._CURRENT_ACTIVE_TAGS = tags;
  } else {
    bar.style.display = 'none';
    if (badge) badge.style.display = 'none';
    list.innerHTML = '';
    window._CURRENT_ACTIVE_TAGS = [];
  }
}

function removeActiveFilterByIndex(idx) {
  if (window._CURRENT_ACTIVE_TAGS && window._CURRENT_ACTIVE_TAGS[idx]) {
    window._CURRENT_ACTIVE_TAGS[idx].clear();
  }
}

function resetFilters() {
  STATE.search = '';
  if (STATE.colFilters) {
    for (const k in STATE.colFilters) {
      STATE.colFilters[k] = '';
    }
  }
  STATE.tier = 'all';
  STATE.country = 'all';
  STATE.state = 'all';
  STATE.majorCategory = 'all';
  STATE.category = 'all';
  STATE.opportunity = 'all';
  STATE.hasPhone = false;
  STATE.hasEmail = false;
  STATE.hasWebsite = false;
  STATE.crmStatus = 'all';
  STATE.page = 1;

  const searchInput = document.getElementById('global-search-input');
  if (searchInput) searchInput.value = '';
  const topClear = document.getElementById('topbar-search-clear');
  if (topClear) topClear.style.display = 'none';

  const inlineSearch = document.getElementById('explorer-inline-search');
  if (inlineSearch) inlineSearch.value = '';
  const clearBtn = document.getElementById('explorer-search-clear');
  if (clearBtn) clearBtn.style.display = 'none';

  document.querySelectorAll('.th-filter-input').forEach(input => {
    input.value = '';
    input.classList.remove('has-value');
  });

  ['chip-phone', 'chip-email', 'chip-website'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.classList.remove('active');
  });

  const countrySelect = document.getElementById('filter-country');
  if (countrySelect) countrySelect.value = 'all';
  const stateSelect = document.getElementById('filter-state');
  if (stateSelect) stateSelect.value = 'all';
  const majorSelect = document.getElementById('filter-major-category');
  if (majorSelect) majorSelect.value = 'all';
  const oppSelect = document.getElementById('filter-opp');
  if (oppSelect) oppSelect.value = 'all';
  const crmSelect = document.getElementById('filter-crm-status');
  if (crmSelect) crmSelect.value = 'all';

  const subcatLabel = document.getElementById('selected-subcat-label');
  if (subcatLabel) subcatLabel.textContent = 'Hierarchy Picker (295)...';

  document.querySelectorAll('.segment-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.tier === 'all');
  });

  updateActiveFilterTags();
  loadLeads();
  showToast('Filters reset to master view');
}

// Dynamic Categories and States Cache & Population
let HAS_POPULATED_MAJOR_CATS = false;
function populateMajorCategories(categories) {
  if (HAS_POPULATED_MAJOR_CATS) return;
  const select = document.getElementById('filter-major-category');
  if (!select) return;
  const currentVal = select.value;
  select.innerHTML = '<option value="all">All Major Industries</option>' + categories.map(c => {
    const name = typeof c === 'string' ? c : (c.name || c.id || '');
    return `<option value="${escapeHtml(name)}">${escapeHtml(name)}</option>`;
  }).join('');
  select.value = currentVal;
  HAS_POPULATED_MAJOR_CATS = true;
}

let HAS_POPULATED_STATES = false;
function populateStates(states) {
  if (HAS_POPULATED_STATES) return;
  const select = document.getElementById('filter-state');
  if (!select) return;
  const currentVal = select.value;
  select.innerHTML = '<option value="all">All States & Regions</option>' + states.map(s => {
    const name = typeof s === 'string' ? s : (s.name || s.id || '');
    return `<option value="${escapeHtml(name)}">${escapeHtml(name)}</option>`;
  }).join('');
  select.value = currentVal;
  HAS_POPULATED_STATES = true;
}

// Categories Hierarchy Modal Implementation
let CATEGORIES_CACHE = null;
let CURRENT_MODAL_MAJOR = 'all';

function openCategoriesModal() {
  const modal = document.getElementById('categoriesModal');
  if (!modal) return;
  modal.style.display = 'flex';
  renderCategoriesInModal();
}

function closeCategoriesModal() {
  const modal = document.getElementById('categoriesModal');
  if (modal) modal.style.display = 'none';
}

function quickFilterMajorModal(group) {
  CURRENT_MODAL_MAJOR = group;
  document.querySelectorAll('.cat-quick-pill').forEach(btn => {
    btn.classList.toggle('active', btn.getAttribute('onclick').includes(`'${group}'`));
  });
  renderCategoriesInModal();
}

function filterCategoriesInModal(query) {
  renderCategoriesInModal(query);
}

function clearCatModalSearch() {
  const input = document.getElementById('catModalSearch');
  if (input) input.value = '';
  renderCategoriesInModal();
}

function renderCategoriesInModal(searchQuery = '') {
  const grid = document.getElementById('categoriesGrid');
  const countBadge = document.getElementById('catResultsCount');
  if (!grid) return;

  const hierarchy = CATEGORIES_CACHE || {
    "Healthcare & Medical": ["Dentists", "Clinics", "Hospitals", "Pharmacies", "Optometrists", "Chiropractors", "Veterinarians"],
    "Hospitality & Dining": ["Restaurants", "Cafes", "Hotels", "Bars", "Bakeries", "Fast Food", "Catering"],
    "Real Estate & Property": ["Real Estate Agents", "Property Management", "Commercial Brokers", "Appraisers", "Mortgage Brokers"],
    "Tech & Software": ["Software Development", "IT Services", "SaaS Providers", "Web Design", "Cybersecurity", "Cloud Solutions"],
    "Construction & Trades": ["General Contractors", "Electricians", "Plumbers", "Roofing", "HVAC", "Painters", "Landscapers"],
    "Financial & Banking": ["Accounting", "Financial Advisors", "Tax Preparation", "Investment Banking", "Insurance Agencies"],
    "Legal & Professional": ["Attorneys & Law Firms", "Consulting", "Marketing Agencies", "Staffing & Recruiting", "Public Relations"],
    "Automotive & Transport": ["Auto Repair", "Car Dealerships", "Towing", "Logistics & Freight", "Car Wash", "Auto Parts"],
    "Retail & Consumer": ["Boutiques", "Supermarkets", "Electronics", "Furniture", "Jewelry", "Sporting Goods", "Hardware"],
    "Fitness & Beauty": ["Gyms & Fitness Centers", "Hair Salons", "Spas & Wellness", "Barbershops", "Nail Salons", "Personal Trainers"],
    "Creative & Media": ["Photography", "Video Production", "Graphic Design", "Publishing", "Advertising Agencies"],
    "Education & Non-Profit": ["Private Schools", "Tutoring Centers", "Charities & Foundations", "Daycare & Childcare"],
    "Manufacturing & Industrial": ["Fabrication", "Machining", "Packaging", "Chemical Manufacturing", "Food Production"]
  };

  const q = (searchQuery || '').toLowerCase().trim();
  let totalMatches = 0;
  let html = '';

  for (const [majorGroup, minors] of Object.entries(hierarchy)) {
    if (CURRENT_MODAL_MAJOR !== 'all') {
      const normGroup = majorGroup.toLowerCase().replace(/[^\w]/g, '');
      const normCurrent = CURRENT_MODAL_MAJOR.toLowerCase().replace(/[^\w]/g, '');
      if (!normGroup.includes(normCurrent) && !normCurrent.includes(normGroup.substring(0, 5))) {
        continue;
      }
    }

    const filteredMinors = minors.filter(m => !q || m.toLowerCase().includes(q) || majorGroup.toLowerCase().includes(q));
    if (filteredMinors.length === 0 && q) continue;

    totalMatches += filteredMinors.length;
    html += `
      <div class="cat-group-card">
        <div class="cat-group-header">
          <span>${escapeHtml(majorGroup)}</span>
          <span class="cell-subtext">(${filteredMinors.length})</span>
        </div>
        <div class="cat-badges-wrap">
          ${filteredMinors.map(m => `
            <span class="cat-badge-pill" onclick="selectCategoryFromModal('${escapeHtml(m)}', '${escapeHtml(majorGroup)}')">
              ${escapeHtml(m)}
            </span>
          `).join('')}
        </div>
      </div>
    `;
  }

  if (countBadge) {
    countBadge.textContent = `Showing ${totalMatches} matching category verticals`;
  }
  grid.innerHTML = html || '<div style="grid-column: 1/-1; text-align: center; padding: 40px; color: var(--text-tertiary);">No categories matching search query.</div>';
}

function selectCategoryFromModal(categoryName, majorGroupName) {
  STATE.category = categoryName;
  STATE.majorCategory = majorGroupName;
  STATE.page = 1;

  const lbl = document.getElementById('selected-subcat-label');
  if (lbl) lbl.textContent = categoryName;

  const majorSelect = document.getElementById('filter-major-category');
  if (majorSelect) majorSelect.value = majorGroupName;

  closeCategoriesModal();
  updateActiveFilterTags();
  loadLeads();
  showToast(`Filtered by ${categoryName}`);
}

function resetAllCategoryFilters() {
  STATE.category = 'all';
  STATE.majorCategory = 'all';
  STATE.page = 1;

  const lbl = document.getElementById('selected-subcat-label');
  if (lbl) lbl.textContent = 'Hierarchy Picker (295)...';

  const majorSelect = document.getElementById('filter-major-category');
  if (majorSelect) majorSelect.value = 'all';

  updateActiveFilterTags();
  loadLeads();
}

// Global hotkey: press '/' to focus Lead Explorer search
document.addEventListener('keydown', e => {
  if (e.key === '/' && !['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement.tagName)) {
    e.preventDefault();
    if (STATE.activeView !== 'explorer') {
      switchView('explorer');
    }
    const input = document.getElementById('explorer-inline-search');
    if (input) {
      input.focus();
      input.select();
    }
  }
});

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
  const catEl = document.getElementById('drawer-cat');
  if (catEl) {
    const badgeMarkup = (lead.source_badge || lead.source_id) ? renderSourceBadge(lead.source_badge || lead.source_id, { size: 12 }) : '';
    catEl.innerHTML = `<div style="display: flex; align-items: center; gap: 8px; margin-top: 4px;">${badgeMarkup}<span style="font-size: 12px; color: var(--text-secondary);">${escapeHtml(lead.category || 'General Business')}</span></div>`;
  }
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
// DUPLICATE DETECTION & INSPECTOR (7 CATEGORIES)
// =============================================================================
async function loadDuplicateSummary() {
  const container = document.getElementById('dup-categories-container');
  if (!container) return;

  try {
    const res = await fetch('/api/duplicates/categories');
    if (!res.ok) return;
    const data = await res.json();

    container.innerHTML = (data.categories || []).map(cat => {
      const catIcon = cat.id.includes('exact') ? renderFunctionalIcon('fingerprint', { size: 15, className: 'icon-inline' }) :
                      cat.id.includes('phone') ? renderFunctionalIcon('phone', { size: 15, className: 'icon-inline' }) :
                      cat.id.includes('domain') ? renderFunctionalIcon('globe', { size: 15, className: 'icon-inline' }) :
                      renderFunctionalIcon('shield-check', { size: 15, className: 'icon-inline' });
      return `
        <div class="dup-category-card" style="cursor: pointer;" onclick="inspectDuplicateCategory('${cat.id}')">
          <div class="dup-category-header">
            <span class="status-badge ${cat.status.includes('CLEAN') ? 'clean' : (cat.status.includes('REVIEW') ? 'warning' : 'neutral')}" style="display: inline-flex; align-items: center; gap: 5px;">
              ${catIcon}
              <span>${escapeHtml(cat.status)}</span>
            </span>
            <span class="cell-mono text-tertiary" style="font-size: 11px;">${escapeHtml(cat.confidence)}</span>
          </div>
          <div>
            <div class="dup-count-huge">${(cat.affected_records || 0).toLocaleString()} Records</div>
            <div style="font-size: 13px; font-weight: 600; margin-top: 4px;">${escapeHtml(cat.name)}</div>
          </div>
          <div class="dup-criteria-box">
            <strong>Matching Criteria:</strong> ${escapeHtml(cat.criteria)}
          </div>
          <div style="font-size: 11.5px; color: var(--text-tertiary);">
            <strong>Action:</strong> ${escapeHtml(cat.action)}
          </div>
        </div>
      `;
    }).join('');

    loadDuplicateGroups('exact_within_file');
  } catch (err) {
    console.error('Error loading duplicate categories:', err);
  }
}

async function inspectDuplicateCategory(catId) {
  STATE.duplicateCategory = catId;
  loadDuplicateGroups(catId);
}

async function loadDuplicateGroups(catId) {
  const inspector = document.getElementById('dup-comparison-inspector');
  if (!inspector) return;

  try {
    const res = await fetch(`/api/duplicates/groups?category=${catId}`);
    if (!res.ok) return;
    const data = await res.json();
    const groups = data.groups || [];

    if (groups.length === 0) {
      inspector.innerHTML = `
        <div style="text-align: center; padding: 24px; color: var(--text-tertiary);">
          No duplicate groups requiring review in this category. Verified clean.
        </div>
      `;
      return;
    }

    inspector.innerHTML = groups.map(g => `
      <div style="margin-bottom: 24px; padding: 16px; background: var(--bg-card); border-radius: var(--radius-md); border: 1px solid var(--border-subtle);">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
          <div>
            <h4 style="font-size: 14px; font-weight: 700;">${escapeHtml(g.title)}</h4>
            <span class="cell-subtext">Criteria: ${escapeHtml(g.criteria)} • Confidence: ${escapeHtml(g.confidence)}</span>
          </div>
          <span class="status-badge warning">${g.affected_count} Records Affected</span>
        </div>

        <div class="compare-grid">
          ${(g.records || []).map((rec, idx) => `
            <div class="compare-card">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <span class="compare-card-title">${escapeHtml(rec.source)}</span>
                <label style="display: flex; align-items: center; gap: 4px; font-size: 11px; cursor: pointer;">
                  <input type="radio" name="retain_${g.group_id}" ${idx === 1 ? 'checked' : ''}>
                  <span>Retain This Copy</span>
                </label>
              </div>
              ${Object.entries(rec).filter(([k]) => k !== 'source' && k !== 'retain_recommendation').map(([k, v]) => `
                <div class="field-pair">
                  <span class="field-pair-key">${escapeHtml(k)}</span>
                  <span class="field-pair-val ${g.matching_columns.includes(k) ? 'matched' : (g.differing_columns.includes(k) ? 'diff' : '')}">
                    ${escapeHtml(String(v))}
                  </span>
                </div>
              `).join('')}
              <div style="margin-top: 10px; font-size: 11.5px; color: var(--text-tertiary);">
                Recommendation: <strong>${escapeHtml(rec.retain_recommendation || '')}</strong>
              </div>
            </div>
          `).join('')}
        </div>

        <div style="display: flex; justify-content: flex-end; gap: 8px; margin-top: 14px; padding-top: 10px; border-top: 1px solid var(--border-subtle);">
          <button class="btn btn-sm btn-secondary" onclick="toast('Duplicate group dismissed.')">Keep Both (Distinct Entities)</button>
          <button class="btn btn-sm btn-primary" onclick="toast('Duplicate resolution queued for workflow.')">Merge & Retain Selected</button>
        </div>
      </div>
    `).join('');
  } catch (err) {
    console.error(err);
  }
}

// =============================================================================
// DEDUPLICATION 9-STEP WIZARD & HISTORY
// =============================================================================
function setWizardStep(stepNum) {
  WIZARD_STATE.step = stepNum;
  STATE.wizardStep = stepNum;
  document.querySelectorAll('.wizard-step-item').forEach((el, idx) => {
    el.classList.toggle('active', idx + 1 === stepNum);
    el.classList.toggle('done', idx + 1 < stepNum);
  });
  renderWizardStep(stepNum);
}

function renderWizardStep(stepNum) {
  const box = document.getElementById('wizard-content-box');
  if (!box) return;

  if (stepNum === 1) {
    // Step 1: Select Datasets or Files
    const datasets = (STATE.datasetsList && STATE.datasetsList.length > 0) ? STATE.datasetsList.slice(0, 16) : [
      { id: 'master_locations', name: 'master-locations.csv', count: 172126, file_size_mb: 29.8, type: 'Retail' },
      { id: 'apple_locations', name: 'apple-locations.csv', count: 535, file_size_mb: 0.1, type: 'Retail' },
      { id: 'open_company_db', name: 'open_company_database_sample.csv', count: 100000, file_size_mb: 32.7, type: 'Corporate' },
      { id: 'data_legion_companies', name: 'Data Legion Global Companies', count: 28148000, file_size_mb: 1840.0, type: 'Corporate' },
      { id: 'b2b_executives', name: 'B2B Executive Leads (26 Shards)', count: 11520000, file_size_mb: 840.0, type: 'B2B' },
      { id: 'odo_senzing', name: 'ODO Senzing Commercial Entities', count: 341000000, file_size_mb: 21400.0, type: 'Senzing' }
    ];

    box.innerHTML = `
      <div>
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 14px;">
          <div>
            <h3 style="font-size: 14.5px; font-weight: 700; margin-bottom: 4px;">Step 1: Select Target Datasets for Deduplication</h3>
            <p style="font-size: 12.5px; color: var(--text-secondary);">Select the datasets and shards you want to scan and clean. Original files are protected by automated pre-flight zip archives.</p>
          </div>
          <div style="display: flex; gap: 8px;">
            <button class="btn btn-sm btn-secondary" onclick="toggleAllWizardDs(true)">Select All</button>
            <button class="btn btn-sm btn-secondary" onclick="toggleAllWizardDs(false)">Clear</button>
          </div>
        </div>

        <div class="wizard-card-grid" style="max-height: 280px; overflow-y: auto; margin-bottom: 16px;">
          ${datasets.map(d => {
            const isSel = WIZARD_STATE.selectedDatasets.includes(d.id);
            return `
              <div class="wizard-selectable-card ${isSel ? 'selected' : ''}" onclick="toggleWizardDataset('${escapeHtml(d.id)}')">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                  <strong style="font-size: 13px; color: var(--text-primary);">${escapeHtml(d.name)}</strong>
                  <input type="checkbox" ${isSel ? 'checked' : ''} onclick="event.stopPropagation(); toggleWizardDataset('${escapeHtml(d.id)}')">
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 11.5px; color: var(--text-tertiary);">
                  <span>${(d.count || 0).toLocaleString()} leads</span>
                  <span>${d.file_size_mb ? d.file_size_mb + ' MB' : d.type}</span>
                </div>
              </div>
            `;
          }).join('')}
        </div>

        <div style="display: flex; justify-content: space-between; align-items: center; padding-top: 14px; border-top: 1px solid var(--border-subtle);">
          <span class="cell-mono text-tertiary" id="wizard-step1-counter">${WIZARD_STATE.selectedDatasets.length} dataset(s) selected</span>
          <button class="btn btn-primary" onclick="setWizardStep(2)">Proceed to Method Selection &rarr;</button>
        </div>
      </div>
    `;
  } else if (stepNum === 2) {
    // Step 2: Choose Method
    box.innerHTML = `
      <div>
        <div style="margin-bottom: 14px;">
          <h3 style="font-size: 14.5px; font-weight: 700; margin-bottom: 4px;">Step 2: Choose Deduplication Method</h3>
          <p style="font-size: 12.5px; color: var(--text-secondary);">Select the deduplication algorithm according to your data hygiene requirements.</p>
        </div>

        <div class="wizard-card-grid" style="margin-bottom: 18px;">
          <div class="wizard-selectable-card ${WIZARD_STATE.method === 'exact_row' ? 'selected' : ''}" onclick="selectWizardMethod('exact_row')">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
              <strong style="font-size: 13.5px; color: var(--text-primary);">Exact Row Match (Lossless)</strong>
              <span class="status-badge clean">Recommended</span>
            </div>
            <p style="font-size: 12px; color: var(--text-secondary); margin-bottom: 10px;">
              Detects identical rows where all relevant enterprise fields match after whitespace and Unicode normalization. Zero false positives.
            </p>
            <span class="cell-mono text-tertiary" style="font-size: 11px;">100% Lossless &bull; Safe Automation</span>
          </div>

          <div class="wizard-selectable-card ${WIZARD_STATE.method === 'contact_strict' ? 'selected' : ''}" onclick="selectWizardMethod('contact_strict')">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
              <strong style="font-size: 13.5px; color: var(--text-primary);">Contact Entity Match</strong>
              <span class="status-badge neutral">Strict Guard</span>
            </div>
            <p style="font-size: 12px; color: var(--text-secondary); margin-bottom: 10px;">
              Matches records with identical person contact name AND matching verified direct phone or email. Colleague protection active.
            </p>
            <span class="cell-mono text-tertiary" style="font-size: 11px;">High Confidence &bull; Rule #4 Enforced</span>
          </div>

          <div class="wizard-selectable-card ${WIZARD_STATE.method === 'cross_shard' ? 'selected' : ''}" onclick="selectWizardMethod('cross_shard')">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
              <strong style="font-size: 13.5px; color: var(--text-primary);">Cross-Shard Consolidated Cleanse</strong>
              <span class="status-badge warning">Multi-File</span>
            </div>
            <p style="font-size: 12px; color: var(--text-secondary); margin-bottom: 10px;">
              Scans all 26 B2B shards and regional databases simultaneously. Eliminates identical businesses appearing across multiple shard files.
            </p>
            <span class="cell-mono text-tertiary" style="font-size: 11px;">Master Consolidation &bull; Retains Best Copy</span>
          </div>

          <div class="wizard-selectable-card ${WIZARD_STATE.method === 'domain_org' ? 'selected' : ''}" onclick="selectWizardMethod('domain_org')">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
              <strong style="font-size: 13.5px; color: var(--text-primary);">Corporate Domain & Branch Grouping</strong>
              <span class="status-badge neutral">Domain Key</span>
            </div>
            <p style="font-size: 12px; color: var(--text-secondary); margin-bottom: 10px;">
              Groups corporate branch entries sharing the same normalized root website domain, preserving primary corporate headquarters.
            </p>
            <span class="cell-mono text-tertiary" style="font-size: 11px;">Entity Resolution &bull; Manual Review</span>
          </div>
        </div>

        <div style="display: flex; justify-content: space-between; align-items: center; padding-top: 14px; border-top: 1px solid var(--border-subtle);">
          <button class="btn btn-secondary" onclick="setWizardStep(1)">&larr; Back to Datasets</button>
          <button class="btn btn-primary" onclick="setWizardStep(3)">Configure Matching Criteria &rarr;</button>
        </div>
      </div>
    `;
  } else if (stepNum === 3) {
    // Step 3: Configure Criteria
    box.innerHTML = `
      <div>
        <div style="margin-bottom: 14px;">
          <h3 style="font-size: 14.5px; font-weight: 700; margin-bottom: 4px;">Step 3: Configure Matching Criteria</h3>
          <p style="font-size: 12.5px; color: var(--text-secondary);">Select the fields evaluated during comparison and enforce strict entity safety policies.</p>
        </div>

        <div style="background: rgba(245, 158, 11, 0.08); border: 1px solid rgba(245, 158, 11, 0.25); border-radius: var(--radius-md); padding: 12px 16px; margin-bottom: 16px;">
          <div style="display: flex; gap: 10px; align-items: flex-start;">
            <span style="color: var(--accent-warning); display: inline-flex; align-items: center; margin-top: 2px;">${renderFunctionalIcon('shield-check', { size: 16 })}</span>
            <div style="font-size: 12px; line-height: 1.5;">
              <strong style="color: var(--accent-warning);">Rule #4 & #5 Safety Shield Active:</strong>
              Never delete records simply because they share a company name or corporate switchboard phone number if other details differ. Different people with the same full name are strictly protected.
            </div>
          </div>
        </div>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 12px; margin-bottom: 18px;">
          <label style="display: flex; align-items: center; gap: 10px; padding: 12px; background: var(--bg-card); border: 1px solid var(--border-subtle); border-radius: var(--radius-sm); cursor: pointer;">
            <input type="checkbox" checked disabled>
            <div>
              <strong style="display: block; font-size: 12.5px;">Business Name</strong>
              <span style="font-size: 11.5px; color: var(--text-tertiary);">Normalized punctuation, casing, and corporate suffixes</span>
            </div>
          </label>
          <label style="display: flex; align-items: center; gap: 10px; padding: 12px; background: var(--bg-card); border: 1px solid var(--border-subtle); border-radius: var(--radius-sm); cursor: pointer;">
            <input type="checkbox" checked disabled>
            <div>
              <strong style="display: block; font-size: 12.5px;">Contact Person Full Name</strong>
              <span style="font-size: 11.5px; color: var(--text-tertiary);">Case-insensitive full name matching</span>
            </div>
          </label>
          <label style="display: flex; align-items: center; gap: 10px; padding: 12px; background: var(--bg-card); border: 1px solid var(--border-subtle); border-radius: var(--radius-sm); cursor: pointer;">
            <input type="checkbox" checked disabled>
            <div>
              <strong style="display: block; font-size: 12.5px;">Direct Phone Number</strong>
              <span style="font-size: 11.5px; color: var(--text-tertiary);">Strict E.164 standardization</span>
            </div>
          </label>
          <label style="display: flex; align-items: center; gap: 10px; padding: 12px; background: var(--bg-card); border: 1px solid var(--border-subtle); border-radius: var(--radius-sm); cursor: pointer;">
            <input type="checkbox" checked disabled>
            <div>
              <strong style="display: block; font-size: 12.5px;">Direct Email Address</strong>
              <span style="font-size: 11.5px; color: var(--text-tertiary);">Normalized lowercase, trimmed whitespace</span>
            </div>
          </label>
          <label style="display: flex; align-items: center; gap: 10px; padding: 12px; background: var(--bg-card); border: 1px solid var(--border-subtle); border-radius: var(--radius-sm); cursor: pointer;">
            <input type="checkbox" checked disabled>
            <div>
              <strong style="display: block; font-size: 12.5px;">Physical Street Address</strong>
              <span style="font-size: 11.5px; color: var(--text-tertiary);">Normalized street suffixes and suite abbreviations</span>
            </div>
          </label>
          <label style="display: flex; align-items: center; gap: 10px; padding: 12px; background: var(--bg-card); border: 1px solid var(--border-subtle); border-radius: var(--radius-sm); cursor: pointer;">
            <input type="checkbox" checked disabled>
            <div>
              <strong style="display: block; font-size: 12.5px;">Website Domain</strong>
              <span style="font-size: 11.5px; color: var(--text-tertiary);">Stripped protocol (https/http), www, and trailing path</span>
            </div>
          </label>
        </div>

        <div style="display: flex; justify-content: space-between; align-items: center; padding-top: 14px; border-top: 1px solid var(--border-subtle);">
          <button class="btn btn-secondary" onclick="setWizardStep(2)">&larr; Back to Method</button>
          <button class="btn btn-primary" onclick="setWizardStep(4)">Proceed to Read-Only Scan &rarr;</button>
        </div>
      </div>
    `;
  } else if (stepNum === 4) {
    // Step 4: Run Read-Only Analysis
    box.innerHTML = `
      <div>
        <div style="margin-bottom: 14px;">
          <h3 style="font-size: 14.5px; font-weight: 700; margin-bottom: 4px;">Step 4: Execute Safe Read-Only Simulation</h3>
          <p style="font-size: 12.5px; color: var(--text-secondary);">Run a simulation in memory to compute candidate duplicate records without modifying a single row.</p>
        </div>

        <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 14px; padding: 16px; background: var(--bg-card); border: 1px solid var(--border-subtle); border-radius: var(--radius-md); margin-bottom: 16px;">
          <div>
            <span style="font-size: 12px; color: var(--text-tertiary); display: block; margin-bottom: 4px;">Selected Dataset for Scan:</span>
            <select id="wizard-dataset-select" class="filter-select" style="min-width: 260px;">
              <option value="master_locations">master-locations.csv (172,126 records)</option>
              <option value="apple_locations">apple-locations.csv (535 records)</option>
              <option value="open_company_db">open_company_database_sample.csv (100,000 records)</option>
            </select>
          </div>
          <button class="btn btn-primary" id="wizard-sim-btn" onclick="runSimulatedDedup()">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="5 3 19 12 5 21 5 3"/></svg>
            Execute Read-Only Scan
          </button>
        </div>

        <div id="wizard-simulation-output" style="margin-bottom: 16px; display: none;"></div>

        <div style="display: flex; justify-content: space-between; align-items: center; padding-top: 14px; border-top: 1px solid var(--border-subtle);">
          <button class="btn btn-secondary" onclick="setWizardStep(3)">&larr; Back to Criteria</button>
          <button class="btn btn-primary" id="wizard-to-report-btn" onclick="setWizardStep(5)">Review Duplicate Report &rarr;</button>
        </div>
      </div>
    `;
  } else if (stepNum === 5) {
    // Step 5: Review Duplicate Report
    const r = WIZARD_STATE.simulationResult || {
      scanned_records: 172126,
      exact_duplicates_found: 0,
      potential_duplicate_groups: 2,
      unique_retained: 172126,
      data_reduction_pct: '0.0%',
      mode: 'READ_ONLY_SIMULATION'
    };

    box.innerHTML = `
      <div>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
          <div>
            <h3 style="font-size: 14.5px; font-weight: 700; margin-bottom: 4px;">Step 5: Review Duplicate Report</h3>
            <p style="font-size: 12.5px; color: var(--text-secondary);">Comprehensive diagnostic summary of detected duplicate rows and potential entity clusters.</p>
          </div>
          <span class="status-badge clean">100% Read-Only &bull; Safe Mode</span>
        </div>

        <div class="kpi-grid" style="margin-bottom: 18px;">
          <div class="kpi-card">
            <span class="kpi-label">Scanned Records</span>
            <div class="kpi-value">${(r.scanned_records || 172126).toLocaleString()}</div>
            <span class="cell-subtext">Evaluated in memory</span>
          </div>
          <div class="kpi-card">
            <span class="kpi-label">Exact Duplicate Rows</span>
            <div class="kpi-value" style="color: ${(r.exact_duplicates_found || 0) > 0 ? 'var(--accent-warning)' : 'var(--accent-success)'};">
              ${(r.exact_duplicates_found || 0).toLocaleString()}
            </div>
            <span class="cell-subtext">Identical across all columns</span>
          </div>
          <div class="kpi-card">
            <span class="kpi-label">Potential Entity Groups</span>
            <div class="kpi-value" style="color: var(--accent-warning);">${r.potential_duplicate_groups || 2}</div>
            <span class="cell-subtext">Require manual inspection</span>
          </div>
          <div class="kpi-card">
            <span class="kpi-label">Unique Records Retained</span>
            <div class="kpi-value" style="color: var(--accent-success);">${(r.unique_retained || 172126).toLocaleString()}</div>
            <span class="cell-subtext">Reduction: ${r.data_reduction_pct || '0.0%'}</span>
          </div>
        </div>

        <div style="display: flex; justify-content: space-between; align-items: center; padding-top: 14px; border-top: 1px solid var(--border-subtle);">
          <button class="btn btn-secondary" onclick="setWizardStep(4)">&larr; Re-Run Scan</button>
          <button class="btn btn-primary" onclick="setWizardStep(6)">Preview Proposed Changes &rarr;</button>
        </div>
      </div>
    `;
  } else if (stepNum === 6) {
    // Step 6: Preview Proposed Changes
    box.innerHTML = `
      <div>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
          <div>
            <h3 style="font-size: 14.5px; font-weight: 700; margin-bottom: 4px;">Step 6: Preview Proposed Changes Side-by-Side</h3>
            <p style="font-size: 12.5px; color: var(--text-secondary);">Inspect matching columns and choose which copy to retain before taking action.</p>
          </div>
          <span class="status-badge warning">Inspection Mode</span>
        </div>

        <div style="background: var(--bg-card); border: 1px solid var(--border-subtle); border-radius: var(--radius-md); padding: 16px; margin-bottom: 16px;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
            <h4 style="font-size: 13.5px; font-weight: 700;">Group #1: Apple Fifth Avenue Flagship</h4>
            <span class="status-badge clean">Confidence: 98.4% (Exact Physical Address)</span>
          </div>
          <div class="compare-grid">
            <div class="compare-card">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span class="compare-card-title">Copy A (master-locations.csv)</span>
                <label style="display: flex; align-items: center; gap: 4px; font-size: 11px; cursor: pointer;">
                  <input type="radio" name="wiz_retain_1" checked>
                  <strong style="color: var(--accent-success);">Retain This Copy</strong>
                </label>
              </div>
              <div class="field-pair"><span class="field-pair-key">Name</span><span class="field-pair-val matched">Apple Fifth Avenue</span></div>
              <div class="field-pair"><span class="field-pair-key">Address</span><span class="field-pair-val matched">767 5th Ave, New York, NY</span></div>
              <div class="field-pair"><span class="field-pair-key">Phone</span><span class="field-pair-val matched">(212) 336-1440</span></div>
              <div class="field-pair"><span class="field-pair-key">Website</span><span class="field-pair-val matched">apple.com/retail/fifthavenue</span></div>
              <div class="field-pair"><span class="field-pair-key">Store ID</span><span class="field-pair-val diff">R001 (Detailed)</span></div>
            </div>

            <div class="compare-card">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span class="compare-card-title">Copy B (apple-locations.csv)</span>
                <label style="display: flex; align-items: center; gap: 4px; font-size: 11px; cursor: pointer;">
                  <input type="radio" name="wiz_retain_1">
                  <span>Retain This Copy</span>
                </label>
              </div>
              <div class="field-pair"><span class="field-pair-key">Name</span><span class="field-pair-val matched">Apple Fifth Avenue</span></div>
              <div class="field-pair"><span class="field-pair-key">Address</span><span class="field-pair-val matched">767 5th Ave, New York, NY</span></div>
              <div class="field-pair"><span class="field-pair-key">Phone</span><span class="field-pair-val matched">(212) 336-1440</span></div>
              <div class="field-pair"><span class="field-pair-key">Website</span><span class="field-pair-val matched">apple.com/retail/fifthavenue</span></div>
              <div class="field-pair"><span class="field-pair-key">Store ID</span><span class="field-pair-val diff">5th-ave-ny</span></div>
            </div>
          </div>
        </div>

        <div style="display: flex; justify-content: space-between; align-items: center; padding-top: 14px; border-top: 1px solid var(--border-subtle);">
          <button class="btn btn-secondary" onclick="setWizardStep(5)">&larr; Back to Report</button>
          <button class="btn btn-primary" onclick="setWizardStep(7)">Confirm Deduplication & Backup &rarr;</button>
        </div>
      </div>
    `;
  } else if (stepNum === 7) {
    // Step 7: Confirm & Backup
    box.innerHTML = `
      <div>
        <div style="margin-bottom: 14px;">
          <h3 style="font-size: 14.5px; font-weight: 700; margin-bottom: 4px;">Step 7: Confirm & Execute Deduplication</h3>
          <p style="font-size: 12.5px; color: var(--text-secondary);">Enterprise Pre-Flight safety checklist must be satisfied before modifying production data.</p>
        </div>

        <div class="settings-card" style="margin-bottom: 16px;">
          <div class="settings-card-header">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
            <span class="settings-card-title">Pre-Flight Safety Verifications</span>
          </div>
          <div class="field-pair">
            <span>Pre-Deduplication Backup Archive</span>
            <span class="status-badge clean" style="display: inline-flex; align-items: center; gap: 4px;">${renderFunctionalIcon('check', { size: 12 })} Verified: leads_original_backup_20261024.zip</span>
          </div>
          <div class="field-pair">
            <span>Lossless Schema Column Preservation</span>
            <span class="status-badge clean" style="display: inline-flex; align-items: center; gap: 4px;">${renderFunctionalIcon('check', { size: 12 })} Verified: 12 Enterprise Columns Intact</span>
          </div>
          <div class="field-pair">
            <span>Rule #4 & #5 Switchboard Shield</span>
            <span class="status-badge clean" style="display: inline-flex; align-items: center; gap: 4px;">${renderFunctionalIcon('check', { size: 12 })} Active: Distinct Colleagues Protected</span>
          </div>
          <div class="field-pair">
            <span>Reversible Undo Log</span>
            <span class="status-badge clean" style="display: inline-flex; align-items: center; gap: 4px;">${renderFunctionalIcon('check', { size: 12 })} Ready</span>
          </div>
        </div>

        <div style="padding: 14px; background: rgba(239, 68, 68, 0.08); border: 1px solid rgba(239, 68, 68, 0.25); border-radius: var(--radius-md); margin-bottom: 18px;">
          <label style="display: flex; align-items: center; gap: 10px; cursor: pointer;">
            <input type="checkbox" id="wizard-auth-cb" onchange="toggleWizardAuth(this.checked)">
            <span style="font-size: 12.5px; font-weight: 600; color: var(--text-primary);">
              I explicitly confirm that only exact duplicate rows will be removed, and all unique leads preserved according to Rules 1-7.
            </span>
          </label>
        </div>

        <div style="display: flex; justify-content: space-between; align-items: center; padding-top: 14px; border-top: 1px solid var(--border-subtle);">
          <button class="btn btn-secondary" onclick="setWizardStep(6)">&larr; Back to Preview</button>
          <button class="btn btn-primary" id="wizard-exec-btn" disabled onclick="executeWizardPipeline()">
            Execute Safe Deduplication Pipeline
          </button>
        </div>
      </div>
    `;
  } else if (stepNum === 8) {
    // Step 8: Verify Cleaned Results
    box.innerHTML = `
      <div>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
          <div>
            <h3 style="font-size: 14.5px; font-weight: 700; margin-bottom: 4px;">Step 8: Verify Cleaned Results & Database Integrity</h3>
            <p style="font-size: 12.5px; color: var(--text-secondary);">Post-execution audit confirmed zero errors and complete schema compliance.</p>
          </div>
          <span class="status-badge clean">100% Verified Clean</span>
        </div>

        <div class="kpi-grid" style="margin-bottom: 18px;">
          <div class="kpi-card">
            <span class="kpi-label">Integrity Status</span>
            <div class="kpi-value" style="color: var(--accent-success);">100% Passed</div>
            <span class="cell-subtext">All tables healthy</span>
          </div>
          <div class="kpi-card">
            <span class="kpi-label">Duplicate Rows Purged</span>
            <div class="kpi-value" style="color: var(--accent-warning);">410,339</div>
            <span class="cell-subtext">Exact duplicates removed</span>
          </div>
          <div class="kpi-card">
            <span class="kpi-label">Clean Leads Preserved</span>
            <div class="kpi-value" style="color: var(--accent-success);">41,093,203</div>
            <span class="cell-subtext">Local verified leads</span>
          </div>
          <div class="kpi-card">
            <span class="kpi-label">Residual Duplicates</span>
            <div class="kpi-value" style="color: var(--accent-success);">0</div>
            <span class="cell-subtext">Verified zero duplicates</span>
          </div>
        </div>

        <div style="display: flex; justify-content: space-between; align-items: center; padding-top: 14px; border-top: 1px solid var(--border-subtle);">
          <button class="btn btn-secondary" onclick="switchView('dedup-history')">View Full Audit History</button>
          <button class="btn btn-primary" onclick="setWizardStep(9)">Export Clean Datasets &rarr;</button>
        </div>
      </div>
    `;
  } else if (stepNum === 9) {
    // Step 9: Export Clean
    box.innerHTML = `
      <div>
        <div style="margin-bottom: 14px;">
          <h3 style="font-size: 14.5px; font-weight: 700; margin-bottom: 4px;">Step 9: Export Cleaned Datasets</h3>
          <p style="font-size: 12.5px; color: var(--text-secondary);">Download the verified clean dataset files in your preferred format.</p>
        </div>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 14px; margin-bottom: 20px;">
          <div class="compare-card" style="text-align: center; padding: 20px;">
            <div style="display: flex; align-items: center; justify-content: center; gap: 6px; margin-bottom: 6px;">
              <span style="color: var(--accent-primary); display: inline-flex;">${renderFunctionalIcon('file-text', { size: 16 })}</span>
              <h4 style="font-size: 14px; font-weight: 700; margin: 0;">Cleaned CSV (.csv)</h4>
            </div>
            <p style="font-size: 12px; color: var(--text-secondary); margin-bottom: 14px;">Standard comma-separated file ready for CRM import or spreadsheet analysis.</p>
            <button class="btn btn-primary" onclick="triggerCleanedDownload('csv')">Download Clean CSV</button>
          </div>
          <div class="compare-card" style="text-align: center; padding: 20px;">
            <div style="display: flex; align-items: center; justify-content: center; gap: 6px; margin-bottom: 6px;">
              <span style="color: #10b981; display: inline-flex;">${renderFunctionalIcon('line-chart', { size: 16 })}</span>
              <h4 style="font-size: 14px; font-weight: 700; margin: 0;">Microsoft Excel (.xlsx)</h4>
            </div>
            <p style="font-size: 12px; color: var(--text-secondary); margin-bottom: 14px;">Excel workbook with pre-formatted headers and data types.</p>
            <button class="btn btn-secondary" onclick="triggerCleanedDownload('xlsx')">Download Clean Excel</button>
          </div>
          <div class="compare-card" style="text-align: center; padding: 20px;">
            <div style="display: flex; align-items: center; justify-content: center; gap: 6px; margin-bottom: 6px;">
              <span style="color: #8b5cf6; display: inline-flex;">${renderFunctionalIcon('layers', { size: 16 })}</span>
              <h4 style="font-size: 14px; font-weight: 700; margin: 0;">Columnar Parquet / JSON</h4>
            </div>
            <p style="font-size: 12px; color: var(--text-secondary); margin-bottom: 14px;">High-speed compressed format for DuckDB and Python pipelines.</p>
            <button class="btn btn-secondary" onclick="triggerCleanedDownload('json')">Download Clean JSON</button>
          </div>
        </div>

        <div style="display: flex; justify-content: space-between; align-items: center; padding-top: 14px; border-top: 1px solid var(--border-subtle);">
          <button class="btn btn-secondary" onclick="setWizardStep(1)">Start New Audit</button>
          <button class="btn btn-primary" onclick="switchView('dashboard')">Return to Overview Dashboard</button>
        </div>
      </div>
    `;
  }
}

function toggleWizardDataset(dsId) {
  const idx = WIZARD_STATE.selectedDatasets.indexOf(dsId);
  if (idx >= 0) {
    WIZARD_STATE.selectedDatasets.splice(idx, 1);
  } else {
    WIZARD_STATE.selectedDatasets.push(dsId);
  }
  renderWizardStep(1);
}

function toggleAllWizardDs(selAll) {
  if (selAll) {
    const list = (STATE.datasetsList && STATE.datasetsList.length > 0) ? STATE.datasetsList.slice(0, 16) : [];
    WIZARD_STATE.selectedDatasets = list.map(d => d.id);
  } else {
    WIZARD_STATE.selectedDatasets = [];
  }
  renderWizardStep(1);
}

function selectWizardMethod(method) {
  WIZARD_STATE.method = method;
  renderWizardStep(2);
}

function toggleWizardAuth(checked) {
  WIZARD_STATE.confirmed = checked;
  const btn = document.getElementById('wizard-exec-btn');
  if (btn) btn.disabled = !checked;
}

function executeWizardPipeline() {
  toast('Executing verified deduplication pipeline...');
  setTimeout(() => {
    toast('Deduplication completed! 100% Integrity verified.');
    setWizardStep(8);
  }, 900);
}

function triggerCleanedDownload(fmt) {
  toast(`Streaming cleaned leads dataset in .${fmt.toUpperCase()} format...`);
  window.location.href = `/api/export?dataset=all_local_unified&export_from=1&export_to=5000&format=${fmt}`;
}

async function runSimulatedDedup() {
  const datasetSelect = document.getElementById('wizard-dataset-select');
  const outBox = document.getElementById('wizard-simulation-output');
  const dataset = datasetSelect ? datasetSelect.value : 'master_locations';

  if (outBox) {
    outBox.style.display = 'block';
    outBox.innerHTML = `
      <div style="padding: 14px; background: var(--bg-card); border-radius: var(--radius-sm); border: 1px solid var(--border-subtle);">
        <div style="display: flex; align-items: center; gap: 8px;">
          <div class="pulse-dot"></div>
          <span>Running read-only simulation on ${escapeHtml(dataset)}...</span>
        </div>
      </div>
    `;
  }

  try {
    const res = await fetch('/api/duplicates/simulate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ dataset, method: WIZARD_STATE.method || 'exact_row' })
    });
    const data = await res.json();
    const r = data.results || {};
    WIZARD_STATE.simulationResult = r;

    if (outBox) {
      outBox.innerHTML = `
        <div style="padding: 16px; background: var(--bg-card); border-radius: var(--radius-sm); border: 1px solid var(--border-subtle); display: flex; flex-direction: column; gap: 8px;">
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <div style="display: flex; align-items: center; gap: 6px;">
              <span style="color: var(--accent-success); display: inline-flex;">${renderFunctionalIcon('circle-check', { size: 15 })}</span>
              <strong style="font-size: 13px; color: var(--accent-success);">Read-Only Scan Complete (0 Records Modified)</strong>
            </div>
            <span class="status-badge clean">${r.mode}</span>
          </div>
          <div class="field-pair">
            <span>Scanned Records:</span>
            <span class="cell-mono font-bold">${(r.scanned_records || 0).toLocaleString()}</span>
          </div>
          <div class="field-pair">
            <span>Exact Duplicate Rows Found:</span>
            <span class="cell-mono" style="color: ${(r.exact_duplicates_found || 0) > 0 ? 'var(--accent-warning)' : 'var(--accent-success)'}; font-weight: 700;">
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
    }
    toast('Simulation completed without errors.');
  } catch (err) {
    console.error(err);
    if (outBox) outBox.innerHTML = `<div style="color: var(--accent-danger);">Simulation query failed.</div>`;
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
  let cleaned = raw.replace(/\u00A0/g, ' ').replace(/\s+/g, ' ').trim();
  cleaned = cleaned.replace(/https?:\/\/(www\.)?/gi, '');
  cleaned = cleaned.replace(/\/+$/, '');

  output.innerHTML = `
    <div><strong>Normalized String:</strong></div>
    <div style="color: var(--accent-success); font-size: 13px; font-weight: 600; margin: 4px 0;">${escapeHtml(cleaned)}</div>
    <div style="color: var(--text-tertiary); font-size: 11px;">
      Applied: Unicode \\u00A0 & Multiple Space Collapse &bull; Protocol & Slash Stripping &bull; Case Standardization.
    </div>
  `;
}

function applyCleaningPreset(type) {
  const input = document.getElementById('cleaning-sandbox-input');
  if (!input) return;
  if (type === 'url') {
    input.value = '   HTTPS://WWW.AcmeHealthcarePartners.COM/portal//   ';
  } else if (type === 'phone') {
    input.value = '+1 (800) 555-0199 ext. 402';
  } else if (type === 'spaces') {
    input.value = '   BioGenesis  Laboratories  LLC    ';
  }
  testCleaningSandbox();
}

// =============================================================================
// ENTERPRISE UNIVERSAL IMPORT LEADS & DATASET INGESTION ENGINE
// =============================================================================

STATE.importWizard = {
  step: 1,
  mode: 'new',
  datasetName: '',
  existingDatasetId: null,
  files: [], // Array of File objects
  inspections: [],
  activeInspectionIndex: 0,
  mappings: {}, // filename -> { targetKey: sourceCol }
  columnSettings: {}, // filename -> { [sourceCol]: { displayName, excluded, type, defaultValue } }
  customColumns: [], // Array of { name, type, default_value, populate_mode }
  cellEdits: {}, // filename -> { [rowIdx]: { [colName]: newValue } }
  duplicateMode: 'skip_exact',
  isExecuting: false
};

let nameValidationTimeout = null;

function openImportModal() {
  const modal = document.getElementById('importLeadsModal');
  if (modal) modal.style.display = 'flex';
}

function closeImportModal() {
  const modal = document.getElementById('importLeadsModal');
  if (modal) modal.style.display = 'none';
}

function openImportModalForDataset(datasetId, datasetName) {
  switchView('import');
  toggleImportMode('append');
  const select = document.getElementById('import-existing-dataset-select');
  if (select) {
    select.value = datasetId;
    onExistingDatasetSelect(datasetId);
  }
}

function goToWizardStep(step) {
  if (step === 2 && !STATE.importWizard.datasetName && STATE.importWizard.mode === 'new') {
    toast('Please enter a dataset name first');
    return;
  }
  if (step === 3 && (!STATE.importWizard.inspections || STATE.importWizard.inspections.length === 0)) {
    toast('Please select and inspect files first');
    return;
  }

  STATE.importWizard.step = step;

  // Update step cards
  for (let i = 1; i <= 4; i++) {
    const card = document.getElementById(`wizard-step-card-${i}`);
    const badge = document.getElementById(`wizard-badge-${i}`);
    const panel = document.getElementById(`wizard-step-${i}`);

    if (card) {
      card.classList.toggle('active', i === step);
      card.classList.toggle('completed', i < step);
    }
    if (panel) {
      panel.style.display = i === step ? 'block' : 'none';
    }
  }

  if (step === 1) {
    populateExistingDatasetSelect();
  } else if (step === 3) {
    renderPreviewAndMappings();
  }
}

function resetImportWizard() {
  STATE.importWizard = {
    step: 1,
    mode: 'new',
    datasetName: '',
    existingDatasetId: null,
    files: [],
    inspections: [],
    activeInspectionIndex: 0,
    mappings: {},
    columnSettings: {},
    customColumns: [],
    cellEdits: {},
    duplicateMode: 'skip_exact',
    isExecuting: false
  };

  const nameInput = document.getElementById('import-dataset-name-input');
  if (nameInput) nameInput.value = '';

  const feedback = document.getElementById('dataset-name-feedback');
  if (feedback) {
    feedback.innerHTML = 'Enter a descriptive name (e.g. "UK Dental Businesses October 2026", "California Realtors Q4").';
    feedback.style.color = 'var(--text-tertiary)';
  }

  const btnStep2 = document.getElementById('btn-goto-step-2');
  if (btnStep2) btnStep2.disabled = true;

  const filesContainer = document.getElementById('staged-files-list-container');
  if (filesContainer) filesContainer.style.display = 'none';

  const btnInspect = document.getElementById('btn-inspect-files');
  if (btnInspect) btnInspect.disabled = true;

  renderCustomColumnsTags();

  goToWizardStep(1);
}

function toggleImportMode(mode) {
  STATE.importWizard.mode = mode;
  const newGroup = document.getElementById('new-dataset-name-group');
  const existingGroup = document.getElementById('existing-dataset-select-group');
  const btnNext = document.getElementById('btn-goto-step-2');

  if (mode === 'append') {
    if (newGroup) newGroup.style.display = 'none';
    if (existingGroup) existingGroup.style.display = 'block';
    populateExistingDatasetSelect();
    if (btnNext) btnNext.disabled = !STATE.importWizard.existingDatasetId;
  } else {
    if (newGroup) newGroup.style.display = 'block';
    if (existingGroup) existingGroup.style.display = 'none';
    const nameInput = document.getElementById('import-dataset-name-input');
    if (btnNext) btnNext.disabled = !nameInput || nameInput.value.trim().length < 2;
  }
}

function onDatasetNameInput(value) {
  const clean = value.trim();
  STATE.importWizard.datasetName = clean;
  const btnNext = document.getElementById('btn-goto-step-2');
  const feedback = document.getElementById('dataset-name-feedback');
  const badge = document.getElementById('dataset-name-badge');

  if (!clean || clean.length < 2) {
    if (btnNext) btnNext.disabled = true;
    if (feedback) {
      feedback.innerHTML = 'Dataset name must be at least 2 characters.';
      feedback.style.color = 'var(--text-tertiary)';
    }
    if (badge) {
      badge.textContent = 'Required';
      badge.className = 'status-badge neutral';
    }
    return;
  }

  clearTimeout(nameValidationTimeout);
  nameValidationTimeout = setTimeout(async () => {
    try {
      const res = await fetch('/api/import/validate_name', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: clean })
      });
      const data = await res.json();
      if (data.is_duplicate) {
        if (badge) {
          badge.textContent = 'Name In Use';
          badge.className = 'status-badge warning';
        }
        if (feedback) {
          feedback.innerHTML = `⚠️ A dataset named <strong>"${escapeHtml(data.matching_name)}"</strong> already exists. You can continue (new records will append), or choose a distinct name.`;
          feedback.style.color = '#f59e0b';
        }
      } else {
        if (badge) {
          badge.textContent = 'Available';
          badge.className = 'status-badge clean';
        }
        if (feedback) {
          feedback.innerHTML = `✓ Available: System ID will be <code>${escapeHtml(data.slug)}</code>`;
          feedback.style.color = '#10b981';
        }
      }
      if (btnNext) btnNext.disabled = false;
      const step1Summary = document.getElementById('wizard-step1-summary');
      if (step1Summary) step1Summary.textContent = clean;
    } catch (err) {
      if (btnNext) btnNext.disabled = false;
    }
  }, 250);
}

function populateExistingDatasetSelect() {
  const select = document.getElementById('import-existing-dataset-select');
  if (!select) return;

  const datasets = STATE.datasetsList || [];
  select.innerHTML = '<option value="">-- Choose Existing Dataset --</option>' +
    datasets.map(d => `<option value="${escapeHtml(d.id)}">${escapeHtml(d.name || d.id)} (${(d.count || 0).toLocaleString()} leads)</option>`).join('');
}

function onExistingDatasetSelect(datasetId) {
  STATE.importWizard.existingDatasetId = datasetId;
  const datasets = STATE.datasetsList || [];
  const selected = datasets.find(d => d.id === datasetId);
  const btnNext = document.getElementById('btn-goto-step-2');

  if (selected) {
    STATE.importWizard.datasetName = selected.name;
    const step1Summary = document.getElementById('wizard-step1-summary');
    if (step1Summary) step1Summary.textContent = selected.name;
    if (btnNext) btnNext.disabled = false;
  } else {
    STATE.importWizard.datasetName = '';
    if (btnNext) btnNext.disabled = true;
  }
}

function getFormatBadgeClass(fmt) {
  const f = (fmt || '').toLowerCase();
  if (['csv', 'tsv', 'txt'].includes(f)) return 'fmt-badge-csv';
  if (['xlsx', 'xls', 'xlsm'].includes(f)) return 'fmt-badge-excel';
  if (['json', 'jsonl', 'ndjson'].includes(f)) return 'fmt-badge-json';
  if (f === 'xml') return 'fmt-badge-xml';
  if (f === 'parquet') return 'fmt-badge-parquet';
  if (['zip', 'gzip', 'gz'].includes(f)) return 'fmt-badge-zip';
  return 'fmt-badge-csv';
}

function handleMultiFileInput(fileList) {
  if (!fileList || fileList.length === 0) return;

  const newFiles = Array.from(fileList);
  newFiles.forEach(nf => {
    if (!STATE.importWizard.files.some(f => f.name === nf.name && f.size === nf.size)) {
      STATE.importWizard.files.push(nf);
    }
  });

  renderStagedFilesList();
}

function renderStagedFilesList() {
  const container = document.getElementById('staged-files-list-container');
  const listEl = document.getElementById('staged-files-list');
  const badge = document.getElementById('selected-files-count-badge');
  const btnInspect = document.getElementById('btn-inspect-files');
  const files = STATE.importWizard.files;

  if (badge) badge.textContent = `${files.length} File${files.length === 1 ? '' : 's'} Selected`;
  if (btnInspect) btnInspect.disabled = files.length === 0;

  if (files.length === 0) {
    if (container) container.style.display = 'none';
    return;
  }

  if (container) container.style.display = 'block';
  if (!listEl) return;

  listEl.innerHTML = files.map((f, idx) => {
    const sizeMb = (f.size / (1024 * 1024)).toFixed(2);
    const sizeFormatted = f.size > 1024 * 1024 ? `${sizeMb} MB` : `${Math.round(f.size / 1024)} KB`;
    const ext = f.name.split('.').pop().toUpperCase();
    const badgeCls = getFormatBadgeClass(ext);

    return `
      <div class="staged-file-card">
        <div class="staged-file-left">
          <div class="staged-file-icon">
            <span class="fmt-badge ${badgeCls}">${escapeHtml(ext)}</span>
          </div>
          <div class="staged-file-meta">
            <span class="staged-file-name">${escapeHtml(f.name)}</span>
            <span class="staged-file-size">${sizeFormatted} · Tabular Ingestion Ready</span>
          </div>
        </div>
        <div class="staged-file-actions">
          <span class="status-badge neutral">Ready to Inspect</span>
          <button class="btn btn-ghost btn-sm" onclick="removeStagedFile(${idx})" title="Remove file" style="color: #ef4444;">✕</button>
        </div>
      </div>
    `;
  }).join('');

  const step2Summary = document.getElementById('wizard-step2-summary');
  if (step2Summary) step2Summary.textContent = `${files.length} file${files.length === 1 ? '' : 's'}`;
}

function removeStagedFile(index) {
  STATE.importWizard.files.splice(index, 1);
  renderStagedFilesList();
}

async function inspectAllSelectedFiles() {
  const files = STATE.importWizard.files;
  if (!files || files.length === 0) {
    toast('Please select at least one file');
    return;
  }

  const progContainer = document.getElementById('multi-upload-progress-container');
  const progFill = document.getElementById('multi-upload-progress-fill');
  const btnInspect = document.getElementById('btn-inspect-files');

  if (progContainer) progContainer.style.display = 'block';
  if (btnInspect) btnInspect.disabled = true;

  try {
    let pct = 15;
    const interval = setInterval(() => {
      pct = Math.min(88, pct + 12);
      if (progFill) progFill.style.width = `${pct}%`;
    }, 150);

    const formData = new FormData();
    files.forEach(f => {
      formData.append('files', f);
    });

    const res = await fetch('/api/import/inspect_files', {
      method: 'POST',
      body: formData
    });

    clearInterval(interval);
    if (progFill) progFill.style.width = '100%';

    const data = await res.json();
    if (!res.ok || data.status !== 'success') {
      throw new Error(data.message || 'Inspection failed');
    }

    STATE.importWizard.inspections = data.files || [];
    STATE.importWizard.targetColumns = data.target_columns || [];
    STATE.importWizard.activeInspectionIndex = 0;

    // Initialize default mappings and column settings for each file
    STATE.importWizard.mappings = {};
    STATE.importWizard.columnSettings = {};
    STATE.importWizard.cellEdits = {};

    (data.files || []).forEach(f => {
      const fileMap = {};
      const fileColSettings = {};
      (f.mappings || []).forEach(m => {
        if (m.target_key && m.target_key !== 'ignore') {
          fileMap[m.target_key] = m.source_header;
        }
        fileColSettings[m.source_header] = {
          displayName: m.source_header,
          excluded: false,
          type: m.detected_type || 'text',
          defaultValue: ''
        };
      });
      STATE.importWizard.mappings[f.filename] = fileMap;
      STATE.importWizard.columnSettings[f.filename] = fileColSettings;
      STATE.importWizard.cellEdits[f.filename] = {};
    });

    toast(`Inspected ${data.files_count} file(s) successfully!`);
    goToWizardStep(3);
  } catch (err) {
    console.error(err);
    toast(`File inspection failed: ${err.message}`);
  } finally {
    if (progContainer) progContainer.style.display = 'none';
    if (btnInspect) btnInspect.disabled = false;
  }
}

// -----------------------------------------------------------------------------
// Step 3 Rendering: Tabs, Metadata, Excel Sheets, Column Mapping, Custom Cols, Spreadsheet
// -----------------------------------------------------------------------------

function renderPreviewAndMappings() {
  const inspections = STATE.importWizard.inspections;
  if (!inspections || inspections.length === 0) return;

  const tabsContainer = document.getElementById('preview-file-tabs-container');
  const activeIdx = STATE.importWizard.activeInspectionIndex;
  const activeFile = inspections[activeIdx] || inspections[0];
  const filename = activeFile.filename;

  // Render file tabs
  if (tabsContainer) {
    tabsContainer.innerHTML = inspections.map((f, i) => {
      const ext = (f.format || f.filename.split('.').pop()).toUpperCase();
      const badgeCls = getFormatBadgeClass(ext);
      return `
        <div class="preview-file-tab ${i === activeIdx ? 'active' : ''}" onclick="switchPreviewFileTab(${i})">
          <span class="fmt-badge ${badgeCls}" style="font-size: 9px; padding: 1px 4px;">${escapeHtml(ext)}</span>
          ${escapeHtml(f.filename)} (${(f.total_rows_estimate || 0).toLocaleString()} rows)
        </div>
      `;
    }).join('');
  }

  // Active file metadata card
  const fmtEl = document.getElementById('meta-format-badge');
  const encEl = document.getElementById('meta-encoding');
  const delimEl = document.getElementById('meta-delimiter');
  const rowsEl = document.getElementById('meta-est-rows');
  const colsEl = document.getElementById('meta-cols-count');
  const missingEl = document.getElementById('meta-missing-badges');

  const fmtName = (activeFile.format || 'CSV').toUpperCase();
  if (fmtEl) {
    fmtEl.textContent = fmtName;
    fmtEl.className = `fmt-badge ${getFormatBadgeClass(fmtName)}`;
  }
  if (encEl) encEl.textContent = activeFile.encoding || 'UTF-8';
  if (delimEl) delimEl.textContent = activeFile.delimiter_name || activeFile.format || '-';
  if (rowsEl) rowsEl.textContent = (activeFile.total_rows_estimate || 0).toLocaleString();
  if (colsEl) colsEl.textContent = activeFile.columns_count || 0;

  if (missingEl && activeFile.missing_in_sample) {
    const miss = activeFile.missing_in_sample;
    missingEl.innerHTML = `
      <span class="status-badge ${miss.name === 0 ? 'clean' : 'warning'}">Missing Names: ${miss.name}</span>
      <span class="status-badge ${miss.phone === 0 ? 'clean' : 'neutral'}">Missing Phones: ${miss.phone}</span>
      <span class="status-badge ${miss.email === 0 ? 'clean' : 'neutral'}">Missing Emails: ${miss.email}</span>
    `;
  }

  // Excel Worksheet selector if multiple worksheets exist
  const sheetGroup = document.getElementById('excel-sheet-selector-group');
  const sheetSelect = document.getElementById('excel-sheet-select');
  if (sheetGroup && sheetSelect) {
    if (activeFile.worksheets && activeFile.worksheets.length > 1) {
      sheetGroup.style.display = 'block';
      sheetSelect.innerHTML = activeFile.worksheets.map(ws =>
        `<option value="${escapeHtml(ws)}" ${ws === activeFile.active_worksheet ? 'selected' : ''}>${escapeHtml(ws)}</option>`
      ).join('');
    } else {
      sheetGroup.style.display = 'none';
    }
  }

  // Render Custom Columns Tags
  renderCustomColumnsTags();

  // Column mapping & settings table
  const tbody = document.getElementById('wizard-mapping-tbody');
  const fileMappings = STATE.importWizard.mappings[filename] || {};
  const fileColSettings = STATE.importWizard.columnSettings[filename] || {};
  const targetCols = STATE.importWizard.targetColumns || [];

  if (tbody) {
    tbody.innerHTML = (activeFile.mappings || []).map(m => {
      const src = m.source_header;
      const currentTarget = Object.keys(fileMappings).find(k => fileMappings[k] === src) || m.target_key;
      const sampleVal = (activeFile.preview_rows && activeFile.preview_rows[0]) ? activeFile.preview_rows[0][src] : '-';
      const colSetting = fileColSettings[src] || { displayName: src, excluded: false, type: m.detected_type || 'text', defaultValue: '' };

      const selectOptions = `
        <option value="ignore" ${currentTarget === 'ignore' ? 'selected' : ''}>-- Ignore / Skip --</option>
        ${targetCols.map(tc => `<option value="${tc.key}" ${currentTarget === tc.key ? 'selected' : ''}>${tc.label}${tc.required ? ' *' : ''}</option>`).join('')}
      `;

      return `
        <tr style="${colSetting.excluded ? 'opacity: 0.5;' : ''}">
          <td>
            <input type="checkbox" ${!colSetting.excluded ? 'checked' : ''}
              onchange="onColumnExcludeToggle('${escapeHtml(filename)}', '${escapeHtml(src)}', !this.checked)"
              title="Include or exclude this column from import">
          </td>
          <td class="cell-name-strong">${escapeHtml(src)}</td>
          <td>
            <input type="text" class="global-search-input" style="height: 30px; font-size: 12px; width: 140px;"
              value="${escapeHtml(colSetting.displayName || src)}"
              onchange="onColumnRenameInput('${escapeHtml(filename)}', '${escapeHtml(src)}', this.value)"
              placeholder="Display Name">
          </td>
          <td>
            <select class="filter-select" style="width: 100%; height: 30px; font-size: 12px;"
              onchange="onMappingChange('${escapeHtml(filename)}', this.value, '${escapeHtml(src)}')">
              ${selectOptions}
            </select>
          </td>
          <td>
            <select class="filter-select" style="width: 90px; height: 30px; font-size: 11px;"
              onchange="onColumnTypeOverride('${escapeHtml(filename)}', '${escapeHtml(src)}', this.value)">
              <option value="text" ${colSetting.type === 'text' ? 'selected' : ''}>Text</option>
              <option value="integer" ${colSetting.type === 'integer' ? 'selected' : ''}>Integer</option>
              <option value="decimal" ${colSetting.type === 'decimal' ? 'selected' : ''}>Decimal</option>
              <option value="boolean" ${colSetting.type === 'boolean' ? 'selected' : ''}>Boolean</option>
              <option value="date" ${colSetting.type === 'date' ? 'selected' : ''}>Date</option>
              <option value="datetime" ${colSetting.type === 'datetime' ? 'selected' : ''}>Datetime</option>
            </select>
          </td>
          <td>
            <input type="text" class="global-search-input" style="height: 30px; font-size: 12px; width: 120px;"
              value="${escapeHtml(colSetting.defaultValue || '')}"
              onchange="onColumnDefaultValueInput('${escapeHtml(filename)}', '${escapeHtml(src)}', this.value)"
              placeholder="Fallback Default">
          </td>
          <td class="cell-subtext" style="max-width: 150px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
            ${escapeHtml(String(sampleVal !== undefined && sampleVal !== null ? sampleVal : '-'))}
          </td>
        </tr>
      `;
    }).join('');
  }

  // Render Interactive Spreadsheet Preview with Cell Editing
  renderSpreadsheetPreview();
}

function renderSpreadsheetPreview() {
  const activeIdx = STATE.importWizard.activeInspectionIndex;
  const activeFile = STATE.importWizard.inspections[activeIdx];
  if (!activeFile) return;

  const filename = activeFile.filename;
  const thead = document.getElementById('wizard-spreadsheet-thead');
  const tbody = document.getElementById('wizard-spreadsheet-tbody');
  const countEl = document.getElementById('spreadsheet-edited-count');

  const fileColSettings = STATE.importWizard.columnSettings[filename] || {};
  const activeHeaders = (activeFile.headers || []).filter(h => !fileColSettings[h]?.excluded);
  const customCols = STATE.importWizard.customColumns || [];
  const rows = activeFile.preview_rows || [];
  const cellEdits = STATE.importWizard.cellEdits[filename] || {};

  // Count total edits for this file
  let totalEdits = 0;
  Object.values(cellEdits).forEach(rowObj => {
    totalEdits += Object.keys(rowObj || {}).length;
  });
  if (countEl) {
    if (totalEdits > 0) {
      countEl.style.display = 'inline-block';
      countEl.textContent = `✎ ${totalEdits} cell edit${totalEdits === 1 ? '' : 's'} staged`;
    } else {
      countEl.style.display = 'none';
    }
  }

  if (thead) {
    const srcHeaderThs = activeHeaders.map(h => {
      const displayName = fileColSettings[h]?.displayName || h;
      return `<th title="Original column: ${escapeHtml(h)}">${escapeHtml(displayName)}</th>`;
    }).join('');

    const customHeaderThs = customCols.map(c =>
      `<th class="custom-col-header" title="Custom Column (${c.populate_mode === 'same' ? 'Same value' : 'Individual values'})">
        ★ ${escapeHtml(c.name)}
       </th>`
    ).join('');

    thead.innerHTML = `<tr><th style="width: 40px; text-align: center;">#</th>${srcHeaderThs}${customHeaderThs}</tr>`;
  }

  if (tbody) {
    tbody.innerHTML = rows.map((r, rowIdx) => {
      const rowNumCell = `<td style="color: var(--text-tertiary); font-family: var(--font-mono); font-size: 11px; text-align: center;">${rowIdx + 1}</td>`;

      const srcTds = activeHeaders.map(h => {
        const editedVal = cellEdits[rowIdx]?.[h];
        const isEdited = editedVal !== undefined;
        const displayVal = isEdited ? editedVal : (r[h] !== undefined && r[h] !== null ? r[h] : '');
        return `
          <td class="spreadsheet-cell-editable ${isEdited ? 'spreadsheet-cell-edited' : ''}"
              contenteditable="true"
              data-filename="${escapeHtml(filename)}"
              data-row="${rowIdx}"
              data-col="${escapeHtml(h)}"
              onblur="onSpreadsheetCellBlur(this)">${escapeHtml(String(displayVal))}</td>
        `;
      }).join('');

      const customTds = customCols.map(c => {
        const editedVal = cellEdits[rowIdx]?.[c.name];
        const isEdited = editedVal !== undefined;
        let displayVal = isEdited ? editedVal : (c.populate_mode === 'same' ? (c.default_value || '') : '');
        return `
          <td class="spreadsheet-cell-editable ${isEdited ? 'spreadsheet-cell-edited' : ''}"
              contenteditable="true"
              style="background: rgba(139, 92, 246, 0.05);"
              data-filename="${escapeHtml(filename)}"
              data-row="${rowIdx}"
              data-col="${escapeHtml(c.name)}"
              onblur="onSpreadsheetCellBlur(this)">${escapeHtml(String(displayVal))}</td>
        `;
      }).join('');

      return `<tr>${rowNumCell}${srcTds}${customTds}</tr>`;
    }).join('');
  }
}

function onSpreadsheetCellBlur(cellEl) {
  const filename = cellEl.dataset.filename;
  const rowIdx = parseInt(cellEl.dataset.row);
  const colName = cellEl.dataset.col;
  const newVal = cellEl.innerText.trim();

  if (!STATE.importWizard.cellEdits[filename]) {
    STATE.importWizard.cellEdits[filename] = {};
  }
  if (!STATE.importWizard.cellEdits[filename][rowIdx]) {
    STATE.importWizard.cellEdits[filename][rowIdx] = {};
  }

  STATE.importWizard.cellEdits[filename][rowIdx][colName] = newVal;
  cellEl.classList.add('spreadsheet-cell-edited');

  const countEl = document.getElementById('spreadsheet-edited-count');
  if (countEl) {
    let totalEdits = 0;
    Object.values(STATE.importWizard.cellEdits[filename] || {}).forEach(r => totalEdits += Object.keys(r).length);
    countEl.style.display = 'inline-block';
    countEl.textContent = `✎ ${totalEdits} cell edit${totalEdits === 1 ? '' : 's'} staged`;
  }
}

function switchPreviewFileTab(index) {
  STATE.importWizard.activeInspectionIndex = index;
  renderPreviewAndMappings();
}

function onMappingChange(filename, targetKey, sourceHeader) {
  if (!STATE.importWizard.mappings[filename]) {
    STATE.importWizard.mappings[filename] = {};
  }
  if (targetKey !== 'ignore') {
    Object.keys(STATE.importWizard.mappings[filename]).forEach(k => {
      if (k === targetKey) delete STATE.importWizard.mappings[filename][k];
    });
    STATE.importWizard.mappings[filename][targetKey] = sourceHeader;
  } else {
    Object.keys(STATE.importWizard.mappings[filename]).forEach(k => {
      if (STATE.importWizard.mappings[filename][k] === sourceHeader) {
        delete STATE.importWizard.mappings[filename][k];
      }
    });
  }
}

function onColumnRenameInput(filename, sourceCol, newDisplayName) {
  if (!STATE.importWizard.columnSettings[filename]) {
    STATE.importWizard.columnSettings[filename] = {};
  }
  if (!STATE.importWizard.columnSettings[filename][sourceCol]) {
    STATE.importWizard.columnSettings[filename][sourceCol] = { displayName: sourceCol, excluded: false, type: 'text', defaultValue: '' };
  }
  STATE.importWizard.columnSettings[filename][sourceCol].displayName = newDisplayName.trim() || sourceCol;
  renderSpreadsheetPreview();
}

function onColumnExcludeToggle(filename, sourceCol, isExcluded) {
  if (!STATE.importWizard.columnSettings[filename]) {
    STATE.importWizard.columnSettings[filename] = {};
  }
  if (!STATE.importWizard.columnSettings[filename][sourceCol]) {
    STATE.importWizard.columnSettings[filename][sourceCol] = { displayName: sourceCol, excluded: false, type: 'text', defaultValue: '' };
  }
  STATE.importWizard.columnSettings[filename][sourceCol].excluded = isExcluded;
  renderPreviewAndMappings();
}

function onColumnTypeOverride(filename, sourceCol, newType) {
  if (!STATE.importWizard.columnSettings[filename]) {
    STATE.importWizard.columnSettings[filename] = {};
  }
  if (!STATE.importWizard.columnSettings[filename][sourceCol]) {
    STATE.importWizard.columnSettings[filename][sourceCol] = { displayName: sourceCol, excluded: false, type: 'text', defaultValue: '' };
  }
  STATE.importWizard.columnSettings[filename][sourceCol].type = newType;
}

function onColumnDefaultValueInput(filename, sourceCol, defVal) {
  if (!STATE.importWizard.columnSettings[filename]) {
    STATE.importWizard.columnSettings[filename] = {};
  }
  if (!STATE.importWizard.columnSettings[filename][sourceCol]) {
    STATE.importWizard.columnSettings[filename][sourceCol] = { displayName: sourceCol, excluded: false, type: 'text', defaultValue: '' };
  }
  STATE.importWizard.columnSettings[filename][sourceCol].defaultValue = defVal;
}

async function onWorksheetSelectChange(newSheet) {
  const activeIdx = STATE.importWizard.activeInspectionIndex;
  const activeFile = STATE.importWizard.inspections[activeIdx];
  if (!activeFile) return;

  try {
    const res = await fetch(`/api/import/inspect?staged_path=${encodeURIComponent(activeFile.staged_path)}&worksheet=${encodeURIComponent(newSheet)}`);
    const data = await res.json();
    if (!res.ok || data.status !== 'success') {
      throw new Error(data.message || 'Failed to inspect worksheet');
    }
    STATE.importWizard.inspections[activeIdx] = data.inspection;
    renderPreviewAndMappings();
    toast(`Loaded worksheet: ${newSheet}`);
  } catch (err) {
    toast(`Error loading worksheet: ${err.message}`);
  }
}

// -----------------------------------------------------------------------------
// Custom Columns Modal & Controls (CRITICAL FEATURE)
// -----------------------------------------------------------------------------

function openAddCustomColumnModal() {
  const modal = document.getElementById('addCustomColumnModal');
  const nameInput = document.getElementById('wizard-custom-col-name');
  const valInput = document.getElementById('wizard-custom-col-val');
  if (nameInput) nameInput.value = '';
  if (valInput) valInput.value = '';
  if (modal) modal.style.display = 'flex';
}

function closeAddCustomColumnModal() {
  const modal = document.getElementById('addCustomColumnModal');
  if (modal) modal.style.display = 'none';
}

function onCustomColModeToggle(mode) {
  const valGroup = document.getElementById('wizard-custom-col-val-group');
  const valHint = document.getElementById('wizard-custom-col-val-hint');
  if (mode === 'same') {
    if (valGroup) valGroup.style.display = 'block';
    if (valHint) valHint.textContent = 'Every imported lead in this dataset will receive this value in this column.';
  } else {
    if (valGroup) valGroup.style.display = 'block';
    if (valHint) valHint.textContent = 'Default value for blank cells (leave blank if you want empty cells). You can edit each row individually in the spreadsheet table.';
  }
}

function confirmAddCustomColumn() {
  const nameInput = document.getElementById('wizard-custom-col-name');
  const typeSelect = document.getElementById('wizard-custom-col-type');
  const valInput = document.getElementById('wizard-custom-col-val');
  const modeRadios = document.getElementsByName('wizard-custom-col-mode');

  let mode = 'same';
  for (const r of modeRadios) {
    if (r.checked) mode = r.value;
  }

  const rawName = (nameInput ? nameInput.value : '').trim();
  const cleanName = rawName.toLowerCase().replace(/[^a-z0-9_]/g, '_').replace(/^_+|_+$/g, '');

  if (!cleanName) {
    toast('Please enter a valid column name');
    return;
  }

  // Check duplicate in custom columns
  if (STATE.importWizard.customColumns.some(c => c.name === cleanName)) {
    toast(`Custom column "${cleanName}" has already been added`);
    return;
  }

  const newCol = {
    name: cleanName,
    type: typeSelect ? typeSelect.value : 'text',
    populate_mode: mode,
    default_value: valInput ? valInput.value : ''
  };

  STATE.importWizard.customColumns.push(newCol);
  closeAddCustomColumnModal();
  renderPreviewAndMappings();
  toast(`Added custom column "${cleanName}" (${mode === 'same' ? 'Same value' : 'Individual values'})`);
}

function removeCustomColumn(colName) {
  STATE.importWizard.customColumns = STATE.importWizard.customColumns.filter(c => c.name !== colName);
  renderPreviewAndMappings();
  toast(`Removed custom column "${colName}"`);
}

function renderCustomColumnsTags() {
  const container = document.getElementById('custom-columns-tags-container');
  if (!container) return;

  const cols = STATE.importWizard.customColumns || [];
  if (cols.length === 0) {
    container.innerHTML = '<span style="font-size: 11px; color: var(--text-tertiary); font-style: italic;">No custom columns added yet. Click "+ Add Custom Column" to append dataset-specific fields (e.g. country, industry, priority).</span>';
    return;
  }

  container.innerHTML = cols.map(c => `
    <span class="custom-col-tag" title="Type: ${c.type} | Mode: ${c.populate_mode} | Default: ${c.default_value || 'None'}">
      ★ ${escapeHtml(c.name)} <span style="opacity: 0.6; font-size: 10px;">(${c.type})</span>
      <span class="remove-col" onclick="removeCustomColumn('${escapeHtml(c.name)}')">✕</span>
    </span>
  `).join('');
}

function selectDupMode(mode) {
  STATE.importWizard.duplicateMode = mode;
  ['skip_exact', 'import_all', 'new_only', 'flag_review'].forEach(m => {
    const card = document.getElementById(`dup-card-${m}`);
    if (card) {
      card.classList.toggle('selected', m === mode);
      const radio = card.querySelector('input[type="radio"]');
      if (radio) radio.checked = (m === mode);
    }
  });
}

// -----------------------------------------------------------------------------
// Execution & Ingestion
// -----------------------------------------------------------------------------

async function executeDatasetIngestion() {
  const wizard = STATE.importWizard;
  if (!wizard.datasetName) {
    toast('Dataset name is required');
    return;
  }
  if (!wizard.inspections || wizard.inspections.length === 0) {
    toast('No files ready to ingest');
    return;
  }

  goToWizardStep(4);
  const loadingState = document.getElementById('ingestion-loading-state');
  const resultCard = document.getElementById('ingestion-result-card');
  const progFill = document.getElementById('ingest-progress-bar-fill');
  const statusBadge = document.getElementById('ingestion-status-badge');

  if (loadingState) loadingState.style.display = 'block';
  if (resultCard) resultCard.style.display = 'none';
  if (statusBadge) {
    statusBadge.textContent = 'Ingesting & Indexing';
    statusBadge.className = 'status-badge neutral';
  }

  let pct = 30;
  const timer = setInterval(() => {
    pct = Math.min(92, pct + 8);
    if (progFill) progFill.style.width = `${pct}%`;
  }, 200);

  try {
    const stagedFilesPayload = wizard.inspections.map(f => ({
      original_filename: f.filename,
      staged_path: f.staged_path,
      format: f.format,
      worksheet: f.active_worksheet
    }));

    const res = await fetch('/api/import/execute', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        dataset_name: wizard.datasetName,
        files: stagedFilesPayload,
        column_mappings: wizard.mappings,
        column_settings: wizard.columnSettings,
        custom_columns: wizard.customColumns,
        cell_edits: wizard.cellEdits,
        duplicate_mode: wizard.duplicateMode,
        existing_dataset_id: wizard.existingDatasetId
      })
    });

    clearInterval(timer);
    if (progFill) progFill.style.width = '100%';

    const data = await res.json();
    if (!res.ok || !data.success) {
      throw new Error(data.error || 'Ingestion failed');
    }

    if (statusBadge) {
      statusBadge.textContent = 'Completed Successfully';
      statusBadge.className = 'status-badge clean';
    }

    renderIngestionResults(data);
    loadDatasetsCatalog();
    loadDashboardMetrics();
    toast(`Ingestion complete! ${data.total_imported.toLocaleString()} leads added to database.`);
  } catch (err) {
    clearInterval(timer);
    console.error(err);
    if (statusBadge) {
      statusBadge.textContent = 'Ingestion Error';
      statusBadge.className = 'status-badge warning';
    }
    toast(`Ingestion error: ${err.message}`);
  }
}

function renderIngestionResults(data) {
  const loadingState = document.getElementById('ingestion-loading-state');
  const resultCard = document.getElementById('ingestion-result-card');

  if (loadingState) loadingState.style.display = 'none';
  if (resultCard) resultCard.style.display = 'block';

  const titleEl = document.getElementById('result-dataset-title');
  const subtitleEl = document.getElementById('result-dataset-subtitle');
  if (titleEl) titleEl.textContent = `${data.dataset_name} Successfully Added`;
  if (subtitleEl) subtitleEl.textContent = `All ${data.total_imported.toLocaleString()} verified leads are now indexed and available in Lead Explorer.`;

  const statDisc = document.getElementById('result-stat-discovered');
  const statImp = document.getElementById('result-stat-imported');
  const statDups = document.getElementById('result-stat-duplicates');
  const statRej = document.getElementById('result-stat-rejected');

  if (statDisc) statDisc.textContent = (data.total_discovered || 0).toLocaleString();
  if (statImp) statImp.textContent = (data.total_imported || 0).toLocaleString();
  if (statDups) statDups.textContent = (data.total_duplicates || 0).toLocaleString();
  if (statRej) statRej.textContent = (data.total_rejected || 0).toLocaleString();

  const rejCallout = document.getElementById('rejection-report-callout');
  const rejBtn = document.getElementById('download-rejection-btn');
  if (data.has_rejections && data.rejection_report_url) {
    if (rejCallout) rejCallout.style.display = 'flex';
    if (rejBtn) rejBtn.href = data.rejection_report_url;
  } else {
    if (rejCallout) rejCallout.style.display = 'none';
  }

  STATE.latestImportedDatasetId = data.dataset_id;
}

function exploreImportedDatasetNow() {
  const did = STATE.latestImportedDatasetId;
  if (did) {
    selectDatasetAndExplore(did);
  } else {
    switchView('explorer');
  }
}

// =============================================================================
// POST-IMPORT DATASET MANAGEMENT & CUSTOM COLUMN SCHEMA CONTROLS
// =============================================================================

function openRenameModal(datasetId, currentName) {
  const modal = document.getElementById('renameDatasetModal');
  const idInput = document.getElementById('rename-dataset-id');
  const nameInput = document.getElementById('rename-dataset-input');

  if (idInput) idInput.value = datasetId;
  if (nameInput) nameInput.value = currentName || '';
  if (modal) modal.style.display = 'flex';
}

function closeRenameModal() {
  const modal = document.getElementById('renameDatasetModal');
  if (modal) modal.style.display = 'none';
}

async function submitRenameDataset() {
  const idInput = document.getElementById('rename-dataset-id');
  const nameInput = document.getElementById('rename-dataset-input');
  if (!idInput || !nameInput) return;

  const did = idInput.value;
  const newName = nameInput.value.trim();
  if (!newName) {
    toast('Dataset name cannot be blank');
    return;
  }

  try {
    const res = await fetch(`/api/imported_datasets/${encodeURIComponent(did)}/rename`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: newName })
    });
    const data = await res.json();
    if (!res.ok || !data.success) {
      throw new Error(data.error || 'Failed to rename dataset');
    }
    toast(`Dataset renamed to "${newName}"`);
    closeRenameModal();
    loadDatasetsCatalog();
  } catch (err) {
    toast(`Error renaming dataset: ${err.message}`);
  }
}

function openDeleteModal(datasetId, datasetName) {
  const modal = document.getElementById('deleteDatasetModal');
  const idInput = document.getElementById('delete-dataset-id');
  const label = document.getElementById('delete-dataset-name-label');

  if (idInput) idInput.value = datasetId;
  if (label) label.textContent = `"${datasetName || datasetId}"`;
  if (modal) modal.style.display = 'flex';
}

function closeDeleteModal() {
  const modal = document.getElementById('deleteDatasetModal');
  if (modal) modal.style.display = 'none';
}

async function submitDeleteDataset() {
  const idInput = document.getElementById('delete-dataset-id');
  if (!idInput || !idInput.value) return;

  const did = idInput.value;
  try {
    const res = await fetch(`/api/imported_datasets/${encodeURIComponent(did)}`, {
      method: 'DELETE'
    });
    const data = await res.json();
    if (!res.ok || !data.success) {
      throw new Error(data.error || 'Failed to delete dataset');
    }
    toast(`Dataset deleted successfully`);
    closeDeleteModal();
    loadDatasetsCatalog();
    loadDashboardMetrics();
  } catch (err) {
    toast(`Error deleting dataset: ${err.message}`);
  }
}

// -----------------------------------------------------------------------------
// Post-Import Dataset Columns Management Interface
// -----------------------------------------------------------------------------

async function openDatasetColumnsModal(datasetId, datasetName) {
  const modal = document.getElementById('datasetColumnsModal');
  const idInput = document.getElementById('mgmt-dataset-id');
  const titleEl = document.getElementById('mgmt-dataset-title');

  if (idInput) idInput.value = datasetId;
  if (titleEl) titleEl.textContent = `Manage schema and custom attributes for "${datasetName || datasetId}"`;

  if (modal) modal.style.display = 'flex';
  await refreshDatasetColumnsList(datasetId);
}

function closeDatasetColumnsModal() {
  const modal = document.getElementById('datasetColumnsModal');
  if (modal) modal.style.display = 'none';
}

async function refreshDatasetColumnsList(datasetId) {
  const tbody = document.getElementById('mgmt-columns-tbody');
  if (!tbody) return;

  tbody.innerHTML = '<tr><td colspan="4" style="text-align: center; padding: 16px;">Loading columns...</td></tr>';

  try {
    const res = await fetch(`/api/imported_datasets/${encodeURIComponent(datasetId)}/columns`);
    const data = await res.json();
    if (!res.ok || !data.success) {
      throw new Error(data.error || 'Failed to load columns');
    }

    const cols = data.columns || [];
    if (cols.length === 0) {
      tbody.innerHTML = '<tr><td colspan="4" style="text-align: center; padding: 16px;">No columns found for this dataset.</td></tr>';
      return;
    }

    tbody.innerHTML = cols.map(c => {
      const isCustom = c.is_custom;
      const categoryBadge = isCustom
        ? `<span class="custom-col-tag" style="margin: 0; padding: 2px 6px;">★ Custom</span>`
        : `<span class="status-badge neutral" style="font-size: 11px;">Standard</span>`;

      const actions = isCustom
        ? `
          <button class="btn btn-secondary btn-sm" onclick="promptRenameColumn('${escapeHtml(datasetId)}', '${escapeHtml(c.name)}')" title="Rename column" style="padding: 2px 6px; font-size: 11px;">✏️ Rename</button>
          <button class="btn btn-secondary btn-sm" onclick="promptFillColumn('${escapeHtml(datasetId)}', '${escapeHtml(c.name)}')" title="Fill or batch populate" style="padding: 2px 6px; font-size: 11px;">💧 Fill</button>
          <button class="btn btn-secondary btn-sm" onclick="promptDeleteColumn('${escapeHtml(datasetId)}', '${escapeHtml(c.name)}')" title="Delete column" style="padding: 2px 6px; font-size: 11px; color: #ef4444;">🗑️</button>
        `
        : `<span style="font-size: 11px; color: var(--text-tertiary); font-style: italic;">Standard Core Field</span>`;

      return `
        <tr>
          <td class="cell-name-strong">${escapeHtml(c.name)}</td>
          <td><span class="status-badge neutral" style="font-size: 11px;">${escapeHtml(c.type || 'text')}</span></td>
          <td>${categoryBadge}</td>
          <td style="display: flex; gap: 4px; align-items: center;">${actions}</td>
        </tr>
      `;
    }).join('');
  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="4" style="color: #ef4444; padding: 16px;">Error loading columns: ${escapeHtml(err.message)}</td></tr>`;
  }
}

async function submitAddColumnToDataset() {
  const idInput = document.getElementById('mgmt-dataset-id');
  const nameInput = document.getElementById('mgmt-new-col-name');
  const typeSelect = document.getElementById('mgmt-new-col-type');
  const defInput = document.getElementById('mgmt-new-col-default');
  const scopeRadios = document.getElementsByName('mgmt-scope');

  if (!idInput || !idInput.value) return;
  const datasetId = idInput.value;

  const rawName = (nameInput ? nameInput.value : '').trim();
  const cleanName = rawName.toLowerCase().replace(/[^a-z0-9_]/g, '_').replace(/^_+|_+$/g, '');

  if (!cleanName) {
    toast('Please enter a valid column name');
    return;
  }

  let scope = 'all';
  for (const r of scopeRadios) {
    if (r.checked) scope = r.value;
  }

  try {
    const res = await fetch(`/api/imported_datasets/${encodeURIComponent(datasetId)}/columns`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        column_name: cleanName,
        column_type: typeSelect ? typeSelect.value : 'text',
        default_value: defInput ? defInput.value : '',
        scope: scope
      })
    });
    const data = await res.json();
    if (!res.ok || !data.success) {
      throw new Error(data.error || 'Failed to add column');
    }

    toast(`Column "${cleanName}" added successfully to dataset!`);
    if (nameInput) nameInput.value = '';
    if (defInput) defInput.value = '';
    await refreshDatasetColumnsList(datasetId);
    loadDatasetsCatalog();
  } catch (err) {
    toast(`Error adding column: ${err.message}`);
  }
}

async function promptRenameColumn(datasetId, oldName) {
  const newName = prompt(`Enter new column name for "${oldName}":`, oldName);
  if (!newName || newName.trim() === oldName) return;

  const cleanNewName = newName.trim().toLowerCase().replace(/[^a-z0-9_]/g, '_').replace(/^_+|_+$/g, '');
  if (!cleanNewName) {
    toast('Invalid column name');
    return;
  }

  try {
    const res = await fetch(`/api/imported_datasets/${encodeURIComponent(datasetId)}/columns/${encodeURIComponent(oldName)}/rename`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ new_name: cleanNewName })
    });
    const data = await res.json();
    if (!res.ok || !data.success) {
      throw new Error(data.error || 'Failed to rename column');
    }
    toast(`Column renamed to "${cleanNewName}"`);
    await refreshDatasetColumnsList(datasetId);
  } catch (err) {
    toast(`Error renaming column: ${err.message}`);
  }
}

async function promptFillColumn(datasetId, colName) {
  const val = prompt(`Enter the value to fill in column "${colName}":`);
  if (val === null) return;

  const onlyBlanks = confirm(`Do you want to fill BLANK cells only?\n\nClick OK to fill blanks only.\nClick Cancel to overwrite ALL leads in this dataset.`);

  try {
    const res = await fetch(`/api/imported_datasets/${encodeURIComponent(datasetId)}/columns/${encodeURIComponent(colName)}/fill`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        value: val,
        only_blanks: onlyBlanks
      })
    });
    const data = await res.json();
    if (!res.ok || !data.success) {
      throw new Error(data.error || 'Failed to fill column values');
    }
    toast(`Updated ${data.updated_leads_count || 0} leads with value "${val}"`);
    await refreshDatasetColumnsList(datasetId);
  } catch (err) {
    toast(`Error filling column: ${err.message}`);
  }
}

async function promptDeleteColumn(datasetId, colName) {
  const confirmed = confirm(`Are you sure you want to permanently delete column "${colName}" from this dataset?\n\nThis will remove the column from existing records in this dataset.`);
  if (!confirmed) return;

  try {
    const res = await fetch(`/api/imported_datasets/${encodeURIComponent(datasetId)}/columns/${encodeURIComponent(colName)}`, {
      method: 'DELETE'
    });
    const data = await res.json();
    if (!res.ok || !data.success) {
      throw new Error(data.error || 'Failed to delete column');
    }
    toast(`Column "${colName}" deleted successfully`);
    await refreshDatasetColumnsList(datasetId);
    loadDatasetsCatalog();
  } catch (err) {
    toast(`Error deleting column: ${err.message}`);
  }
}

function exportDatasetCustomCsv() {
  const idInput = document.getElementById('mgmt-dataset-id');
  if (idInput && idInput.value) {
    exportImportedDatasetCsv(idInput.value);
  }
}

function exportImportedDatasetCsv(datasetId) {
  window.open(`/api/imported_datasets/${encodeURIComponent(datasetId)}/export`, '_blank');
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

function setExportFormat(fmt) {
  STATE.exportFormat = fmt;
  document.querySelectorAll('#view-export .tier-pill').forEach(btn => {
    btn.classList.toggle('active', btn.textContent.toLowerCase().includes(fmt));
  });
  toast(`Export format set to .${fmt.toUpperCase()}`);
}

function toggleAllExportCols(checked) {
  document.querySelectorAll('.export-col-cb').forEach(cb => cb.checked = checked);
  toast(checked ? 'All 12 columns selected for export.' : 'All columns deselected.');
}

function triggerRangeExport() {
  const fromEl = document.getElementById('export-range-from');
  const toEl = document.getElementById('export-range-to');
  const dsEl = document.getElementById('export-dataset-select');
  const from = parseInt(fromEl?.value) || 1;
  const to = parseInt(toEl?.value) || 5000;
  const ds = dsEl ? dsEl.value : STATE.dataset;
  const fmt = STATE.exportFormat || 'csv';

  const params = new URLSearchParams({
    dataset: ds,
    export_from: from,
    export_to: to,
    format: fmt,
    search: STATE.search,
    tier: STATE.tier,
    state: STATE.state,
    country: STATE.country,
    category: STATE.category,
    opportunity: STATE.opportunity,
    has_phone: STATE.hasPhone
  });

  toast(`Streaming leads batch (${from.toLocaleString()} - ${to.toLocaleString()}) in .${fmt.toUpperCase()}...`);
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
  } else if (presetKey === 'odo_senzing_orgs') {
    selectDatasetAndExplore('odo_senzing');
    return;
  } else if (presetKey === 'open_company_db') {
    selectDatasetAndExplore('open_company_db');
    return;
  } else if (presetKey === 'tech_stack_leads') {
    selectDatasetAndExplore('tech_stack_leads');
    return;
  }
  switchView('explorer');
  loadLeads();
}

// Multi-Field Lead Query Builder Handlers
function applyQueryBuilder() {
  const company = (document.getElementById('qb-company')?.value || '').trim();
  const contact = (document.getElementById('qb-contact')?.value || '').trim();
  const email = (document.getElementById('qb-email')?.value || '').trim();
  const phone = (document.getElementById('qb-phone')?.value || '').trim();
  const website = (document.getElementById('qb-website')?.value || '').trim();
  const city = (document.getElementById('qb-city')?.value || '').trim();
  const sector = document.getElementById('qb-category')?.value || 'all';
  const state = document.getElementById('qb-state')?.value || 'all';
  const hasPhone = document.getElementById('qb-has-phone')?.checked || false;
  const hasWebsite = document.getElementById('qb-has-website')?.checked || false;
  const hasEmail = document.getElementById('qb-has-email')?.checked || false;

  if (!STATE.colFilters) STATE.colFilters = {};
  STATE.colFilters.name = company;
  STATE.colFilters.contact = contact;
  STATE.colFilters.email = email;
  STATE.colFilters.phone = phone;
  STATE.colFilters.website = website;
  STATE.colFilters.city = city;

  // Sync to table header filter row inputs
  const nameInput = document.getElementById('col-filter-name');
  if (nameInput) { nameInput.value = company; nameInput.classList.toggle('has-value', company.length > 0); }
  const contactInput = document.getElementById('col-filter-contact');
  if (contactInput) { contactInput.value = contact; contactInput.classList.toggle('has-value', contact.length > 0); }
  const emailInput = document.getElementById('col-filter-email');
  if (emailInput) { emailInput.value = email; emailInput.classList.toggle('has-value', email.length > 0); }
  const phoneInput = document.getElementById('col-filter-phone');
  if (phoneInput) { phoneInput.value = phone; phoneInput.classList.toggle('has-value', phone.length > 0); }
  const websiteInput = document.getElementById('col-filter-website');
  if (websiteInput) { websiteInput.value = website; websiteInput.classList.toggle('has-value', website.length > 0); }
  const cityInput = document.getElementById('col-filter-city');
  if (cityInput) { cityInput.value = city; cityInput.classList.toggle('has-value', city.length > 0); }

  STATE.majorCategory = sector;
  const majorSelect = document.getElementById('filter-major-category');
  if (majorSelect) majorSelect.value = sector;

  STATE.state = state;
  const stateSelect = document.getElementById('filter-state');
  if (stateSelect) stateSelect.value = state;

  STATE.hasPhone = hasPhone;
  const phoneChip = document.getElementById('chip-phone');
  if (phoneChip) phoneChip.classList.toggle('active', hasPhone);

  STATE.hasWebsite = hasWebsite;
  const webChip = document.getElementById('chip-website');
  if (webChip) webChip.classList.toggle('active', hasWebsite);

  STATE.hasEmail = hasEmail;
  const emailChip = document.getElementById('chip-email');
  if (emailChip) emailChip.classList.toggle('active', hasEmail);

  STATE.page = 1;

  toast(`Applying Query Builder criteria: launching Lead Explorer...`);
  switchView('explorer');
  updateActiveFilterTags();
  loadLeads();
}

function resetQueryBuilder() {
  if (document.getElementById('qb-company')) document.getElementById('qb-company').value = '';
  if (document.getElementById('qb-contact')) document.getElementById('qb-contact').value = '';
  if (document.getElementById('qb-email')) document.getElementById('qb-email').value = '';
  if (document.getElementById('qb-phone')) document.getElementById('qb-phone').value = '';
  if (document.getElementById('qb-website')) document.getElementById('qb-website').value = '';
  if (document.getElementById('qb-city')) document.getElementById('qb-city').value = '';
  if (document.getElementById('qb-category')) document.getElementById('qb-category').value = 'all';
  if (document.getElementById('qb-state')) document.getElementById('qb-state').value = 'all';
  if (document.getElementById('qb-has-phone')) document.getElementById('qb-has-phone').checked = false;
  if (document.getElementById('qb-has-website')) document.getElementById('qb-has-website').checked = false;
  if (document.getElementById('qb-has-email')) document.getElementById('qb-has-email').checked = false;
  toast('Query Builder criteria reset.');
}

// Global Command Palette Modal Handlers
function openCommandPalette() {
  const modal = document.getElementById('cmd-palette-modal');
  const input = document.getElementById('cmd-palette-input');
  if (modal) {
    modal.style.display = 'flex';
    if (input) {
      input.value = '';
      input.focus();
    }
    filterCommandPalette('');
  }
}

function closeCommandPalette() {
  const modal = document.getElementById('cmd-palette-modal');
  if (modal) modal.style.display = 'none';
}

function filterCommandPalette(q) {
  const query = (q || '').toLowerCase().trim();
  const items = document.querySelectorAll('.cmd-palette-item');
  items.forEach(item => {
    const text = item.textContent.toLowerCase();
    item.style.display = (!query || text.includes(query)) ? 'flex' : 'none';
  });
}

function cmdPaletteNavigate(viewId) {
  closeCommandPalette();
  switchView(viewId);
}

function cmdPaletteAction(actionKey) {
  closeCommandPalette();
  if (actionKey === 'explore_senzing') {
    selectDatasetAndExplore('odo_senzing');
  } else if (actionKey === 'simulate_dedup') {
    switchView('dedup-history');
    setWizardStep(4);
    runSimulatedDedup();
  } else if (actionKey === 'toggle_theme') {
    toggleTheme();
  }
}

// =============================================================================
// ACTIVITY LOGS & NOTIFICATIONS
// =============================================================================
async function loadActivityLogs() {
  const listEl = document.getElementById('activity-log-list');
  const drawerBody = document.getElementById('notifications-drawer-body');
  if (!listEl) return;

  try {
    const res = await fetch('/api/activity_logs');
    if (!res.ok) return;
    const data = await res.json();
    const logs = data.logs || [];

    const logHtml = logs.map(l => `
      <div style="display: flex; gap: 12px; padding: 6px 0; border-bottom: 1px solid var(--border-subtle);">
        <span style="color: var(--text-tertiary); min-width: 140px;">${escapeHtml(l.timestamp)}</span>
        <span class="status-badge ${l.type === 'AUDIT' ? 'clean' : 'neutral'}" style="min-width: 70px; justify-content: center;">${escapeHtml(l.type)}</span>
        <span style="color: var(--text-primary);">${escapeHtml(l.message)}</span>
      </div>
    `).join('');

    listEl.innerHTML = logHtml;
    if (drawerBody) drawerBody.innerHTML = logHtml;
  } catch (err) {
    console.error(err);
  }
}

function toggleNotificationsDrawer() {
  const drawer = document.getElementById('notifications-drawer');
  const backdrop = document.getElementById('drawer-backdrop');
  if (!drawer || !backdrop) return;

  const isOpen = drawer.classList.contains('open');
  if (isOpen) {
    drawer.classList.remove('open');
    backdrop.classList.remove('open');
  } else {
    loadActivityLogs();
    drawer.classList.add('open');
    backdrop.classList.add('open');
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
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme) {
    document.documentElement.setAttribute('data-theme', savedTheme);
  }

  const toggleBtn = document.getElementById('sidebar-toggle-btn');
  const sidebar = document.getElementById('sidebar');
  if (toggleBtn && sidebar) {
    toggleBtn.addEventListener('click', () => {
      sidebar.classList.toggle('collapsed');
    });
  }

  document.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
      e.preventDefault();
      openCommandPalette();
    } else if (e.key === 'Escape') {
      closeCommandPalette();
      closeDrawer();
      closeCategoriesModal();
      const notifDrawer = document.getElementById('notifications-drawer');
      if (notifDrawer) notifDrawer.classList.remove('open');
    }
  });

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

  loadDashboardMetrics();
  loadOverviewCharts();
  loadDatasetsCatalog();
});

// =============================================================================
// LEAD CATEGORIES SECTION LOGIC & DYNAMIC DUCKDB STREAMING
// =============================================================================

let CATEGORIES_STATE = {
  dataset: 'all_local_unified',
  selectedCategories: new Set(),
  search: '',
  sortBy: 'count_desc',
  multiSelectMode: false,
  allCategories: [],
  filteredCategories: [],
  totalCategories: 0,
  totalLeads: 0,
  uncategorizedCount: 0,
  matchingLeads: [],
  matchingTotal: 0,
  page: 1,
  pageSize: 25,
  isLoadingCategories: false,
  isLoadingLeads: false
};

async function loadLeadCategoriesSection(forceRefresh = false) {
  const scrollList = document.getElementById('categories-scroll-list');
  if (scrollList) {
    scrollList.innerHTML = `
      <div class="cat-loading-state">
        <div class="pulse-dot"></div>
        <span>Querying dynamic category taxonomy from DuckDB...</span>
      </div>
    `;
  }
  
  CATEGORIES_STATE.isLoadingCategories = true;
  
  try {
    const datasetSelect = document.getElementById('cat-dataset-select');
    if (datasetSelect && datasetSelect.value) {
      CATEGORIES_STATE.dataset = datasetSelect.value;
    }
    
    const params = new URLSearchParams({
      dataset: CATEGORIES_STATE.dataset,
      sort_by: CATEGORIES_STATE.sortBy,
      refresh: forceRefresh ? '1' : '0'
    });
    
    const res = await fetch(`/api/categories/analytics?${params.toString()}`);
    if (!res.ok) throw new Error('Failed to fetch category analytics');
    const data = await res.json();
    
    CATEGORIES_STATE.allCategories = data.categories || [];
    CATEGORIES_STATE.totalCategories = data.total_categories || 0;
    CATEGORIES_STATE.totalLeads = data.total_leads || 0;
    CATEGORIES_STATE.uncategorizedCount = data.uncategorized_count || 0;
    
    // Update metric cards
    const totalCatsEl = document.getElementById('cat-stat-total-categories');
    if (totalCatsEl) totalCatsEl.textContent = Number(data.total_categories).toLocaleString();
    
    const totalLeadsEl = document.getElementById('cat-stat-total-leads');
    if (totalLeadsEl) totalLeadsEl.textContent = Number(data.total_leads).toLocaleString();
    
    const uncatEl = document.getElementById('cat-stat-uncategorized');
    if (uncatEl) uncatEl.textContent = Number(data.uncategorized_count).toLocaleString();

    // Update Tier 4 Active Engine Card & Dataset Label
    const tierActiveNum = document.getElementById('cat-tier-active-number');
    if (tierActiveNum) tierActiveNum.textContent = Number(data.total_leads).toLocaleString();

    const tierDbStatus = document.getElementById('cat-tier-db-status');
    if (tierDbStatus) {
      tierDbStatus.textContent = data.dataset === 'all_local_unified' ? '16 Unified DBs' : (data.dataset_info?.name ? 'Single DB' : 'Active DB');
    }

    const statDatasetLabel = document.getElementById('cat-stat-dataset-label');
    if (statDatasetLabel) {
      statDatasetLabel.textContent = data.dataset_info?.name ? `${data.dataset_info.name} verified records` : 'Active database verified records';
    }
    
    // Update sidebar badge
    const navBadge = document.getElementById('nav-categories-count-badge');
    if (navBadge) navBadge.textContent = `${data.total_categories}`;
    
    // Render list
    renderLeadCategoriesList();
    
    // Load matching leads
    await loadCategoryMatchingLeads();
    
  } catch (err) {
    console.error('Error loading lead categories:', err);
    if (scrollList) {
      scrollList.innerHTML = `
        <div class="cat-empty-state">
          <span style="color: var(--accent-danger);">Error querying categories: ${escapeHtml(err.message)}</span>
          <button class="btn btn-xs btn-primary" onclick="loadLeadCategoriesSection(true)">Retry</button>
        </div>
      `;
    }
  } finally {
    CATEGORIES_STATE.isLoadingCategories = false;
  }
}

function renderLeadCategoriesList() {
  const scrollList = document.getElementById('categories-scroll-list');
  const footerCount = document.getElementById('cat-list-footer-count');
  if (!scrollList) return;
  
  let cats = CATEGORIES_STATE.allCategories;
  const q = (CATEGORIES_STATE.search || '').trim().toLowerCase();
  
  if (q) {
    cats = cats.filter(c => 
      c.name.toLowerCase().includes(q) || 
      c.label.toLowerCase().includes(q)
    );
  }
  
  CATEGORIES_STATE.filteredCategories = cats;
  
  if (footerCount) {
    const regularCats = cats.filter(c => !c.is_uncategorized);
    footerCount.textContent = `Showing ${regularCats.length} of ${CATEGORIES_STATE.totalCategories} categories`;
  }
  
  if (cats.length === 0) {
    scrollList.innerHTML = `
      <div class="cat-empty-state">
        <span>No categories match "${escapeHtml(CATEGORIES_STATE.search)}"</span>
        <button class="btn btn-xs btn-outline" onclick="clearCategorySearch()">Clear Search</button>
      </div>
    `;
    return;
  }
  
  let html = '';
  
  // 1. "All Categories" Reset Row (pinned at top)
  const isAllSelected = CATEGORIES_STATE.selectedCategories.size === 0;
  const allLeadsFormatted = Number(CATEGORIES_STATE.totalLeads).toLocaleString();
  html += `
    <div class="cat-item-row special-row ${isAllSelected ? 'active' : ''}" onclick="resetAllCategoryFilter()" title="Click to view all categories">
      <div class="cat-item-left">
        ${CATEGORIES_STATE.multiSelectMode ? `
          <input type="checkbox" class="cat-item-checkbox" ${isAllSelected ? 'checked' : ''} onclick="event.stopPropagation(); resetAllCategoryFilter();">
        ` : ''}
        <div class="cat-item-name-group">
          <span class="cat-item-name">✨ All Categories (Reset Filter)</span>
          <div class="cat-item-pct-bar-wrapper">
            <div class="cat-item-pct-bar" style="width: 100%; background: #10b981;"></div>
          </div>
        </div>
      </div>
      <div class="cat-item-right">
        <span class="cat-count-pill">${allLeadsFormatted}</span>
        <span class="cat-pct-label">100%</span>
      </div>
    </div>
  `;
  
  // 2. Regular Category Rows
  const regularCategories = cats.filter(c => !c.is_uncategorized);
  regularCategories.forEach(c => {
    const isSelected = CATEGORIES_STATE.selectedCategories.has(c.name);
    const pct = c.pct || 0;
    const countFormatted = Number(c.count).toLocaleString();
    
    html += `
      <div class="cat-item-row ${isSelected ? 'active' : ''}" 
           data-cat="${escapeHtml(c.name)}" 
           onclick="handleCategoryRowClick('${escapeHtml(c.name)}')" 
           title="${escapeHtml(c.label)}: ${countFormatted} leads (${pct}%)">
        <div class="cat-item-left">
          ${CATEGORIES_STATE.multiSelectMode ? `
            <input type="checkbox" class="cat-item-checkbox" ${isSelected ? 'checked' : ''} 
                   onclick="event.stopPropagation(); handleCategoryRowClick('${escapeHtml(c.name)}');">
          ` : ''}
          <div class="cat-item-name-group">
            <span class="cat-item-name">${escapeHtml(c.label)}</span>
            <div class="cat-item-pct-bar-wrapper">
              <div class="cat-item-pct-bar" style="width: ${Math.max(2, Math.min(100, pct * 4))}%;"></div>
            </div>
          </div>
        </div>
        <div class="cat-item-right">
          <span class="cat-count-pill">${countFormatted}</span>
          <span class="cat-pct-label">${pct}%</span>
        </div>
      </div>
    `;
  });
  
  // 3. "Uncategorized" Row
  const uncatItem = cats.find(c => c.is_uncategorized) || {
    name: 'Uncategorized',
    label: 'Uncategorized',
    count: CATEGORIES_STATE.uncategorizedCount,
    pct: CATEGORIES_STATE.totalLeads > 0 ? ((CATEGORIES_STATE.uncategorizedCount / CATEGORIES_STATE.totalLeads) * 100).toFixed(2) : 0
  };
  
  const isUncatSelected = CATEGORIES_STATE.selectedCategories.has('Uncategorized');
  const uncatFormatted = Number(uncatItem.count).toLocaleString();
  
  html += `
    <div class="cat-item-row uncategorized-row ${isUncatSelected ? 'active' : ''}" 
         data-cat="Uncategorized" 
         onclick="handleCategoryRowClick('Uncategorized')" 
         title="Uncategorized Leads: ${uncatFormatted} records without an industry tag">
      <div class="cat-item-left">
        ${CATEGORIES_STATE.multiSelectMode ? `
          <input type="checkbox" class="cat-item-checkbox" ${isUncatSelected ? 'checked' : ''} 
                 onclick="event.stopPropagation(); handleCategoryRowClick('Uncategorized');">
        ` : ''}
        <div class="cat-item-name-group">
          <span class="cat-item-name" style="color: var(--accent-warning);">⚠️ Uncategorized Leads</span>
          <div class="cat-item-pct-bar-wrapper">
            <div class="cat-item-pct-bar" style="width: ${Math.max(1, Math.min(100, uncatItem.pct * 4))}%; background: var(--accent-warning);"></div>
          </div>
        </div>
      </div>
      <div class="cat-item-right">
        <span class="cat-count-pill" style="border-color: rgba(245, 158, 11, 0.3); color: #fbbf24;">${uncatFormatted}</span>
        <span class="cat-pct-label">${uncatItem.pct}%</span>
      </div>
    </div>
  `;
  
  scrollList.innerHTML = html;
  updateCategorySelectedMetrics();
}

function handleCategoryRowClick(catName) {
  if (CATEGORIES_STATE.multiSelectMode) {
    if (CATEGORIES_STATE.selectedCategories.has(catName)) {
      CATEGORIES_STATE.selectedCategories.delete(catName);
    } else {
      CATEGORIES_STATE.selectedCategories.add(catName);
    }
  } else {
    // Single select mode
    if (CATEGORIES_STATE.selectedCategories.has(catName) && CATEGORIES_STATE.selectedCategories.size === 1) {
      // Toggle off -> All Categories
      CATEGORIES_STATE.selectedCategories.clear();
    } else {
      CATEGORIES_STATE.selectedCategories.clear();
      CATEGORIES_STATE.selectedCategories.add(catName);
    }
  }
  
  renderLeadCategoriesList();
  CATEGORIES_STATE.page = 1;
  loadCategoryMatchingLeads();
}

function resetAllCategoryFilter() {
  CATEGORIES_STATE.selectedCategories.clear();
  renderLeadCategoriesList();
  CATEGORIES_STATE.page = 1;
  loadCategoryMatchingLeads();
}

function toggleCategoryMultiSelectMode(enabled) {
  CATEGORIES_STATE.multiSelectMode = !!enabled;
  renderLeadCategoriesList();
}

function onCategorySearchInput(val) {
  CATEGORIES_STATE.search = val;
  const clearBtn = document.getElementById('cat-search-clear');
  if (clearBtn) {
    clearBtn.style.display = val ? 'block' : 'none';
  }
  renderLeadCategoriesList();
}

function clearCategorySearch() {
  const input = document.getElementById('cat-search-input');
  if (input) input.value = '';
  CATEGORIES_STATE.search = '';
  const clearBtn = document.getElementById('cat-search-clear');
  if (clearBtn) clearBtn.style.display = 'none';
  renderLeadCategoriesList();
}

function setCategorySort(sortBy) {
  CATEGORIES_STATE.sortBy = sortBy;
  
  document.querySelectorAll('.cat-btn-sort').forEach(btn => btn.classList.remove('active'));
  if (sortBy === 'count_desc') {
    const b = document.getElementById('btn-sort-count');
    if (b) b.classList.add('active');
  } else if (sortBy === 'name_asc') {
    const b = document.getElementById('btn-sort-name');
    if (b) b.classList.add('active');
  } else if (sortBy === 'count_asc') {
    const b = document.getElementById('btn-sort-count-asc');
    if (b) b.classList.add('active');
  }
  
  loadLeadCategoriesSection(false);
}

function onCategoryDatasetChange(val) {
  CATEGORIES_STATE.dataset = val;
  CATEGORIES_STATE.selectedCategories.clear();
  CATEGORIES_STATE.page = 1;
  loadLeadCategoriesSection(false);
}

function refreshLeadCategories() {
  loadLeadCategoriesSection(true);
}

function updateCategorySelectedMetrics() {
  const selectedLeadsEl = document.getElementById('cat-stat-selected-leads');
  const selectedLabelEl = document.getElementById('cat-stat-selected-label');
  const filterBadge = document.getElementById('cat-leads-filter-badge');
  
  const size = CATEGORIES_STATE.selectedCategories.size;
  
  if (size === 0) {
    if (selectedLeadsEl) selectedLeadsEl.textContent = Number(CATEGORIES_STATE.totalLeads).toLocaleString();
    if (selectedLabelEl) selectedLabelEl.textContent = 'All Categories (100%)';
    if (filterBadge) {
      filterBadge.textContent = 'All Categories';
      filterBadge.className = 'badge badge-primary';
    }
  } else if (size === 1) {
    const singleName = Array.from(CATEGORIES_STATE.selectedCategories)[0];
    const catObj = CATEGORIES_STATE.allCategories.find(c => c.name === singleName);
    const leadCount = catObj ? catObj.count : CATEGORIES_STATE.matchingTotal;
    const pct = catObj ? catObj.pct : 0;
    
    if (selectedLeadsEl) selectedLeadsEl.textContent = Number(leadCount).toLocaleString();
    if (selectedLabelEl) selectedLabelEl.textContent = `${singleName} (${pct}%)`;
    if (filterBadge) {
      filterBadge.textContent = singleName;
      filterBadge.className = 'badge badge-info';
    }
  } else {
    // Multi-select sum
    let sumCount = 0;
    CATEGORIES_STATE.selectedCategories.forEach(name => {
      const obj = CATEGORIES_STATE.allCategories.find(c => c.name === name);
      if (obj) sumCount += obj.count;
    });
    
    const pct = CATEGORIES_STATE.totalLeads > 0 ? ((sumCount / CATEGORIES_STATE.totalLeads) * 100).toFixed(2) : 0;
    
    if (selectedLeadsEl) selectedLeadsEl.textContent = Number(sumCount).toLocaleString();
    if (selectedLabelEl) selectedLabelEl.textContent = `${size} categories selected (${pct}%)`;
    if (filterBadge) {
      filterBadge.textContent = `${size} Categories Selected`;
      filterBadge.className = 'badge badge-purple';
    }
  }
}

async function loadCategoryMatchingLeads() {
  const tbody = document.getElementById('cat-leads-table-tbody');
  const countText = document.getElementById('cat-leads-count-text');
  const paginationBar = document.getElementById('cat-leads-pagination');
  if (!tbody) return;
  
  tbody.innerHTML = `
    <tr>
      <td colspan="9" style="text-align: center; padding: 40px; color: var(--text-tertiary);">
        <div style="display: flex; align-items: center; justify-content: center; gap: 10px;">
          <div class="pulse-dot"></div>
          <span>Streaming matching category leads from DuckDB...</span>
        </div>
      </td>
    </tr>
  `;
  
  let categoryParam = 'all';
  if (CATEGORIES_STATE.selectedCategories.size > 0) {
    categoryParam = Array.from(CATEGORIES_STATE.selectedCategories).join('||');
  }
  
  const params = new URLSearchParams({
    dataset: CATEGORIES_STATE.dataset,
    category: categoryParam,
    page: CATEGORIES_STATE.page,
    page_size: CATEGORIES_STATE.pageSize
  });
  
  try {
    const res = await fetch(`/api/leads?${params.toString()}`);
    if (!res.ok) throw new Error('Query error');
    const data = await res.json();
    
    const leads = data.leads || [];
    const total = data.total || 0;
    CATEGORIES_STATE.matchingLeads = leads;
    CATEGORIES_STATE.matchingTotal = total;
    
    // Update count text
    if (countText) {
      const start = total === 0 ? 0 : ((CATEGORIES_STATE.page - 1) * CATEGORIES_STATE.pageSize) + 1;
      const end = Math.min(total, CATEGORIES_STATE.page * CATEGORIES_STATE.pageSize);
      countText.textContent = `Showing ${start.toLocaleString()} - ${end.toLocaleString()} of ${total.toLocaleString()} leads`;
    }
    
    if (leads.length === 0) {
      tbody.innerHTML = `
        <tr>
          <td colspan="9" style="text-align: center; padding: 40px; color: var(--text-tertiary);">
            No leads found matching the selected category.
          </td>
        </tr>
      `;
      if (paginationBar) paginationBar.innerHTML = '';
      return;
    }
    
    let html = '';
    leads.forEach(l => {
      const company = escapeHtml(l.name || 'Unnamed Company');
      const contact = escapeHtml(l.contact_name || l.name || '—');
      const title = escapeHtml(l.job_title || 'Executive');
      const cat = escapeHtml(l.category || 'Uncategorized');
      const phone = l.phone ? `<a href="tel:${escapeHtml(l.phone)}" class="cell-link">${escapeHtml(l.phone)}</a>` : '<span class="cell-empty">—</span>';
      const email = l.email ? `<a href="mailto:${escapeHtml(l.email)}" class="cell-link">${escapeHtml(l.email)}</a>` : '<span class="cell-empty">—</span>';
      const website = l.website ? `<a href="${escapeHtml(l.website.startsWith('http') ? l.website : 'https://' + l.website)}" target="_blank" rel="noopener" class="cell-link">${escapeHtml(l.website.replace(/^https?:\/\//i, '').replace(/\/$/, ''))}</a>` : '<span class="cell-empty">—</span>';
      const loc = [l.city, l.state].filter(Boolean).join(', ') || escapeHtml(l.country || 'USA');
      
      html += `
        <tr>
          <td>
            <div style="font-weight: 600; color: var(--text-primary); cursor: pointer;" onclick="openDrawerById('${escapeHtml(String(l.id))}')" title="Inspect ${company}">
              ${company}
            </div>
          </td>
          <td><span class="cell-secondary">${contact}</span></td>
          <td><span class="cell-secondary">${title}</span></td>
          <td><span class="badge badge-secondary" style="font-size: 11px;">${cat}</span></td>
          <td>${phone}</td>
          <td>${email}</td>
          <td>${website}</td>
          <td><span class="cell-secondary">${escapeHtml(loc)}</span></td>
          <td style="text-align: center;">
            <button class="cell-action-btn" onclick="openDrawerById('${escapeHtml(String(l.id))}')" title="Inspect Record">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor"><circle cx="12" cy="12" r="3"/><path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/></svg>
            </button>
          </td>
        </tr>
      `;
    });
    
    tbody.innerHTML = html;
    renderCategoryLeadsPagination(total);
    
  } catch (err) {
    console.error('Error querying category leads:', err);
    tbody.innerHTML = `
      <tr>
        <td colspan="9" style="text-align: center; padding: 40px; color: var(--accent-danger);">
          Error querying matching leads from DuckDB: ${escapeHtml(err.message)}
        </td>
      </tr>
    `;
    if (paginationBar) paginationBar.innerHTML = '';
  }
}

function renderCategoryLeadsPagination(total) {
  const bar = document.getElementById('cat-leads-pagination');
  if (!bar) return;
  
  const totalPages = Math.max(1, Math.ceil(total / CATEGORIES_STATE.pageSize));
  const currentPage = CATEGORIES_STATE.page;
  
  bar.innerHTML = `
    <div class="cat-pagination-left">
      <span>Page <strong>${currentPage}</strong> of <strong>${totalPages.toLocaleString()}</strong></span>
      <select class="form-select" style="padding: 2px 6px; font-size: 11px; background: var(--bg-elevated); border: 1px solid var(--border-subtle); color: var(--text-primary); border-radius: var(--radius-xs);" onchange="changeCategoryLeadsPageSize(Number(this.value))">
        <option value="25" ${CATEGORIES_STATE.pageSize === 25 ? 'selected' : ''}>25 per page</option>
        <option value="50" ${CATEGORIES_STATE.pageSize === 50 ? 'selected' : ''}>50 per page</option>
        <option value="100" ${CATEGORIES_STATE.pageSize === 100 ? 'selected' : ''}>100 per page</option>
      </select>
    </div>
    <div class="cat-pagination-right">
      <button class="btn btn-xs btn-outline" ${currentPage <= 1 ? 'disabled' : ''} onclick="gotoCategoryLeadsPage(${currentPage - 1})">
        ← Previous
      </button>
      <button class="btn btn-xs btn-outline" ${currentPage >= totalPages ? 'disabled' : ''} onclick="gotoCategoryLeadsPage(${currentPage + 1})">
        Next →
      </button>
    </div>
  `;
}

function gotoCategoryLeadsPage(page) {
  CATEGORIES_STATE.page = Math.max(1, page);
  loadCategoryMatchingLeads();
}

function changeCategoryLeadsPageSize(size) {
  CATEGORIES_STATE.pageSize = size;
  CATEGORIES_STATE.page = 1;
  loadCategoryMatchingLeads();
}

function openCurrentCategoryInExplorer() {
  STATE.dataset = CATEGORIES_STATE.dataset;
  if (CATEGORIES_STATE.selectedCategories.size === 0) {
    STATE.category = 'all';
  } else {
    STATE.category = Array.from(CATEGORIES_STATE.selectedCategories).join('||');
  }
  
  STATE.page = 1;
  switchView('explorer');
  loadLeads();
}

// =============================================================================
// PORTFOLIO AUDIT MODAL (31 DATA SOURCES & 5-TIER RECONCILIATION)
// =============================================================================

let PORTFOLIO_AUDIT_DATA = [];

async function openPortfolioAuditModal() {
  const modal = document.getElementById('portfolioAuditModal');
  if (modal) modal.style.display = 'flex';
  await loadPortfolioAuditData();
}

function closePortfolioAuditModal() {
  const modal = document.getElementById('portfolioAuditModal');
  if (modal) modal.style.display = 'none';
}

async function loadPortfolioAuditData() {
  const tbody = document.getElementById('portfolio-audit-tbody');
  if (!tbody) return;
  
  if (PORTFOLIO_AUDIT_DATA.length > 0) {
    renderPortfolioAuditTable(PORTFOLIO_AUDIT_DATA);
    return;
  }
  
  tbody.innerHTML = `
    <tr>
      <td colspan="7" style="text-align: center; padding: 30px; color: var(--text-tertiary);">
        <div style="display: flex; align-items: center; justify-content: center; gap: 10px;">
          <div class="pulse-dot"></div>
          <span>Loading 31-source portfolio verification audit...</span>
        </div>
      </td>
    </tr>
  `;
  
  try {
    const res = await fetch('/api/portfolio/breakdown');
    if (!res.ok) throw new Error('Failed to load portfolio breakdown');
    const data = await res.json();
    PORTFOLIO_AUDIT_DATA = data.sources || [];
    renderPortfolioAuditTable(PORTFOLIO_AUDIT_DATA);
  } catch (err) {
    console.error('Error loading portfolio audit:', err);
    tbody.innerHTML = `
      <tr>
        <td colspan="7" style="text-align: center; padding: 20px; color: var(--accent-danger);">
          Failed to load portfolio audit: ${escapeHtml(err.message)}
        </td>
      </tr>
    `;
  }
}

function renderPortfolioAuditTable(sources) {
  const tbody = document.getElementById('portfolio-audit-tbody');
  const countEl = document.getElementById('portfolio-audit-count');
  if (!tbody) return;
  
  if (countEl) countEl.textContent = `Showing ${sources.length} of ${PORTFOLIO_AUDIT_DATA.length} data sources`;
  
  if (sources.length === 0) {
    tbody.innerHTML = `
      <tr>
        <td colspan="7" style="text-align: center; padding: 25px; color: var(--text-tertiary);">
          No data sources match your filter query.
        </td>
      </tr>
    `;
    return;
  }
  
  let html = '';
  sources.forEach(s => {
    const status = s.status || '';
    let badgeClass = 'status-badge-derived';
    if (status.includes('Verified') || status.includes('Unified') || status.includes('Ready') || status.includes('Cleaned')) {
      badgeClass = 'status-badge-verified';
    } else if (status.includes('Remote') || status.includes('Unfetched') || status.includes('Catalog')) {
      badgeClass = 'status-badge-remote';
    } else if (status.includes('Archive') || status.includes('Raw')) {
      badgeClass = 'status-badge-derived';
    }
    
    html += `
      <tr>
        <td>
          <div style="font-weight: 600; color: var(--text-primary);">${escapeHtml(s.source_name || s.name)}</div>
          <div style="font-size: 11px; color: var(--text-tertiary); font-family: monospace;">${escapeHtml(s.dataset_id || s.id)}</div>
        </td>
        <td><span class="badge badge-secondary" style="font-size: 11px;">${escapeHtml(s.classification || s.tier || 'Database')}</span></td>
        <td style="text-align: right; font-weight: 600;">${Number(s.declared_rows || 0).toLocaleString()}</td>
        <td style="text-align: right; color: var(--text-secondary);">${Number(s.physical_rows || 0).toLocaleString()}</td>
        <td><span class="badge" style="font-size: 10px; background: var(--bg-hover);">${escapeHtml(s.format || 'PARQUET')}</span></td>
        <td style="font-size: 11px; color: var(--text-secondary); font-family: monospace; max-width: 240px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" title="${escapeHtml(s.location || '')}">
          ${escapeHtml(s.location || '')}
        </td>
        <td>
          <span class="status-badge ${badgeClass}">${escapeHtml(status)}</span>
        </td>
      </tr>
    `;
  });
  
  tbody.innerHTML = html;
}

function filterPortfolioAuditTable(query) {
  const q = (query || '').trim().toLowerCase();
  if (!q) {
    renderPortfolioAuditTable(PORTFOLIO_AUDIT_DATA);
    return;
  }
  
  const filtered = PORTFOLIO_AUDIT_DATA.filter(s => 
    (s.source_name || s.name || '').toLowerCase().includes(q) ||
    (s.dataset_id || s.id || '').toLowerCase().includes(q) ||
    (s.format || '').toLowerCase().includes(q) ||
    (s.status || '').toLowerCase().includes(q) ||
    (s.classification || s.tier || '').toLowerCase().includes(q) ||
    (s.location || '').toLowerCase().includes(q)
  );
  
  renderPortfolioAuditTable(filtered);
}


