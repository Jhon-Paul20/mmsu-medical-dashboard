<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>MMSU Health Records · Dashboard</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Figtree:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg:        #0a0f0d;
      --surface:   #111a15;
      --surface2:  #162019;
      --border:    rgba(255,255,255,0.06);
      --border2:   rgba(255,255,255,0.10);
      --green:     #1a7a3c;
      --green-dim: #0f4a24;
      --accent:    #e8c84a;
      --accent2:   #f5dfa0;
      --accent-dim:rgba(232,200,74,0.12);
      --text:      #f0ede8;
      --text-2:    rgba(240,237,232,0.55);
      --text-3:    rgba(240,237,232,0.30);
      --danger:    #e05555;
      --danger-bg: rgba(224,85,85,0.12);
      --safe:      #4ec97a;
      --safe-bg:   rgba(78,201,122,0.12);
      --blue:      #5ba4d4;
      --pink:      #d47eb0;
      --sidebar-w: 256px;
      --radius:    14px;
      --radius-sm: 8px;
    }

    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    html { scroll-behavior: smooth; }

    body {
      font-family: 'Figtree', sans-serif;
      background: var(--bg);
      color: var(--text);
      min-height: 100vh;
      overflow-x: hidden;
    }

    /* ── SIDEBAR ── */
    .sidebar {
      position: fixed;
      left: 0; top: 0; bottom: 0;
      width: var(--sidebar-w);
      background: var(--surface);
      border-right: 1px solid var(--border);
      display: flex;
      flex-direction: column;
      z-index: 100;
      overflow: hidden;
    }

    .sidebar::before {
      content: '';
      position: absolute;
      top: -60px; right: -40px;
      width: 180px; height: 180px;
      background: radial-gradient(circle, rgba(232,200,74,0.07) 0%, transparent 70%);
      pointer-events: none;
    }

    .sidebar-logo {
      padding: 24px 20px 20px;
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      gap: 14px;
      flex-shrink: 0;
    }

    .logo-mark {
      width: 40px; height: 40px;
      background: linear-gradient(135deg, var(--accent), #c9a82e);
      border-radius: 10px;
      display: flex; align-items: center; justify-content: center;
      flex-shrink: 0;
      box-shadow: 0 4px 16px rgba(232,200,74,0.25);
    }
    .logo-mark svg { width: 20px; height: 20px; }

    .logo-info { min-width: 0; }
    .logo-title {
      font-family: 'Instrument Serif', serif;
      font-size: 15px;
      color: var(--text);
      line-height: 1.2;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .logo-sub {
      font-size: 10.5px;
      color: var(--text-3);
      margin-top: 2px;
      letter-spacing: 0.04em;
    }

    .sidebar-nav {
      padding: 16px 12px;
      flex: 1;
      overflow-y: auto;
      overflow-x: hidden;
    }
    .sidebar-nav::-webkit-scrollbar { width: 3px; }
    .sidebar-nav::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 10px; }

    .nav-label {
      font-size: 9.5px;
      font-weight: 600;
      color: var(--text-3);
      text-transform: uppercase;
      letter-spacing: 0.1em;
      padding: 10px 10px 4px;
    }

    .nav-item {
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 9px 12px;
      border-radius: var(--radius-sm);
      border: none;
      background: transparent;
      color: var(--text-2);
      font-size: 13px;
      font-family: 'Figtree', sans-serif;
      font-weight: 400;
      cursor: pointer;
      width: 100%;
      text-align: left;
      margin-bottom: 1px;
      transition: all 0.15s ease;
      position: relative;
    }
    .nav-item:hover { background: var(--border); color: var(--text); }
    .nav-item.active { background: var(--accent-dim); color: var(--accent); font-weight: 500; }
    .nav-item.active::before {
      content: '';
      position: absolute;
      left: 0; top: 25%; bottom: 25%;
      width: 2px;
      background: var(--accent);
      border-radius: 4px;
    }

    .nav-icon {
      width: 18px; height: 18px;
      opacity: 0.8;
      flex-shrink: 0;
    }
    .nav-item.active .nav-icon { opacity: 1; }

    .sidebar-divider {
      height: 1px;
      background: var(--border);
      margin: 12px 10px;
    }

    .cond-search-wrap {
      padding: 4px 4px 8px;
      position: relative;
    }
    .cond-search-wrap svg {
      position: absolute;
      left: 14px; top: 50%;
      transform: translateY(-60%);
      width: 13px; height: 13px;
      color: var(--text-3);
    }
    .cond-search {
      width: 100%;
      padding: 8px 10px 8px 32px;
      background: var(--bg);
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      color: var(--text);
      font-size: 12px;
      font-family: 'Figtree', sans-serif;
      outline: none;
      transition: border-color 0.15s;
    }
    .cond-search::placeholder { color: var(--text-3); }
    .cond-search:focus { border-color: rgba(232,200,74,0.3); }

    .cond-btn {
      display: flex;
      align-items: center;
      justify-content: space-between;
      width: 100%;
      padding: 7px 12px;
      border-radius: 6px;
      border: none;
      background: transparent;
      color: var(--text-2);
      font-size: 12.5px;
      font-family: 'Figtree', sans-serif;
      cursor: pointer;
      transition: all 0.12s;
      text-align: left;
    }
    .cond-btn:hover { background: var(--border); color: var(--text); }
    .cond-btn.active { background: var(--accent-dim); color: var(--accent); font-weight: 500; }
    .cond-dot {
      width: 6px; height: 6px;
      border-radius: 50%;
      background: currentColor;
      opacity: 0.5;
      flex-shrink: 0;
    }
    .cond-btn.active .cond-dot { opacity: 1; }

    .sidebar-footer {
      padding: 16px 20px;
      border-top: 1px solid var(--border);
      flex-shrink: 0;
    }


    /* ── MAIN ── */
    .main {
      margin-left: var(--sidebar-w);
      padding: 32px 36px;
      min-height: 100vh;
    }

    /* Top bar */
    .topbar {
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      margin-bottom: 32px;
    }

    .page-heading {
      font-family: 'Instrument Serif', serif;
      font-size: 30px;
      color: var(--text);
      line-height: 1.1;
    }
    .page-heading em {
      font-style: italic;
      color: var(--accent);
    }
    .page-sub {
      font-size: 13px;
      color: var(--text-2);
      margin-top: 5px;
    }

    .topbar-right {
      display: flex;
      align-items: center;
      gap: 10px;
      padding-top: 4px;
    }

    .status-pill {
      display: flex;
      align-items: center;
      gap: 6px;
      padding: 7px 14px;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 20px;
      font-size: 12px;
      color: var(--text-2);
    }
    .status-dot {
      width: 7px; height: 7px;
      border-radius: 50%;
      background: var(--safe);
      box-shadow: 0 0 8px var(--safe);
      animation: pulse-dot 2s ease-in-out infinite;
    }
    @keyframes pulse-dot {
      0%, 100% { opacity: 1; }
      50% { opacity: 0.4; }
    }

    /* ── KPI CARDS ── */
    .kpi-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 14px;
      margin-bottom: 24px;
    }

    .kpi-card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 20px 22px;
      position: relative;
      overflow: hidden;
      transition: border-color 0.2s, transform 0.2s;
    }
    .kpi-card:hover {
      border-color: var(--border2);
      transform: translateY(-1px);
    }
    .kpi-card::after {
      content: '';
      position: absolute;
      bottom: 0; left: 0; right: 0;
      height: 1px;
      background: linear-gradient(90deg, transparent, var(--accent), transparent);
      opacity: 0.3;
    }
    .kpi-icon {
      width: 34px; height: 34px;
      border-radius: 8px;
      display: flex; align-items: center; justify-content: center;
      margin-bottom: 14px;
      font-size: 16px;
    }
    .kpi-icon.gold { background: var(--accent-dim); }
    .kpi-icon.blue { background: rgba(91,164,212,0.12); }
    .kpi-icon.pink { background: rgba(212,126,176,0.12); }
    .kpi-icon.green { background: rgba(78,201,122,0.12); }

    .kpi-label {
      font-size: 11px;
      font-weight: 500;
      color: var(--text-3);
      text-transform: uppercase;
      letter-spacing: 0.08em;
      margin-bottom: 6px;
    }
    .kpi-value {
      font-family: 'Instrument Serif', serif;
      font-size: 34px;
      color: var(--text);
      line-height: 1;
    }
    .kpi-sub {
      font-size: 11.5px;
      color: var(--text-3);
      margin-top: 5px;
    }

    /* ── MEDICINE PANEL ── */
    .med-panel {
      display: none;
      background: var(--surface2);
      border: 1px solid rgba(232,200,74,0.2);
      border-radius: var(--radius);
      padding: 20px 24px;
      margin-bottom: 24px;
      animation: slideIn 0.25s ease;
    }
    .med-panel.visible { display: block; }
    @keyframes slideIn {
      from { opacity: 0; transform: translateY(-8px); }
      to   { opacity: 1; transform: translateY(0); }
    }
    .med-panel-head {
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 16px;
    }
    .med-panel-title {
      font-size: 12px;
      font-weight: 600;
      color: var(--accent);
      text-transform: uppercase;
      letter-spacing: 0.07em;
    }
    .med-panel-cond {
      font-family: 'Instrument Serif', serif;
      font-size: 16px;
      color: var(--text);
      margin-left: 4px;
    }
    .med-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
      gap: 10px;
    }
    .med-card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 14px 16px;
      transition: border-color 0.15s;
    }
    .med-card:hover { border-color: rgba(232,200,74,0.25); }
    .med-name {
      font-size: 13px;
      font-weight: 600;
      color: var(--text);
      margin-bottom: 4px;
    }
    .med-desc { font-size: 11.5px; color: var(--text-2); line-height: 1.5; }
    .med-warn {
      font-size: 11px;
      color: var(--danger);
      margin-top: 6px;
      display: flex;
      align-items: center;
      gap: 4px;
    }

    /* ── CHARTS ── */
    .charts-grid {
      display: grid;
      grid-template-columns: 1fr 1fr 1fr;
      gap: 14px;
      margin-bottom: 24px;
    }
    .chart-card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 20px;
    }
    .chart-card.wide { grid-column: 1 / 3; }
    .chart-label {
      font-size: 11px;
      font-weight: 600;
      color: var(--text-3);
      text-transform: uppercase;
      letter-spacing: 0.09em;
      margin-bottom: 4px;
    }
    .chart-title-text {
      font-family: 'Instrument Serif', serif;
      font-size: 16px;
      color: var(--text);
      margin-bottom: 18px;
    }
    canvas { max-height: 200px; }

    /* ── TABLE ── */
    .table-wrap {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      overflow: hidden;
    }

    .table-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 18px 22px;
      border-bottom: 1px solid var(--border);
    }
    .table-title-block { }
    .table-title {
      font-size: 11px;
      font-weight: 600;
      color: var(--text-3);
      text-transform: uppercase;
      letter-spacing: 0.09em;
    }
    .table-count {
      font-family: 'Instrument Serif', serif;
      font-size: 17px;
      color: var(--text);
      margin-top: 2px;
    }

    .table-search-wrap {
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .table-search {
      padding: 8px 14px;
      background: var(--bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      color: var(--text);
      font-size: 12.5px;
      font-family: 'Figtree', sans-serif;
      outline: none;
      width: 200px;
      transition: border-color 0.15s;
    }
    .table-search::placeholder { color: var(--text-3); }
    .table-search:focus { border-color: rgba(232,200,74,0.3); }

    .active-filter {
      font-size: 11.5px;
      padding: 5px 12px;
      background: var(--accent-dim);
      color: var(--accent);
      border-radius: 20px;
      font-weight: 500;
    }

    table { width: 100%; border-collapse: collapse; }

    thead tr { border-bottom: 1px solid var(--border); }
    thead th {
      padding: 10px 18px;
      text-align: left;
      font-size: 10.5px;
      font-weight: 600;
      color: var(--text-3);
      text-transform: uppercase;
      letter-spacing: 0.09em;
      white-space: nowrap;
    }

    tbody tr {
      border-bottom: 1px solid var(--border);
      cursor: pointer;
      transition: background 0.12s;
    }
    tbody tr:last-child { border-bottom: none; }
    tbody tr:hover { background: rgba(255,255,255,0.025); }

    tbody td {
      padding: 13px 18px;
      font-size: 13px;
      color: var(--text-2);
    }
    td.name-col { font-weight: 500; color: var(--text); }
    .blood-badge {
      font-size: 11.5px;
      font-weight: 700;
      color: var(--accent);
      background: var(--accent-dim);
      padding: 2px 8px;
      border-radius: 5px;
    }
    .conditions-cell {
      max-width: 220px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      font-size: 12px;
    }
    .risk-tag {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      padding: 3px 10px;
      border-radius: 20px;
      font-size: 11px;
      font-weight: 600;
    }
    .risk-tag.high { background: var(--danger-bg); color: var(--danger); }
    .risk-tag.normal { background: var(--safe-bg); color: var(--safe); }

    /* ── MODAL ── */
    .modal-overlay {
      position: fixed;
      inset: 0;
      background: rgba(0,0,0,0.65);
      backdrop-filter: blur(6px);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 200;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.2s;
    }
    .modal-overlay.open {
      opacity: 1;
      pointer-events: all;
    }
    .modal {
      background: var(--surface);
      border: 1px solid var(--border2);
      border-radius: 18px;
      width: 520px;
      max-width: 90vw;
      max-height: 85vh;
      overflow-y: auto;
      padding: 32px;
      position: relative;
      transform: scale(0.96) translateY(10px);
      transition: transform 0.2s ease;
      box-shadow: 0 32px 80px rgba(0,0,0,0.6);
    }
    .modal-overlay.open .modal {
      transform: scale(1) translateY(0);
    }
    .modal::-webkit-scrollbar { width: 4px; }
    .modal::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 10px; }

    .modal-close {
      position: absolute;
      top: 20px; right: 20px;
      width: 30px; height: 30px;
      background: var(--surface2);
      border: 1px solid var(--border);
      border-radius: 50%;
      cursor: pointer;
      display: flex; align-items: center; justify-content: center;
      color: var(--text-2);
      font-size: 16px;
      transition: all 0.15s;
    }
    .modal-close:hover { background: var(--border); color: var(--text); }

    .modal-avatar {
      width: 56px; height: 56px;
      background: linear-gradient(135deg, var(--green-dim), var(--green));
      border-radius: 16px;
      display: flex; align-items: center; justify-content: center;
      font-family: 'Instrument Serif', serif;
      font-size: 22px;
      color: var(--accent);
      margin-bottom: 14px;
      box-shadow: 0 8px 24px rgba(26,122,60,0.25);
    }
    .modal-name {
      font-family: 'Instrument Serif', serif;
      font-size: 22px;
      color: var(--text);
      margin-bottom: 2px;
    }
    .modal-dept {
      font-size: 12.5px;
      color: var(--text-2);
      margin-bottom: 20px;
    }

    .modal-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
      margin-bottom: 20px;
    }
    .modal-field {
      background: var(--surface2);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 12px 14px;
    }
    .modal-field-label {
      font-size: 10px;
      font-weight: 600;
      color: var(--text-3);
      text-transform: uppercase;
      letter-spacing: 0.09em;
      margin-bottom: 4px;
    }
    .modal-field-val {
      font-size: 14px;
      font-weight: 600;
      color: var(--text);
    }

    .modal-section-title {
      font-size: 10.5px;
      font-weight: 600;
      color: var(--text-3);
      text-transform: uppercase;
      letter-spacing: 0.09em;
      margin-bottom: 10px;
    }

    .pills-wrap { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 20px; }
    .pill {
      padding: 4px 12px;
      border-radius: 20px;
      font-size: 12px;
      font-weight: 500;
      background: var(--surface2);
      border: 1px solid var(--border);
      color: var(--text-2);
    }
    .pill.high {
      background: var(--danger-bg);
      border-color: rgba(224,85,85,0.2);
      color: var(--danger);
    }

    .modal-meds-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
    }
    .modal-med-card {
      background: var(--surface2);
      border: 1px solid var(--border);
      border-radius: 9px;
      padding: 12px 14px;
    }
    .modal-med-cond-label {
      font-size: 9.5px;
      font-weight: 600;
      color: var(--accent);
      text-transform: uppercase;
      letter-spacing: 0.08em;
      margin-bottom: 6px;
    }
    .modal-med-name {
      font-size: 12.5px;
      font-weight: 600;
      color: var(--text);
      margin-bottom: 3px;
    }
    .modal-med-desc { font-size: 11px; color: var(--text-2); }

    /* ── EMPTY STATE ── */
    .empty-state {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 60px 24px;
      gap: 10px;
    }
    .empty-icon {
      width: 52px; height: 52px;
      background: var(--surface2);
      border: 1px solid var(--border);
      border-radius: 14px;
      display: flex; align-items: center; justify-content: center;
      margin-bottom: 4px;
    }
    .empty-title {
      font-family: 'Instrument Serif', serif;
      font-size: 17px;
      color: var(--text-2);
    }
    .empty-sub { font-size: 12.5px; color: var(--text-3); }

    /* ── TOAST ── */
    .toast {
      position: fixed;
      bottom: 24px; right: 24px;
      background: var(--surface);
      border: 1px solid var(--border2);
      border-radius: 10px;
      padding: 12px 18px;
      font-size: 13px;
      color: var(--text);
      box-shadow: 0 8px 32px rgba(0,0,0,0.4);
      transform: translateY(80px);
      opacity: 0;
      transition: all 0.3s ease;
      z-index: 300;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .toast.show { transform: translateY(0); opacity: 1; }
    .toast-dot { width: 8px; height: 8px; border-radius: 50%; background: var(--safe); }

    /* ── SCROLLBAR ── */
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 10px; }

    /* ── ENTRY ANIM ── */
    .fade-in {
      opacity: 0;
      animation: fadeUp 0.4s ease forwards;
    }
    @keyframes fadeUp {
      from { opacity: 0; transform: translateY(12px); }
      to   { opacity: 1; transform: translateY(0); }
    }
    .kpi-card:nth-child(1) { animation-delay: 0.05s; }
    .kpi-card:nth-child(2) { animation-delay: 0.1s; }
    .kpi-card:nth-child(3) { animation-delay: 0.15s; }
    .kpi-card:nth-child(4) { animation-delay: 0.2s; }
  </style>
</head>
<body>

<!-- ── SIDEBAR ── -->
<aside class="sidebar">
  <div class="sidebar-logo">
    <div class="logo-mark">
      <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M10 2v16M2 10h16" stroke="#0a0f0d" stroke-width="2.5" stroke-linecap="round"/>
      </svg>
    </div>
    <div class="logo-info">
      <div class="logo-title">MMSU Medical</div>
      <div class="logo-sub">Health Records System</div>
    </div>
  </div>

  <nav class="sidebar-nav">
    <div class="nav-label">Main</div>
    <button class="nav-item active" onclick="window.scrollTo({top:0,behavior:'smooth'})">
      <svg class="nav-icon" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.5">
        <rect x="2" y="2" width="7" height="7" rx="2"/><rect x="11" y="2" width="7" height="7" rx="2"/>
        <rect x="2" y="11" width="7" height="7" rx="2"/><rect x="11" y="11" width="7" height="7" rx="2"/>
      </svg>
      Overview
    </button>
    <button class="nav-item" onclick="document.querySelector('.table-wrap').scrollIntoView({behavior:'smooth'})">
      <svg class="nav-icon" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.5">
        <path d="M2 5h16M2 10h16M2 15h16"/>
      </svg>
      Personnel List
    </button>
    <button class="nav-item" onclick="document.querySelector('.charts-grid').scrollIntoView({behavior:'smooth'})">
      <svg class="nav-icon" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.5">
        <path d="M2 16V8l4-3 4 4 4-6 4 2v11H2z"/>
      </svg>
      Analytics
    </button>

    <div class="sidebar-divider"></div>
    <div class="nav-label">Filter by Condition</div>

    <div class="cond-search-wrap">
      <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5">
        <circle cx="6.5" cy="6.5" r="4"/><path d="M10 10l3.5 3.5"/>
      </svg>
      <input class="cond-search" type="text" id="conditionSearch" placeholder="Search condition…" oninput="searchCondition()">
    </div>
    <div id="conditionList"></div>
  </nav>

  <div class="sidebar-footer">
    <div style="font-size:12px;color:var(--text-3);margin-bottom:10px;padding:0 2px;">
      Logged in as <span style="color:var(--accent);font-weight:500;" id="loggedInUser">admin</span>
    </div>
    <button onclick="handleLogout()" style="width:100%;display:flex;align-items:center;gap:8px;padding:8px 12px;border-radius:var(--radius-sm);border:1px solid var(--border);background:transparent;color:var(--text-2);font-size:12.5px;font-family:'Figtree',sans-serif;cursor:pointer;transition:all 0.15s;" onmouseover="this.style.background='var(--danger-bg)';this.style.color='var(--danger)';this.style.borderColor='rgba(224,85,85,0.25)'" onmouseout="this.style.background='transparent';this.style.color='var(--text-2)';this.style.borderColor='var(--border)'">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" style="flex-shrink:0">
        <path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4M16 17l5-5-5-5M21 12H9"/>
      </svg>
      Sign Out
    </button>
  </div>

</aside>

<!-- ── MAIN ── -->
<main class="main">

  <div class="topbar">
    <div>
      <div class="page-heading">Personnel <em>Health Records</em></div>
      <div class="page-sub" id="activeFilterLabel">All personnel — records loaded</div>
    </div>
    <div class="topbar-right">
      <div class="status-pill">
        <div class="status-dot"></div>
        System Active
      </div>
    </div>
  </div>

  <!-- KPI Cards -->
  <div class="kpi-grid">
    <div class="kpi-card fade-in">
      <div class="kpi-icon gold">👥</div>
      <div class="kpi-label">Total Personnel</div>
      <div class="kpi-value" id="totalRecords">—</div>
      <div class="kpi-sub">Active records</div>
    </div>
    <div class="kpi-card fade-in">
      <div class="kpi-icon blue">🩸</div>
      <div class="kpi-label">Common Blood Type</div>
      <div class="kpi-value" id="commonBloodType">—</div>
      <div class="kpi-sub">Most frequent type</div>
    </div>
    <div class="kpi-card fade-in">
      <div class="kpi-icon blue">♂</div>
      <div class="kpi-label">Male</div>
      <div class="kpi-value" id="malePercent">—</div>
      <div class="kpi-sub">Of total personnel</div>
    </div>
    <div class="kpi-card fade-in">
      <div class="kpi-icon pink">♀</div>
      <div class="kpi-label">Female</div>
      <div class="kpi-value" id="femalePercent">—</div>
      <div class="kpi-sub">Of total personnel</div>
    </div>
  </div>

  <!-- Medicine Panel -->
  <div class="med-panel" id="medPanel">
    <div class="med-panel-head">
      <svg width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="#e8c84a" stroke-width="1.5">
        <path d="M8 2v12M2 8h12"/>
      </svg>
      <div class="med-panel-title">Treatment Suggestions —</div>
      <div class="med-panel-cond" id="medPanelCondition"></div>
    </div>
    <div class="med-grid" id="medGrid"></div>
  </div>

  <!-- Charts -->
  <div class="charts-grid">
    <div class="chart-card wide">
      <div class="chart-label">Distribution</div>
      <div class="chart-title-text">Blood Type Frequency</div>
      <canvas id="bloodTypeChart"></canvas>
    </div>
    <div class="chart-card">
      <div class="chart-label">Demographics</div>
      <div class="chart-title-text">Gender Split</div>
      <canvas id="genderChart"></canvas>
    </div>
    <div class="chart-card wide">
      <div class="chart-label">Breakdown</div>
      <div class="chart-title-text">Personnel by Department</div>
      <canvas id="deptChart"></canvas>
    </div>
    <div class="chart-card">
      <div class="chart-label">Risk</div>
      <div class="chart-title-text">High Risk Rate</div>
      <canvas id="riskChart"></canvas>
    </div>
  </div>

  <!-- Personnel Table -->
  <div class="table-wrap">
    <div class="table-header">
      <div class="table-title-block">
        <div class="table-title">Personnel Records</div>
        <div class="table-count" id="tableCountLabel">No data loaded</div>
      </div>
      <div class="table-search-wrap">
        <span class="active-filter" id="filterBadge">All</span>
        <input type="text" class="table-search" placeholder="Search name…" oninput="searchTable(this.value)" id="tableSearch">
      </div>
    </div>
    <table>
      <thead>
        <tr>
          <th>Name</th>
          <th>Gender</th>
          <th>Blood</th>
          <th>Department</th>
          <th>Conditions</th>
          <th>Risk</th>
        </tr>
      </thead>
      <tbody id="personnelTable">
        <tr>
          <td colspan="6">
            <div class="empty-state">
              <div class="empty-icon">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="rgba(240,237,232,0.3)" stroke-width="1.5">
                  <path d="M9 12h6M9 16h6M17 3H7a2 2 0 00-2 2v14a2 2 0 002 2h10a2 2 0 002-2V5a2 2 0 00-2-2z"/>
                </svg>
              </div>
              <div class="empty-title">No records loaded</div>
              <div class="empty-sub">No records found for the selected filter</div>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>

</main>

<!-- ── MODAL ── -->
<div class="modal-overlay" id="modalOverlay" onclick="closeModal(event)">
  <div class="modal">
    <button class="modal-close" onclick="closeModalDirect()">✕</button>
    <div class="modal-avatar" id="modalAvatar">?</div>
    <div class="modal-name" id="modalName"></div>
    <div class="modal-dept" id="modalDept"></div>

    <div class="modal-grid">
      <div class="modal-field">
        <div class="modal-field-label">Gender</div>
        <div class="modal-field-val" id="modalGender"></div>
      </div>
      <div class="modal-field">
        <div class="modal-field-label">Blood Type</div>
        <div class="modal-field-val" style="color:var(--accent)" id="modalBlood"></div>
      </div>
    </div>

    <div class="modal-section-title">Recorded Conditions</div>
    <div class="pills-wrap" id="modalConditions"></div>

    <div id="modalMedsSection">
      <div class="modal-section-title" id="modalMedsTitle" style="display:none;">Treatment Suggestions</div>
      <div class="modal-meds-grid" id="modalMeds"></div>
    </div>
  </div>
</div>

<!-- ── UPLOAD CONFIRM MODAL ── -->
<div class="modal-overlay" id="uploadConfirmOverlay" style="z-index:250;">
  <div class="modal" style="max-width:400px;text-align:center;">
    <div style="font-size:32px;margin-bottom:12px;">⚠️</div>
    <div class="modal-name" style="font-size:18px;margin-bottom:8px;">Replace all records?</div>
    <div style="font-size:13px;color:var(--text-2);margin-bottom:24px;line-height:1.6;">
      Uploading a CSV will <strong style="color:var(--danger);">permanently delete</strong> all existing personnel records and replace them with the file contents. This cannot be undone.
    </div>
    <div style="display:flex;gap:10px;justify-content:center;">
      <button onclick="cancelUpload()" style="padding:9px 20px;border-radius:8px;border:1px solid var(--border2);background:transparent;color:var(--text-2);font-family:'Figtree',sans-serif;font-size:13px;cursor:pointer;">Cancel</button>
      <button onclick="confirmUpload()" style="padding:9px 20px;border-radius:8px;border:none;background:var(--danger);color:#fff;font-family:'Figtree',sans-serif;font-size:13px;font-weight:600;cursor:pointer;">Yes, Replace All</button>
    </div>
  </div>
</div>

<!-- ── TOAST ── -->
<div class="toast" id="toast">
  <div class="toast-dot"></div>
  <span id="toastMsg"></span>
</div>

<script>
  let allData = [];
  let filteredData = [];
  let activeCondition = 'All';
  let bloodChart, genderChart, deptChart, riskChart;
  let csrfToken = '';

  async function fetchCsrfToken() {
    try {
      const res = await fetch('/csrf-token');
      if (res.status === 401) { window.location.href = '/login'; return; }
      const data = await res.json();
      csrfToken = data.token;
    } catch(e) { console.error('Failed to fetch CSRF token', e); }
  }

  async function handleLogout() {
    if (!confirm('Sign out of MMSU Medical Dashboard?')) return;
    await fetch('/logout', {
      method: 'POST',
      headers: { 'X-CSRF-Token': csrfToken, 'Content-Type': 'application/json' }
    });
    window.location.href = '/login';
  }
  let pendingUploadFile = null;

  function requestUpload(file) {
    pendingUploadFile = file;
    document.getElementById('uploadConfirmOverlay').classList.add('open');
  }

  function cancelUpload() {
    pendingUploadFile = null;
    document.getElementById('uploadConfirmOverlay').classList.remove('open');
  }

  async function confirmUpload() {
    document.getElementById('uploadConfirmOverlay').classList.remove('open');
    if (!pendingUploadFile) return;
    const formData = new FormData();
    formData.append('file', pendingUploadFile);
    pendingUploadFile = null;
    try {
      const res = await fetch('/upload', {
        method: 'POST',
        headers: { 'X-CSRF-Token': csrfToken },
        body: formData
      });
      const data = await res.json();
      showToast(data.message || data.error || 'Upload complete');
      const fresh = await fetch('/personnel');
      allData = await fresh.json();
      filterData('All');
    } catch (e) {
      showToast('Upload failed. Please try again.');
    }
  }

  const HIGH_RISK = ['Cancer','Heart Disease','HIV/AIDS','Tuberculosis','Stroke','Kidney Disease','Liver Disease','Pneumonia','Epilepsy','Lupus'];

  const MEDICINES = {
    'Hypertension': [
      { name: 'Amlodipine', desc: 'Calcium channel blocker for blood pressure control.', warn: '' },
      { name: 'Losartan', desc: 'ARB for hypertension and kidney protection.', warn: '' },
      { name: 'Hydrochlorothiazide', desc: 'Diuretic for mild hypertension.', warn: '' }
    ],
    'Diabetes': [
      { name: 'Metformin', desc: 'First-line oral medication for type 2 diabetes.', warn: '' },
      { name: 'Glimepiride', desc: 'Sulfonylurea stimulating insulin secretion.', warn: '' },
      { name: 'Insulin', desc: 'Required for type 1 or advanced type 2.', warn: 'Requires monitoring.' }
    ],
    'Asthma': [
      { name: 'Salbutamol Inhaler', desc: 'Short-acting bronchodilator for acute attacks.', warn: '' },
      { name: 'Budesonide Inhaler', desc: 'Inhaled corticosteroid for long-term control.', warn: '' }
    ],
    'Heart Disease': [
      { name: 'Aspirin', desc: 'Antiplatelet therapy for clot prevention.', warn: '' },
      { name: 'Atorvastatin', desc: 'Reduces LDL cholesterol and inflammation.', warn: '' },
      { name: 'Bisoprolol', desc: 'Beta-blocker to reduce heart rate and workload.', warn: 'Specialist required.' }
    ],
    'Allergies': [
      { name: 'Cetirizine', desc: 'Non-drowsy antihistamine for daily use.', warn: '' },
      { name: 'Loratadine', desc: 'Long-acting antihistamine tablet.', warn: '' }
    ],
    'Obesity': [
      { name: 'Orlistat', desc: 'Lipase inhibitor reducing dietary fat absorption.', warn: '' },
      { name: 'Diet & Exercise', desc: 'Primary intervention for weight management.', warn: '' }
    ],
    'Tuberculosis': [
      { name: 'Rifampicin', desc: 'Key antibiotic in TB regimen.', warn: 'DOT required.' },
      { name: 'Isoniazid', desc: 'Bactericidal agent against TB.', warn: 'Monitor liver function.' }
    ],
    'Anemia': [
      { name: 'Ferrous Sulfate', desc: 'Iron supplementation for iron-deficiency anemia.', warn: '' },
      { name: 'Folic Acid', desc: 'Supports red blood cell production.', warn: '' }
    ],
    'Cancer': [
      { name: 'Chemotherapy', desc: 'Cytotoxic drug therapy for cancer.', warn: 'Specialist required.' },
      { name: 'Palliative Care', desc: 'Supportive care to improve quality of life.', warn: '' }
    ],
    'Arthritis': [
      { name: 'Naproxen', desc: 'NSAID for joint pain and inflammation.', warn: '' },
      { name: 'Methotrexate', desc: 'DMARD for rheumatoid arthritis.', warn: 'Specialist required.' }
    ],
    'Mental Health': [
      { name: 'Sertraline', desc: 'SSRI antidepressant for anxiety and depression.', warn: '' },
      { name: 'Counseling', desc: 'Cognitive behavioral therapy recommended.', warn: '' }
    ],
    'Liver Disease': [
      { name: 'Silymarin', desc: 'Hepatoprotective agent from milk thistle.', warn: '' },
      { name: 'Ursodeoxycholic Acid', desc: 'Bile acid for cholestatic liver disease.', warn: 'Specialist required.' }
    ],
    'Kidney Disease': [
      { name: 'Amlodipine', desc: 'Controls BP to protect kidney function.', warn: '' },
      { name: 'Erythropoietin', desc: 'For anemia in chronic kidney disease.', warn: 'Specialist required.' }
    ],
    'Migraine': [
      { name: 'Sumatriptan', desc: 'Triptan for acute migraine attacks.', warn: '' },
      { name: 'Topiramate', desc: 'Preventive therapy for frequent migraines.', warn: '' }
    ],
    'Ulcer': [
      { name: 'Omeprazole', desc: 'Proton pump inhibitor reducing stomach acid.', warn: '' },
      { name: 'Amoxicillin', desc: 'Antibiotic for H. pylori eradication.', warn: '' }
    ],
    'Gastritis': [
      { name: 'Pantoprazole', desc: 'PPI for gastric acid reduction.', warn: '' },
      { name: 'Antacids', desc: 'Quick relief from gastric discomfort.', warn: '' }
    ],
    'Hepatitis': [
      { name: 'Tenofovir', desc: 'Antiviral for hepatitis B.', warn: 'Specialist required.' },
      { name: 'Sofosbuvir', desc: 'Direct-acting antiviral for hepatitis C.', warn: 'Specialist required.' }
    ],
    'Thyroid Disorder': [
      { name: 'Levothyroxine', desc: 'Synthetic T4 for hypothyroidism.', warn: '' },
      { name: 'Methimazole', desc: 'Antithyroid drug for hyperthyroidism.', warn: '' }
    ],
    'Pneumonia': [
      { name: 'Amoxicillin-Clavulanate', desc: 'Broad-spectrum antibiotic for community pneumonia.', warn: '' },
      { name: 'Azithromycin', desc: 'Macrolide antibiotic for atypical pneumonia.', warn: '' }
    ],
    'HIV/AIDS': [
      { name: 'Tenofovir/Lamivudine', desc: 'NRTI backbone of antiretroviral therapy.', warn: 'Specialist required.' },
      { name: 'Dolutegravir', desc: 'Integrase inhibitor for ART regimen.', warn: 'Specialist required.' }
    ],
    'Dengue': [
      { name: 'Paracetamol', desc: 'Fever and pain management.', warn: 'Avoid aspirin/NSAIDs.' },
      { name: 'IV Fluids', desc: 'Hydration support in severe cases.', warn: '' }
    ],
    'Stroke': [
      { name: 'Aspirin', desc: 'Antiplatelet therapy post-ischemic stroke.', warn: '' },
      { name: 'Clopidogrel', desc: 'Alternative antiplatelet for stroke prevention.', warn: 'Specialist required.' }
    ],
    'Bronchitis': [
      { name: 'Salbutamol', desc: 'Bronchodilator for airway relief.', warn: '' },
      { name: 'Amoxicillin', desc: 'Antibiotic if bacterial cause suspected.', warn: '' }
    ],
    'Epilepsy': [
      { name: 'Valproic Acid', desc: 'Broad-spectrum anticonvulsant.', warn: 'Monitor liver function.' },
      { name: 'Carbamazepine', desc: 'Anticonvulsant for focal seizures.', warn: '' }
    ],
    'Glaucoma': [
      { name: 'Timolol Eye Drops', desc: 'Beta-blocker reducing intraocular pressure.', warn: '' },
      { name: 'Latanoprost Eye Drops', desc: 'Prostaglandin analogue for IOP.', warn: '' }
    ],
    'Cyst': [
      { name: 'Observation', desc: 'Many cysts resolve on their own.', warn: '' },
      { name: 'Surgical Referral', desc: 'For large or symptomatic cysts.', warn: '' }
    ],
    'Covid-19': [
      { name: 'Paracetamol', desc: 'Fever and pain management.', warn: '' },
      { name: 'Paxlovid', desc: 'Antiviral for high-risk patients.', warn: 'Specialist assessment required.' }
    ],
    'Sinusitis': [
      { name: 'Amoxicillin', desc: 'Antibiotic for bacterial sinusitis.', warn: '' },
      { name: 'Nasal Saline Rinse', desc: 'Decongestant irrigation therapy.', warn: '' }
    ],
    'Gout': [
      { name: 'Allopurinol', desc: 'Reduces uric acid production.', warn: '' },
      { name: 'Colchicine', desc: 'Anti-inflammatory for acute gout attacks.', warn: '' }
    ],
    'GERD': [
      { name: 'Omeprazole', desc: 'Proton pump inhibitor for GERD.', warn: '' },
      { name: 'Domperidone', desc: 'Prokinetic agent for reflux symptoms.', warn: '' }
    ]
  };

  const allConditionsList = ['Hypertension','Diabetes','Asthma','Heart Disease','Allergies','Obesity','Tuberculosis','Anemia','Cancer','Arthritis','Covid-19','Mental Health','Liver Disease','Kidney Disease','Migraine','Ulcer','Gastritis','Hepatitis','Thyroid Disorder','Pneumonia','HIV/AIDS','Dengue','Stroke','Bronchitis','Epilepsy','Glaucoma','Cyst','Scoliosis','Gallstones','Varicose Veins','Sinusitis','Tonsillitis','Lupus','GERD','Psoriasis','Vertigo','Gout','Hernia'];

  function isHighRisk(conditions) {
    return conditions.some(c => HIGH_RISK.includes(c));
  }

  function showToast(msg) {
    const t = document.getElementById('toast');
    document.getElementById('toastMsg').textContent = msg;
    t.classList.add('show');
    setTimeout(() => t.classList.remove('show'), 3000);
  }

  function renderTable(data) {
    const tbody = document.getElementById("personnelTable");
    document.getElementById("tableCountLabel").textContent = data.length
      ? `${data.length} record${data.length === 1 ? '' : 's'} found`
      : 'No results';

    if (data.length === 0) {
      tbody.innerHTML = `<tr><td colspan="6"><div class="empty-state">
        <div class="empty-icon">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="rgba(240,237,232,0.3)" stroke-width="1.5">
            <circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/>
          </svg>
        </div>
        <div class="empty-title">No matching records</div>
        <div class="empty-sub">Try adjusting your search or filter</div>
      </div></td></tr>`;
      return;
    }
    tbody.innerHTML = data.map(p => {
      const risk = isHighRisk(p.conditions);
      const initials = p.name.split(' ').map(w => w[0]).join('').slice(0,2).toUpperCase();
      return `<tr onclick="openModal(${JSON.stringify(p).replace(/"/g,'&quot;')})">
        <td class="name-col">${p.name}</td>
        <td>${p.gender}</td>
        <td><span class="blood-badge">${p.blood || '—'}</span></td>
        <td>${p.department}</td>
        <td class="conditions-cell">${p.conditions.join(', ') || '—'}</td>
        <td>${risk
          ? '<span class="risk-tag high">⚠ High Risk</span>'
          : '<span class="risk-tag normal">✓ Normal</span>'}</td>
      </tr>`;
    }).join('');
  }

  function processData(data) {
    const total = data.length;
    const bloodFreq = {};
    const genderFreq = { Male: 0, Female: 0 };
    const deptFreq = {};
    let highRiskCount = 0;

    data.forEach(p => {
      if (p.blood) bloodFreq[p.blood] = (bloodFreq[p.blood] || 0) + 1;
      if (p.gender === 'Male' || p.gender === 'Female') genderFreq[p.gender]++;
      if (p.department) deptFreq[p.department] = (deptFreq[p.department] || 0) + 1;
      if (isHighRisk(p.conditions)) highRiskCount++;
    });

    const mostCommonBlood = total > 0 && Object.keys(bloodFreq).length
      ? Object.entries(bloodFreq).reduce((a, b) => b[1] > a[1] ? b : a)[0]
      : '—';
    const malePercent = total > 0 ? ((genderFreq.Male / total) * 100).toFixed(1) + '%' : '—';
    const femalePercent = total > 0 ? ((genderFreq.Female / total) * 100).toFixed(1) + '%' : '—';

    document.getElementById("totalRecords").textContent = total || '—';
    document.getElementById("commonBloodType").textContent = mostCommonBlood;
    document.getElementById("malePercent").textContent = malePercent;
    document.getElementById("femalePercent").textContent = femalePercent;

    if (bloodChart) bloodChart.destroy();
    if (genderChart) genderChart.destroy();
    if (deptChart) deptChart.destroy();
    if (riskChart) riskChart.destroy();

    const chartFont = { family: 'Figtree', size: 11 };
    const tickColor = 'rgba(240,237,232,0.4)';
    const gridColor = 'rgba(255,255,255,0.04)';

    bloodChart = new Chart(document.getElementById("bloodTypeChart"), {
      type: 'bar',
      data: {
        labels: Object.keys(bloodFreq),
        datasets: [{
          label: 'Count',
          data: Object.values(bloodFreq),
          backgroundColor: 'rgba(232,200,74,0.75)',
          borderColor: 'rgba(232,200,74,1)',
          borderWidth: 1,
          borderRadius: 5,
          hoverBackgroundColor: 'rgba(232,200,74,0.95)'
        }]
      },
      options: {
        plugins: { legend: { display: false }, tooltip: { backgroundColor: '#162019', titleColor: '#f0ede8', bodyColor: 'rgba(240,237,232,0.7)', borderColor: 'rgba(255,255,255,0.08)', borderWidth: 1 } },
        scales: {
          x: { ticks: { color: tickColor, font: chartFont }, grid: { color: gridColor } },
          y: { ticks: { color: tickColor, font: chartFont }, grid: { color: gridColor } }
        }
      }
    });

    genderChart = new Chart(document.getElementById("genderChart"), {
      type: 'doughnut',
      data: {
        labels: ['Male', 'Female'],
        datasets: [{
          data: [genderFreq.Male, genderFreq.Female],
          backgroundColor: ['rgba(91,164,212,0.85)', 'rgba(212,126,176,0.85)'],
          borderColor: ['#111a15','#111a15'],
          borderWidth: 3,
          hoverOffset: 4
        }]
      },
      options: {
        plugins: {
          legend: { labels: { color: tickColor, font: chartFont, boxWidth: 10, padding: 16 } },
          tooltip: { backgroundColor: '#162019', titleColor: '#f0ede8', bodyColor: 'rgba(240,237,232,0.7)' }
        },
        cutout: '68%'
      }
    });

    const deptColors = {
      CHS: 'rgba(232,200,74,0.8)', COE: 'rgba(91,164,212,0.8)',
      CBEA: 'rgba(212,126,176,0.8)', CAS: 'rgba(78,201,122,0.8)',
      CTE: 'rgba(255,165,80,0.8)'
    };
    const depts = Object.keys(deptFreq);
    deptChart = new Chart(document.getElementById("deptChart"), {
      type: 'bar',
      data: {
        labels: depts,
        datasets: [{
          label: 'Personnel',
          data: Object.values(deptFreq),
          backgroundColor: depts.map(d => deptColors[d] || 'rgba(120,120,180,0.7)'),
          borderRadius: 5
        }]
      },
      options: {
        plugins: { legend: { display: false }, tooltip: { backgroundColor: '#162019', titleColor: '#f0ede8', bodyColor: 'rgba(240,237,232,0.7)' } },
        scales: {
          x: { ticks: { color: tickColor, font: chartFont }, grid: { color: gridColor } },
          y: { ticks: { color: tickColor, font: chartFont }, grid: { color: gridColor } }
        }
      }
    });

    riskChart = new Chart(document.getElementById("riskChart"), {
      type: 'doughnut',
      data: {
        labels: ['High Risk', 'Normal'],
        datasets: [{
          data: [highRiskCount, total - highRiskCount],
          backgroundColor: ['rgba(224,85,85,0.8)', 'rgba(78,201,122,0.8)'],
          borderColor: ['#111a15','#111a15'],
          borderWidth: 3,
          hoverOffset: 4
        }]
      },
      options: {
        plugins: {
          legend: { labels: { color: tickColor, font: chartFont, boxWidth: 10, padding: 16 } },
          tooltip: { backgroundColor: '#162019', titleColor: '#f0ede8', bodyColor: 'rgba(240,237,232,0.7)' }
        },
        cutout: '68%'
      }
    });

    renderTable(data);
  }

  function filterData(condition) {
    activeCondition = condition;
    document.getElementById('filterBadge').textContent = condition;
    document.getElementById('activeFilterLabel').textContent =
      condition === 'All'
        ? `All personnel — ${allData.length} record${allData.length === 1 ? '' : 's'}`
        : `Filtered by: ${condition}`;
    document.getElementById('tableSearch').value = '';

    document.querySelectorAll('.cond-btn').forEach(b =>
      b.classList.toggle('active', b.dataset.cond === condition));

    filteredData = condition === 'All' ? allData : allData.filter(p => p.conditions.includes(condition));
    processData(filteredData);

    const panel = document.getElementById('medPanel');
    if (condition !== 'All' && MEDICINES[condition]) {
      document.getElementById('medPanelCondition').textContent = condition;
      document.getElementById('medGrid').innerHTML = MEDICINES[condition].map(m =>
        `<div class="med-card">
          <div class="med-name">${m.name}</div>
          <div class="med-desc">${m.desc}</div>
          ${m.warn ? `<div class="med-warn">⚠ ${m.warn}</div>` : ''}
        </div>`).join('');
      panel.classList.add('visible');
    } else {
      panel.classList.remove('visible');
    }
  }

  function searchTable(query) {
    const q = query.toLowerCase();
    const base = activeCondition === 'All' ? allData : allData.filter(p => p.conditions.includes(activeCondition));
    const results = q ? base.filter(p => p.name.toLowerCase().includes(q) || p.department.toLowerCase().includes(q)) : base;
    renderTable(results);
  }

  function searchCondition() {
    const q = document.getElementById("conditionSearch").value.toLowerCase();
    document.querySelectorAll('.cond-btn').forEach(b => {
      b.style.display = b.textContent.toLowerCase().includes(q) ? '' : 'none';
    });
  }

  function generateConditionList() {
    const container = document.getElementById("conditionList");
    container.innerHTML = `<button class="cond-btn active" data-cond="All" onclick="filterData('All')">
      <span>All Personnel</span><span class="cond-dot"></span>
    </button>`;
    allConditionsList.forEach(cond => {
      const btn = document.createElement("button");
      btn.className = "cond-btn";
      btn.dataset.cond = cond;
      btn.innerHTML = `<span>${cond}</span><span class="cond-dot"></span>`;
      btn.onclick = () => filterData(cond);
      container.appendChild(btn);
    });
  }

  function openModal(p) {
    if (typeof p === 'string') p = JSON.parse(p);
    const initials = p.name.split(' ').map(w => w[0]).join('').slice(0,2).toUpperCase();
    document.getElementById('modalAvatar').textContent = initials;
    document.getElementById('modalName').textContent = p.name;
    document.getElementById('modalDept').textContent = p.department + ' Department';
    document.getElementById('modalGender').textContent = p.gender;
    document.getElementById('modalBlood').textContent = p.blood || '—';

    document.getElementById('modalConditions').innerHTML = p.conditions.length > 0
      ? p.conditions.map(c => `<span class="pill ${HIGH_RISK.includes(c) ? 'high' : ''}">${c}</span>`).join('')
      : '<span style="color:var(--text-3);font-size:13px;">No conditions recorded</span>';

    const meds = p.conditions.filter(c => MEDICINES[c]).map(c => ({ condition: c, meds: MEDICINES[c] }));
    const medsTitle = document.getElementById('modalMedsTitle');
    const medsDiv = document.getElementById('modalMeds');
    if (meds.length > 0) {
      medsTitle.style.display = 'block';
      medsDiv.innerHTML = meds.flatMap(m =>
        m.meds.slice(0, 2).map(med =>
          `<div class="modal-med-card">
            <div class="modal-med-cond-label">${m.condition}</div>
            <div class="modal-med-name">${med.name}</div>
            <div class="modal-med-desc">${med.desc}</div>
          </div>`
        )
      ).join('');
    } else {
      medsTitle.style.display = 'none';
      medsDiv.innerHTML = '';
    }

    document.getElementById('modalOverlay').classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  function closeModal(e) {
    if (e.target === document.getElementById('modalOverlay')) closeModalDirect();
  }
  function closeModalDirect() {
    document.getElementById('modalOverlay').classList.remove('open');
    document.body.style.overflow = '';
  }

  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') closeModalDirect();
  });

  // Initialise: fetch CSRF token and personnel data in parallel
  fetchCsrfToken();

  fetch('/personnel')
    .then(res => {
      if (res.status === 401) { window.location.href = '/login'; return null; }
      return res.json();
    })
    .then(data => {
      if (!data) return;
      allData = data;
      filterData('All');
    })
    .catch(err => {
      console.error('Failed to load personnel:', err);
    });

  generateConditionList();
</script>
</body>
</html>