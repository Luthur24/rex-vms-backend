<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Admin Portal — REX Insurance VMS</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root {
  --bg: #FFFFFF; --surface: #F7F8FA; --surface-hover: #F0F2F5; --border: #E4E7EC;
  --text-primary: #1C2333; --text-secondary: #5B6472; --text-tertiary: #8A93A3;
  --accent: #6B4C6E; --accent-tint: #F1EAF2; --accent-hover: #573D59;
  --danger: #B3261E; --danger-bg: #FBEAE9; --success: #1E7B4D; --success-bg: #E7F5EC;
  --warn: #B8792A; --warn-bg: #FBF1E4;
  --font-display: 'Manrope', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --font-body: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: var(--font-body); background: var(--bg); color: var(--text-primary); -webkit-font-smoothing: antialiased; min-height: 100vh; transition: background-color .3s, color .3s; }
body.theme-dark { --bg: #0B0D12; --surface: #15171E; --surface-hover: #1C1F28; --border: #262A35; --text-primary: #F2F4F8; --text-secondary: #A6ADBB; --text-tertiary: #6E7684; --accent-tint: #241A26; --success-bg: #123324; --warn-bg: #2E230F; }
.top-bar { display: flex; align-items: center; justify-content: space-between; padding: 16px 32px; border-bottom: 1px solid var(--border); }
.top-left { display: flex; align-items: center; gap: 12px; }
.badge-icon { width: 34px; height: 34px; border-radius: 9px; background: var(--accent); display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.badge-icon svg { width: 18px; height: 18px; stroke: #fff; fill: none; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }
.top-left .titles .company { font-family: var(--font-display); font-weight: 800; font-size: 14.5px; }
.top-left .titles .portal { font-size: 12.5px; color: var(--text-secondary); }
.top-right { display: flex; align-items: center; gap: 14px; }
#clock { font-size: 12.5px; color: var(--text-tertiary); font-variant-numeric: tabular-nums; }
.user-chip { font-size: 12.5px; color: var(--text-secondary); background: var(--surface); border: 1px solid var(--border); padding: 6px 12px; border-radius: 100px; }
.logout-btn { font-size: 12.5px; font-weight: 600; color: var(--danger); background: var(--danger-bg); border: none; padding: 7px 12px; border-radius: 7px; cursor: pointer; }
.theme-toggle { width: 34px; height: 34px; border-radius: 50%; border: 1px solid var(--border); background: var(--surface); display: flex; align-items: center; justify-content: center; cursor: pointer; }
.theme-toggle:hover { background: var(--surface-hover); }
.theme-toggle svg { width: 16px; height: 16px; fill: none; stroke: var(--text-primary); stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; }
.theme-toggle .icon-moon { display: none; }
body.theme-dark .theme-toggle .icon-sun { display: none; }
body.theme-dark .theme-toggle .icon-moon { display: block; }
.conn-banner { display: none; background: var(--accent); color: #fff; font-size: 12.5px; font-weight: 600; text-align: center; padding: 8px; }
.conn-banner.show { display: block; }
.app-shell { display: none; } .app-shell.ready { display: block; }
.shell { display: flex; max-width: 1280px; margin: 0 auto; min-height: calc(100vh - 68px); }
.sidebar { width: 220px; flex-shrink: 0; padding: 24px 14px; border-right: 1px solid var(--border); }
.nav-item { display: flex; align-items: center; gap: 10px; width: 100%; text-align: left; padding: 10px 12px; border-radius: 9px; border: none; background: transparent; color: var(--text-secondary); font-size: 13.5px; font-weight: 600; cursor: pointer; margin-bottom: 4px; font-family: var(--font-body); }
.nav-item svg { width: 17px; height: 17px; fill: none; stroke: currentColor; stroke-width: 1.9; stroke-linecap: round; stroke-linejoin: round; flex-shrink: 0; }
.nav-item:hover { background: var(--surface-hover); color: var(--text-primary); }
.nav-item.active { background: var(--accent-tint); color: var(--accent); }
.content { flex: 1; padding: 28px 32px 60px; min-width: 0; }
.view { display: none; } .view.active { display: block; }
.view-title { font-family: var(--font-display); font-size: 20px; font-weight: 800; margin-bottom: 4px; }
.view-sub { font-size: 13px; color: var(--text-tertiary); margin-bottom: 22px; }
.stats-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 22px; }
.stat-card { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 16px 18px; }
.stat-card .num { font-family: var(--font-display); font-size: 24px; font-weight: 800; }
.stat-card .label { font-size: 11.5px; color: var(--text-tertiary); margin-top: 3px; }
.panel { background: var(--surface); border: 1px solid var(--border); border-radius: 14px; padding: 22px 22px 8px; margin-bottom: 20px; }
.panel-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; flex-wrap: wrap; gap: 10px; }
.panel-header h2 { font-family: var(--font-display); font-size: 15.5px; font-weight: 700; }
.panel-header .sub { font-size: 12.5px; color: var(--text-tertiary); }
.two-col { display: grid; grid-template-columns: 1.3fr 1fr; gap: 20px; }
.header-actions { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }
.search-row { position: relative; width: 260px; max-width: 100%; }
.search-row svg { position: absolute; left: 11px; top: 50%; transform: translateY(-50%); width: 15px; height: 15px; stroke: var(--text-tertiary); fill: none; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }
.search-row input { width: 100%; padding: 9px 12px 9px 33px; border-radius: 8px; border: 1px solid var(--border); background: var(--bg); color: var(--text-primary); font-size: 13.5px; outline: none; }
.search-row input:focus { border-color: var(--accent); box-shadow: 0 0 0 3px var(--accent-tint); }
table { width: 100%; border-collapse: collapse; }
thead th { text-align: left; font-size: 11.5px; font-weight: 700; letter-spacing: .03em; text-transform: uppercase; color: var(--text-tertiary); padding: 10px 12px; border-bottom: 1px solid var(--border); }
tbody td { padding: 12px; font-size: 13.5px; border-bottom: 1px solid var(--border); vertical-align: middle; }
tbody tr:last-child td { border-bottom: none; }
tbody tr:hover { background: var(--surface-hover); }
.name-cell { font-weight: 700; } .sub-cell { font-size: 11.5px; color: var(--text-tertiary); margin-top: 2px; }
.role-pill, .status-pill { display: inline-flex; align-items: center; gap: 5px; font-size: 11px; font-weight: 700; padding: 4px 10px; border-radius: 100px; white-space: nowrap; }
.role-pill.security { background: #E8F1F2; color: #0F4C5C; } body.theme-dark .role-pill.security { background: #12262B; }
.role-pill.frontdesk { background: var(--warn-bg); color: var(--warn); }
.role-pill.admin { background: var(--accent-tint); color: var(--accent); }
.status-pill .dot { width: 6px; height: 6px; border-radius: 50%; background: currentColor; }
.row-actions { display: flex; gap: 8px; justify-content: flex-end; }
.icon-btn { display: inline-flex; align-items: center; gap: 5px; font-size: 12.5px; font-weight: 600; color: var(--accent); background: var(--accent-tint); border: none; padding: 7px 12px; border-radius: 7px; cursor: pointer; }
.icon-btn:hover { filter: brightness(.96); } body.theme-dark .icon-btn:hover { filter: brightness(1.15); }
.btn-add { display: inline-flex; align-items: center; gap: 6px; font-size: 13px; font-weight: 700; color: #fff; background: var(--accent); border: none; padding: 9px 14px; border-radius: 8px; cursor: pointer; white-space: nowrap; }
.btn-add:hover { background: var(--accent-hover); }
.btn-add svg { width: 14px; height: 14px; fill: none; stroke: currentColor; stroke-width: 2.2; stroke-linecap: round; stroke-linejoin: round; }
.empty-row td { text-align: center; padding: 40px 20px; color: var(--text-tertiary); font-size: 13.5px; }
.visit-status-pill { display: inline-flex; align-items: center; gap: 5px; font-size: 11px; font-weight: 700; padding: 4px 10px; border-radius: 100px; white-space: nowrap; }
.visit-status-pill.checked-out { background: var(--success-bg); color: var(--success); }
.visit-status-pill.rejected { background: var(--danger-bg); color: var(--danger); }
.visit-status-pill.with-host, .visit-status-pill.approved, .visit-status-pill.pending, .visit-status-pill.hold { background: #E8F1F2; color: #0F4C5C; }
body.theme-dark .visit-status-pill.with-host, body.theme-dark .visit-status-pill.approved, body.theme-dark .visit-status-pill.pending, body.theme-dark .visit-status-pill.hold { background: #12262B; }
.visit-status-pill .dot { width: 6px; height: 6px; border-radius: 50%; background: currentColor; }
.bar-row { display: flex; align-items: center; gap: 10px; margin-bottom: 12px; }
.bar-row .bar-label { width: 110px; font-size: 12.5px; font-weight: 600; flex-shrink: 0; }
.bar-track { flex: 1; background: var(--bg); border-radius: 100px; height: 8px; overflow: hidden; }
.bar-fill { height: 100%; background: var(--accent); border-radius: 100px; }
.bar-row .bar-num { width: 28px; text-align: right; font-size: 12px; font-weight: 700; color: var(--text-tertiary); flex-shrink: 0; }
.charts-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-top: 16px; }
.chart-body { padding: 4px 18px 18px; }
.donut-wrap { display: flex; align-items: center; gap: 18px; flex-wrap: wrap; }
.donut { width: 130px; height: 130px; border-radius: 50%; position: relative; flex-shrink: 0; }
.donut::after { content: attr(data-total); position: absolute; inset: 24px; border-radius: 50%; background: var(--bg); display: flex; align-items: center; justify-content: center; font-family: var(--font-display); font-weight: 800; font-size: 22px; color: var(--text-primary); }
.legend { display: flex; flex-direction: column; gap: 7px; font-size: 12.5px; color: var(--text-secondary); min-width: 120px; flex: 1; }
.legend div { display: flex; align-items: center; gap: 8px; }
.legend i { width: 10px; height: 10px; border-radius: 3px; flex-shrink: 0; }
.legend b { margin-left: auto; color: var(--text-primary); }
.col-chart { display: flex; align-items: flex-end; gap: 10px; height: 150px; padding-top: 10px; }
.col-chart .col { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: flex-end; height: 100%; gap: 5px; }
.col-chart .col .v { font-size: 11px; font-weight: 700; color: var(--text-secondary); }
.col-chart .col .b { width: 100%; max-width: 34px; background: var(--accent); border-radius: 6px 6px 0 0; min-height: 3px; }
.col-chart .col .d { font-size: 11px; color: var(--text-tertiary); }
@media (max-width: 1100px) { .charts-row { grid-template-columns: 1fr; } }
.report-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 14px; }
.report-card { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 18px; display: flex; align-items: flex-start; gap: 14px; }
.report-card .r-icon { width: 38px; height: 38px; border-radius: 9px; background: var(--accent-tint); display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.report-card .r-icon svg { width: 18px; height: 18px; stroke: var(--accent); fill: none; stroke-width: 1.9; stroke-linecap: round; stroke-linejoin: round; }
.report-card .r-title { font-weight: 700; font-size: 13.5px; margin-bottom: 3px; }
.report-card .r-sub { font-size: 12px; color: var(--text-tertiary); margin-bottom: 12px; }
.report-actions { display: flex; gap: 8px; }
.btn-tiny { font-size: 12px; font-weight: 700; padding: 6px 11px; border-radius: 7px; cursor: pointer; border: 1px solid var(--border); background: var(--bg); color: var(--text-secondary); }
.btn-tiny:hover { background: var(--surface-hover); }
.btn-tiny.primary { background: var(--accent); color: #fff; border-color: var(--accent); }
.btn-tiny.primary:hover { background: var(--accent-hover); }
.logs-count-chip { font-size: 12px; font-weight: 600; color: var(--accent); background: var(--accent-tint); padding: 4px 10px; border-radius: 100px; white-space: nowrap; }
.load-more-row { text-align: center; padding: 18px 0; }
.btn-load-more { font-size: 13px; font-weight: 700; color: var(--accent); background: var(--accent-tint); border: none; padding: 10px 22px; border-radius: 9px; cursor: pointer; }
.btn-load-more:hover { filter: brightness(.96); } body.theme-dark .btn-load-more:hover { filter: brightness(1.15); }
.logs-fully-loaded { text-align: center; padding: 16px 0; font-size: 12.5px; color: var(--text-tertiary); }
.session-card { display: flex; align-items: center; justify-content: space-between; padding: 12px 14px; border: 1px solid var(--border); border-radius: 10px; margin-bottom: 8px; background: var(--bg); }
.session-card .s-name { font-weight: 700; font-size: 13.5px; }
.session-card .s-meta { font-size: 11.5px; color: var(--text-tertiary); margin-top: 2px; }
.concurrency-row { display: flex; align-items: center; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid var(--border); }
.concurrency-row:last-child { border-bottom: none; }
.concurrency-row .c-portal { font-weight: 700; font-size: 13.5px; text-transform: capitalize; }
.stepper { display: flex; align-items: center; gap: 10px; }
.stepper button { width: 28px; height: 28px; border-radius: 7px; border: 1px solid var(--border); background: var(--bg); cursor: pointer; font-weight: 700; color: var(--text-primary); }
.stepper button:hover { background: var(--surface-hover); }
.stepper .val { font-weight: 700; font-size: 14px; min-width: 16px; text-align: center; }
.modal-overlay { display: none; position: fixed; inset: 0; background: rgba(10,12,16,.5); align-items: center; justify-content: center; z-index: 100; padding: 20px; overflow-y: auto; }
.modal-overlay.show { display: flex; }
.modal { background: var(--bg); border: 1px solid var(--border); border-radius: 14px; width: 100%; max-width: 440px; padding: 24px; margin: auto; }
.modal h3 { font-family: var(--font-display); font-size: 16px; font-weight: 700; margin-bottom: 4px; }
.modal .modal-sub { font-size: 12.5px; color: var(--text-tertiary); margin-bottom: 18px; }
.field { display: flex; flex-direction: column; gap: 6px; margin-bottom: 14px; }
.field label { font-size: 12.5px; font-weight: 600; color: var(--text-secondary); }
.field input, .field select { font-family: var(--font-body); font-size: 13.5px; padding: 9px 11px; border-radius: 8px; border: 1px solid var(--border); background: var(--surface); color: var(--text-primary); outline: none; }
.field input:focus, .field select:focus { border-color: var(--accent); box-shadow: 0 0 0 3px var(--accent-tint); }
.field input.invalid { border-color: var(--danger); box-shadow: 0 0 0 3px var(--danger-bg); }
.field .error-text { font-size: 11.5px; color: var(--danger); display: none; margin-top: 2px; }
.field.error .error-text { display: block; }
.modal-actions { display: flex; gap: 10px; margin-top: 20px; }
.btn-primary { flex: 1; background: var(--accent); color: #fff; border: none; padding: 11px 16px; border-radius: 9px; font-size: 13.5px; font-weight: 700; cursor: pointer; }
.btn-primary:hover { background: var(--accent-hover); }
.btn-secondary { background: var(--surface); border: 1px solid var(--border); color: var(--text-secondary); padding: 11px 16px; border-radius: 9px; font-size: 13.5px; font-weight: 600; cursor: pointer; }
.btn-secondary:hover { background: var(--surface-hover); }
.toast { position: fixed; bottom: 24px; left: 50%; transform: translateX(-50%) translateY(10px); background: var(--accent); color: #fff; font-size: 13px; font-weight: 600; padding: 11px 18px; border-radius: 9px; opacity: 0; pointer-events: none; transition: opacity .2s, transform .2s; display: flex; align-items: center; gap: 8px; z-index: 300; }
.toast.show { opacity: 1; transform: translateX(-50%) translateY(0); }
.toast.error { background: var(--danger); }
.login-gate { min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 24px; }
.login-card { width: 100%; max-width: 380px; background: var(--surface); border: 1px solid var(--border); border-radius: 16px; padding: 32px 28px; }
.login-card .badge-icon { margin: 0 auto 18px; width: 46px; height: 46px; }
.login-card .badge-icon svg { width: 24px; height: 24px; }
.login-card h1 { font-family: var(--font-display); font-size: 18px; font-weight: 800; text-align: center; margin-bottom: 4px; }
.login-card .sub { font-size: 12.5px; color: var(--text-tertiary); text-align: center; margin-bottom: 24px; }
.login-error { font-size: 12.5px; color: var(--danger); background: var(--danger-bg); padding: 9px 12px; border-radius: 8px; margin-bottom: 14px; display: none; }
.login-error.show { display: block; }
.guide-fab { position: fixed; bottom: 24px; right: 24px; width: 52px; height: 52px; border-radius: 50%; background: var(--accent); border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 14px rgba(0,0,0,.25); z-index: 150; }
.guide-fab svg { width: 24px; height: 24px; stroke: #fff; fill: none; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }
.guide-panel { display: none; position: fixed; bottom: 88px; right: 24px; width: 340px; max-width: calc(100vw - 32px); max-height: 480px; background: var(--bg); border: 1px solid var(--border); border-radius: 16px; box-shadow: 0 10px 30px rgba(0,0,0,.2); z-index: 150; flex-direction: column; overflow: hidden; }
.guide-panel.show { display: flex; }
.guide-head { padding: 14px 16px; border-bottom: 1px solid var(--border); display: flex; align-items: center; justify-content: space-between; }
.guide-head .t { font-family: var(--font-display); font-weight: 700; font-size: 13.5px; }
.guide-head .close-guide { background: none; border: none; color: var(--text-tertiary); cursor: pointer; font-size: 18px; line-height: 1; }
.guide-body { flex: 1; overflow-y: auto; padding: 14px 16px; display: flex; flex-direction: column; gap: 10px; }
.guide-msg { font-size: 13px; line-height: 1.5; padding: 9px 12px; border-radius: 10px; max-width: 88%; }
.guide-msg.bot { background: var(--surface); align-self: flex-start; }
.guide-msg.user { background: var(--accent); color: #fff; align-self: flex-end; }
.guide-quick { display: flex; flex-wrap: wrap; gap: 6px; padding: 0 16px 12px; }
.guide-quick button { font-size: 11.5px; font-weight: 600; color: var(--accent); background: var(--accent-tint); border: none; padding: 6px 10px; border-radius: 100px; cursor: pointer; }
.guide-input-row { display: flex; gap: 8px; padding: 12px 16px; border-top: 1px solid var(--border); }
.guide-input-row input { flex: 1; font-size: 13px; padding: 9px 11px; border-radius: 8px; border: 1px solid var(--border); background: var(--surface); color: var(--text-primary); outline: none; }
.guide-input-row button { background: var(--accent); color: #fff; border: none; width: 36px; border-radius: 8px; cursor: pointer; flex-shrink: 0; }
@media (max-width: 980px) { .stats-row { grid-template-columns: repeat(2, 1fr); } .two-col { grid-template-columns: 1fr; } .report-grid { grid-template-columns: 1fr; } }
@media (max-width: 760px) { .shell { flex-direction: column; } .sidebar { width: 100%; border-right: none; border-bottom: 1px solid var(--border); display: flex; overflow-x: auto; padding: 12px; gap: 6px; } .nav-item { white-space: nowrap; margin-bottom: 0; } .content { padding: 20px; } .search-row { width: 100%; } }
.pw-wrap { position: relative; }
.pw-wrap input { padding-right: 64px; width: 100%; }
.pw-toggle { position: absolute; right: 6px; top: 50%; transform: translateY(-50%); background: none; border: none; color: var(--accent); font-size: 12.5px; font-weight: 700; cursor: pointer; padding: 8px; }
.switch-portal { display: block; text-align: center; margin-top: 14px; font-size: 12.5px; color: var(--text-secondary); text-decoration: none; }
.switch-portal:hover { text-decoration: underline; }
.login-card input { font-size: 16px; }
body.theme-dark .login-card .sub { color: #98A0AE; }
body.theme-dark { --accent: #8A5C90; --accent-hover: #744B79; }
@media (max-width: 720px) {
  .panel { overflow-x: auto; }
  table { min-width: 620px; }
}
/* ===== Deep-navy theme + animated wave background ===== */
body.theme-dark {
  color-scheme: dark; background: #050B1F;
  --bg: #0A1230; --surface: #101B42; --surface-hover: #182760; --border: #243372;
  --text-primary: #EAF0FF; --text-secondary: #B6C3E8; --text-tertiary: #8E9DCB;
  --accent-tint: #2A2260; --accent-fg: #C4B5FD;
  --success: #4ADE9A; --success-bg: #0E3A2E; --warn-bg: #3A2C12; --hold-bg: #17224F;
  --danger: #FF8F86; --danger-bg: rgba(255,110,100,.15);
  --glass: rgba(13,22,58,.58); --glass-edge: rgba(130,160,255,.20);

}
.bg-fx { position: fixed; inset: 0; z-index: -1; overflow: hidden; pointer-events: none;
  background: radial-gradient(120% 80% at 50% -10%, #12246B 0%, transparent 60%), linear-gradient(180deg, #060D2A 0%, #040A1E 100%); }
.fx-orb { position: absolute; border-radius: 50%; will-change: transform; }
.fx-orb.o1 { width: 70vmax; height: 70vmax; left: -25vmax; top: -30vmax; background: radial-gradient(closest-side, rgba(139,92,246,.34), transparent); animation: fx-orb1 32s ease-in-out infinite alternate; }
.fx-orb.o2 { width: 60vmax; height: 60vmax; right: -22vmax; top: -18vmax; background: radial-gradient(closest-side, rgba(59,130,246,.30), transparent); animation: fx-orb2 38s ease-in-out infinite alternate; }
@keyframes fx-orb1 { to { transform: translate3d(14vmax, 8vmax, 0) scale(1.12); } }
@keyframes fx-orb2 { to { transform: translate3d(-12vmax, 10vmax, 0) scale(1.10); } }
.fx-stars { position: absolute; left: 0; top: 0; width: 100%; height: 68%; }
.fx-stars circle { fill: #CFE0FF; opacity: .2; animation: fx-tw 5s ease-in-out infinite; }
@keyframes fx-tw { 0%, 100% { opacity: .12; } 50% { opacity: .9; } }
.fx-bob { position: absolute; left: 0; right: 0; bottom: -24px; animation: fx-bob 12s ease-in-out infinite alternate; will-change: transform; }
@keyframes fx-bob { to { transform: translate3d(0, -14px, 0); } }
.fx-wave { position: absolute; left: 0; bottom: 0; width: 200%; height: 100%; animation: fx-drift 60s linear infinite; will-change: transform; }
.fx-wave.rev { animation-direction: reverse; }
.fx-wave svg { display: block; width: 100%; height: 100%; }
.fx-line { fill: none; stroke-width: 1.6; vector-effect: non-scaling-stroke; stroke-linejoin: round; }
@keyframes fx-drift { to { transform: translate3d(-50%, 0, 0); } }
@media (prefers-reduced-motion: reduce) { .bg-fx * { animation: none !important; } }

/* Frosted navy panels */
.top-bar { background: rgba(6,12,36,.55); border-bottom-color: var(--glass-edge); -webkit-backdrop-filter: saturate(140%) blur(12px); backdrop-filter: saturate(140%) blur(12px); }
.sidebar { background: rgba(6,12,36,.42); border-right-color: var(--glass-edge); -webkit-backdrop-filter: blur(10px); backdrop-filter: blur(10px); }
.panel, .stat-box, .stat-card, .report-card, .session-card, .login-card {
  background: var(--glass); border-color: var(--glass-edge);
  box-shadow: 0 18px 50px -26px rgba(0,0,0,.65), inset 0 1px 0 rgba(255,255,255,.04);
  -webkit-backdrop-filter: blur(12px); backdrop-filter: blur(12px);
}
.login-card { box-shadow: 0 30px 80px -30px rgba(0,0,0,.7), 0 0 0 1px rgba(255,255,255,.03) inset; }
.fullpage { background: rgba(6,12,34,.82); -webkit-backdrop-filter: blur(14px); backdrop-filter: blur(14px); }
.modal-overlay { background: rgba(3,6,20,.62); -webkit-backdrop-filter: blur(4px); backdrop-filter: blur(4px); }
.modal, .guide-panel { box-shadow: 0 28px 70px -24px rgba(0,0,0,.75); }
@supports not ((backdrop-filter: blur(1px)) or (-webkit-backdrop-filter: blur(1px))) {
  .top-bar, .sidebar, .panel, .stat-box, .stat-card, .report-card, .session-card, .login-card { background: rgba(10,18,48,.92); }
  .fullpage { background: #060C22; }
}

/* Light-on-dark text for items that used the accent colour as text */
body.theme-dark :is(.count-chip, .edit-btn, .appt-toggle button.active, .detail-avatar, .visit-status-cell.pending,
  .visit-status-cell.hold, .visit-status-cell.approved, .visit-status-cell.with-host, .recent-tag, .guide-quick button,
  .pw-toggle, .appt-tag.walkin, .status-pill.pending, .modal-avatar, .nav-item.active, .role-pill.admin, .icon-btn,
  .logs-count-chip, .btn-load-more) { color: var(--accent-fg); }
body.theme-dark :is(.appt-tag.scheduled, .status-pill.approved, .role-pill.security, .visit-status-pill.with-host,
  .visit-status-pill.approved, .visit-status-pill.pending, .visit-status-pill.hold) { background: #0E3550; color: #7DD3E8; }

@media (max-width: 720px) {
  .top-bar { padding: 12px 16px; gap: 10px; }
  .top-right { gap: 8px; }
  #clock { display: none; }
  .top-left .titles .portal { white-space: nowrap; }
}

/* ===== Portal switcher (links to the other two portals) ===== */
.portal-switch { display: flex; align-items: center; gap: 6px; }
.portal-switch .ps-label { font-size: 11.5px; color: var(--text-tertiary); margin-right: 2px; }
.portal-switch a { font-size: 12.5px; font-weight: 600; color: var(--text-secondary); text-decoration: none; padding: 6px 12px; border: 1px solid var(--border); border-radius: 100px; background: var(--surface); white-space: nowrap; transition: color .15s, border-color .15s, background-color .15s; }
.portal-switch a:hover, .portal-switch a:focus-visible { color: var(--text-primary); border-color: var(--accent); background: var(--accent-tint); }
.login-card .portal-switch { flex-wrap: wrap; justify-content: center; margin-top: 18px; padding-top: 16px; border-top: 1px solid var(--border); }
.login-card .portal-switch .ps-label { width: 100%; text-align: center; margin: 0 0 2px; }
@media (max-width: 720px) {
  .top-bar { flex-wrap: wrap; }
  .top-bar .portal-switch { order: 3; width: 100%; justify-content: center; }
}
</style>
</head>
<body class="theme-dark">
<div class="bg-fx" aria-hidden="true"><div class="fx-orb o1"></div><div class="fx-orb o2"></div><svg class="fx-stars" viewBox="0 0 1000 600" preserveAspectRatio="xMidYMid slice"><circle cx="324" cy="91" r="1.3" style="animation-duration:3.3s;animation-delay:-3.8s"/><circle cx="366" cy="35" r="1.2" style="animation-duration:3.1s;animation-delay:-3.0s"/><circle cx="70" cy="54" r="1.1" style="animation-duration:6.3s;animation-delay:-0.9s"/><circle cx="223" cy="376" r="1.6" style="animation-duration:5.3s;animation-delay:-2.8s"/><circle cx="976" cy="28" r="1.5" style="animation-duration:4.2s;animation-delay:-1.0s"/><circle cx="118" cy="185" r="1.4" style="animation-duration:3.7s;animation-delay:-4.1s"/><circle cx="639" cy="223" r="1.2" style="animation-duration:3.3s;animation-delay:-0.4s"/><circle cx="206" cy="408" r="1.1" style="animation-duration:4.3s;animation-delay:-4.1s"/><circle cx="453" cy="180" r="1.4" style="animation-duration:5.8s;animation-delay:-1.7s"/><circle cx="574" cy="315" r="1.5" style="animation-duration:5.9s;animation-delay:-2.0s"/><circle cx="980" cy="71" r="1.1" style="animation-duration:6.0s;animation-delay:-1.1s"/><circle cx="489" cy="24" r="1.3" style="animation-duration:6.1s;animation-delay:-4.0s"/><circle cx="875" cy="188" r="1.3" style="animation-duration:5.4s;animation-delay:-4.1s"/><circle cx="456" cy="504" r="1.6" style="animation-duration:4.9s;animation-delay:-4.6s"/><circle cx="61" cy="421" r="1.3" style="animation-duration:7.0s;animation-delay:-5.8s"/><circle cx="285" cy="231" r="1.3" style="animation-duration:3.1s;animation-delay:-3.2s"/><circle cx="168" cy="70" r="0.8" style="animation-duration:6.1s;animation-delay:-0.9s"/><circle cx="248" cy="235" r="1.5" style="animation-duration:3.3s;animation-delay:-3.1s"/><circle cx="549" cy="530" r="1.4" style="animation-duration:6.5s;animation-delay:-1.9s"/><circle cx="415" cy="215" r="1.5" style="animation-duration:6.8s;animation-delay:-1.1s"/><circle cx="176" cy="139" r="0.9" style="animation-duration:4.9s;animation-delay:-4.1s"/><circle cx="263" cy="2" r="1.1" style="animation-duration:4.5s;animation-delay:-4.0s"/><circle cx="953" cy="414" r="1.2" style="animation-duration:5.5s;animation-delay:-4.7s"/><circle cx="54" cy="540" r="1.4" style="animation-duration:6.5s;animation-delay:-5.6s"/><circle cx="392" cy="239" r="0.8" style="animation-duration:5.5s;animation-delay:-0.4s"/><circle cx="67" cy="125" r="0.8" style="animation-duration:4.4s;animation-delay:-0.4s"/><circle cx="0" cy="91" r="0.8" style="animation-duration:4.5s;animation-delay:-0.2s"/><circle cx="874" cy="368" r="0.8" style="animation-duration:4.0s;animation-delay:-2.4s"/><circle cx="364" cy="74" r="1.5" style="animation-duration:7.0s;animation-delay:-3.3s"/><circle cx="484" cy="52" r="0.8" style="animation-duration:4.4s;animation-delay:-1.9s"/><circle cx="829" cy="97" r="0.7" style="animation-duration:6.8s;animation-delay:-3.7s"/><circle cx="147" cy="326" r="0.7" style="animation-duration:5.1s;animation-delay:-6.8s"/><circle cx="863" cy="418" r="0.9" style="animation-duration:4.5s;animation-delay:-1.2s"/><circle cx="772" cy="320" r="1.4" style="animation-duration:4.3s;animation-delay:-1.6s"/><circle cx="812" cy="591" r="1.5" style="animation-duration:6.2s;animation-delay:-5.7s"/><circle cx="740" cy="136" r="1.2" style="animation-duration:4.4s;animation-delay:-0.2s"/><circle cx="28" cy="168" r="0.9" style="animation-duration:5.8s;animation-delay:-6.7s"/><circle cx="447" cy="562" r="1.6" style="animation-duration:6.8s;animation-delay:-2.6s"/><circle cx="220" cy="136" r="0.9" style="animation-duration:3.8s;animation-delay:-4.4s"/><circle cx="900" cy="504" r="1.1" style="animation-duration:5.6s;animation-delay:-5.6s"/><circle cx="85" cy="396" r="1.5" style="animation-duration:6.1s;animation-delay:-5.3s"/><circle cx="478" cy="107" r="1.4" style="animation-duration:4.3s;animation-delay:-5.6s"/><circle cx="972" cy="238" r="1.1" style="animation-duration:6.8s;animation-delay:-5.1s"/><circle cx="170" cy="76" r="0.8" style="animation-duration:6.6s;animation-delay:-5.6s"/><circle cx="146" cy="496" r="1.6" style="animation-duration:5.6s;animation-delay:-2.5s"/><circle cx="549" cy="79" r="0.7" style="animation-duration:6.9s;animation-delay:-4.5s"/></svg><div class="fx-bob" style="height:calc(62vh + 24px);animation-duration:14s;animation-delay:-3s"><div class="fx-wave" style="animation-duration:90s"><svg viewBox="0 0 2880 320" preserveAspectRatio="none"><defs><linearGradient id="fxg1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2B3FBF" stop-opacity="0.55"/><stop offset="1" stop-color="#0A1448" stop-opacity="0.9"/></linearGradient></defs><path d="M0,91.5 L18,94.2 L36,95.9 L54,96.7 L72,96.5 L90,95.7 L108,94.1 L126,92.0 L144,89.6 L162,86.9 L180,84.2 L198,81.5 L216,78.9 L234,76.5 L252,74.4 L270,72.6 L288,71.0 L306,69.6 L324,68.4 L342,67.3 L360,66.3 L378,65.1 L396,63.9 L414,62.5 L432,61.0 L450,59.2 L468,57.3 L486,55.3 L504,53.2 L522,51.2 L540,49.4 L558,47.9 L576,46.9 L594,46.5 L612,46.7 L630,47.7 L648,49.5 L666,52.2 L684,55.7 L702,60.0 L720,65.0 L738,70.5 L756,76.4 L774,82.4 L792,88.3 L810,93.9 L828,98.9 L846,103.1 L864,106.4 L882,108.5 L900,109.3 L918,108.8 L936,106.9 L954,103.6 L972,99.2 L990,93.6 L1008,87.1 L1026,79.9 L1044,72.4 L1062,64.7 L1080,57.2 L1098,50.1 L1116,43.8 L1134,38.4 L1152,34.2 L1170,31.3 L1188,29.7 L1206,29.6 L1224,30.8 L1242,33.4 L1260,37.1 L1278,41.8 L1296,47.3 L1314,53.4 L1332,59.8 L1350,66.2 L1368,72.4 L1386,78.2 L1404,83.5 L1422,87.9 L1440,91.5 L1458,94.2 L1476,95.9 L1494,96.7 L1512,96.5 L1530,95.7 L1548,94.1 L1566,92.0 L1584,89.6 L1602,86.9 L1620,84.2 L1638,81.5 L1656,78.9 L1674,76.5 L1692,74.4 L1710,72.6 L1728,71.0 L1746,69.6 L1764,68.4 L1782,67.3 L1800,66.3 L1818,65.1 L1836,63.9 L1854,62.5 L1872,61.0 L1890,59.2 L1908,57.3 L1926,55.3 L1944,53.2 L1962,51.2 L1980,49.4 L1998,47.9 L2016,46.9 L2034,46.5 L2052,46.7 L2070,47.7 L2088,49.5 L2106,52.2 L2124,55.7 L2142,60.0 L2160,65.0 L2178,70.5 L2196,76.4 L2214,82.4 L2232,88.3 L2250,93.9 L2268,98.9 L2286,103.1 L2304,106.4 L2322,108.5 L2340,109.3 L2358,108.8 L2376,106.9 L2394,103.6 L2412,99.2 L2430,93.6 L2448,87.1 L2466,79.9 L2484,72.4 L2502,64.7 L2520,57.2 L2538,50.1 L2556,43.8 L2574,38.4 L2592,34.2 L2610,31.3 L2628,29.7 L2646,29.6 L2664,30.8 L2682,33.4 L2700,37.1 L2718,41.8 L2736,47.3 L2754,53.4 L2772,59.8 L2790,66.2 L2808,72.4 L2826,78.2 L2844,83.5 L2862,87.9 L2880,91.5 L2880,320 L0,320 Z" fill="url(#fxg1)"/><path class="fx-line" d="M0,91.5 L18,94.2 L36,95.9 L54,96.7 L72,96.5 L90,95.7 L108,94.1 L126,92.0 L144,89.6 L162,86.9 L180,84.2 L198,81.5 L216,78.9 L234,76.5 L252,74.4 L270,72.6 L288,71.0 L306,69.6 L324,68.4 L342,67.3 L360,66.3 L378,65.1 L396,63.9 L414,62.5 L432,61.0 L450,59.2 L468,57.3 L486,55.3 L504,53.2 L522,51.2 L540,49.4 L558,47.9 L576,46.9 L594,46.5 L612,46.7 L630,47.7 L648,49.5 L666,52.2 L684,55.7 L702,60.0 L720,65.0 L738,70.5 L756,76.4 L774,82.4 L792,88.3 L810,93.9 L828,98.9 L846,103.1 L864,106.4 L882,108.5 L900,109.3 L918,108.8 L936,106.9 L954,103.6 L972,99.2 L990,93.6 L1008,87.1 L1026,79.9 L1044,72.4 L1062,64.7 L1080,57.2 L1098,50.1 L1116,43.8 L1134,38.4 L1152,34.2 L1170,31.3 L1188,29.7 L1206,29.6 L1224,30.8 L1242,33.4 L1260,37.1 L1278,41.8 L1296,47.3 L1314,53.4 L1332,59.8 L1350,66.2 L1368,72.4 L1386,78.2 L1404,83.5 L1422,87.9 L1440,91.5 L1458,94.2 L1476,95.9 L1494,96.7 L1512,96.5 L1530,95.7 L1548,94.1 L1566,92.0 L1584,89.6 L1602,86.9 L1620,84.2 L1638,81.5 L1656,78.9 L1674,76.5 L1692,74.4 L1710,72.6 L1728,71.0 L1746,69.6 L1764,68.4 L1782,67.3 L1800,66.3 L1818,65.1 L1836,63.9 L1854,62.5 L1872,61.0 L1890,59.2 L1908,57.3 L1926,55.3 L1944,53.2 L1962,51.2 L1980,49.4 L1998,47.9 L2016,46.9 L2034,46.5 L2052,46.7 L2070,47.7 L2088,49.5 L2106,52.2 L2124,55.7 L2142,60.0 L2160,65.0 L2178,70.5 L2196,76.4 L2214,82.4 L2232,88.3 L2250,93.9 L2268,98.9 L2286,103.1 L2304,106.4 L2322,108.5 L2340,109.3 L2358,108.8 L2376,106.9 L2394,103.6 L2412,99.2 L2430,93.6 L2448,87.1 L2466,79.9 L2484,72.4 L2502,64.7 L2520,57.2 L2538,50.1 L2556,43.8 L2574,38.4 L2592,34.2 L2610,31.3 L2628,29.7 L2646,29.6 L2664,30.8 L2682,33.4 L2700,37.1 L2718,41.8 L2736,47.3 L2754,53.4 L2772,59.8 L2790,66.2 L2808,72.4 L2826,78.2 L2844,83.5 L2862,87.9 L2880,91.5" stroke="('#7C93FF', 0.35)" stroke-opacity="1"/></svg></div></div><div class="fx-bob" style="height:calc(52vh + 24px);animation-duration:12s;animation-delay:-6s"><div class="fx-wave rev" style="animation-duration:64s"><svg viewBox="0 0 2880 320" preserveAspectRatio="none"><defs><linearGradient id="fxg2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3A56E8" stop-opacity="0.45"/><stop offset="1" stop-color="#0E1B5E" stop-opacity="0.9"/></linearGradient></defs><path d="M0,124.4 L18,124.0 L36,120.9 L54,115.3 L72,107.6 L90,98.3 L108,88.3 L126,78.7 L144,70.3 L162,64.2 L180,60.8 L198,60.6 L216,63.4 L234,68.9 L252,76.4 L270,85.1 L288,94.1 L306,102.4 L324,109.3 L342,114.4 L360,117.3 L378,118.1 L396,117.2 L414,115.0 L432,112.2 L450,109.1 L468,106.4 L486,104.3 L504,102.8 L522,101.8 L540,101.1 L558,100.1 L576,98.6 L594,96.2 L612,92.7 L630,88.3 L648,83.2 L666,77.9 L684,73.1 L702,69.4 L720,67.6 L738,68.0 L756,71.1 L774,76.7 L792,84.4 L810,93.7 L828,103.7 L846,113.3 L864,121.7 L882,127.8 L900,131.2 L918,131.4 L936,128.6 L954,123.1 L972,115.6 L990,106.9 L1008,97.9 L1026,89.6 L1044,82.7 L1062,77.6 L1080,74.7 L1098,73.9 L1116,74.8 L1134,77.0 L1152,79.8 L1170,82.9 L1188,85.6 L1206,87.7 L1224,89.2 L1242,90.2 L1260,90.9 L1278,91.9 L1296,93.4 L1314,95.8 L1332,99.3 L1350,103.7 L1368,108.8 L1386,114.1 L1404,118.9 L1422,122.6 L1440,124.4 L1458,124.0 L1476,120.9 L1494,115.3 L1512,107.6 L1530,98.3 L1548,88.3 L1566,78.7 L1584,70.3 L1602,64.2 L1620,60.8 L1638,60.6 L1656,63.4 L1674,68.9 L1692,76.4 L1710,85.1 L1728,94.1 L1746,102.4 L1764,109.3 L1782,114.4 L1800,117.3 L1818,118.1 L1836,117.2 L1854,115.0 L1872,112.2 L1890,109.1 L1908,106.4 L1926,104.3 L1944,102.8 L1962,101.8 L1980,101.1 L1998,100.1 L2016,98.6 L2034,96.2 L2052,92.7 L2070,88.3 L2088,83.2 L2106,77.9 L2124,73.1 L2142,69.4 L2160,67.6 L2178,68.0 L2196,71.1 L2214,76.7 L2232,84.4 L2250,93.7 L2268,103.7 L2286,113.3 L2304,121.7 L2322,127.8 L2340,131.2 L2358,131.4 L2376,128.6 L2394,123.1 L2412,115.6 L2430,106.9 L2448,97.9 L2466,89.6 L2484,82.7 L2502,77.6 L2520,74.7 L2538,73.9 L2556,74.8 L2574,77.0 L2592,79.8 L2610,82.9 L2628,85.6 L2646,87.7 L2664,89.2 L2682,90.2 L2700,90.9 L2718,91.9 L2736,93.4 L2754,95.8 L2772,99.3 L2790,103.7 L2808,108.8 L2826,114.1 L2844,118.9 L2862,122.6 L2880,124.4 L2880,320 L0,320 Z" fill="url(#fxg2)"/><path class="fx-line" d="M0,124.4 L18,124.0 L36,120.9 L54,115.3 L72,107.6 L90,98.3 L108,88.3 L126,78.7 L144,70.3 L162,64.2 L180,60.8 L198,60.6 L216,63.4 L234,68.9 L252,76.4 L270,85.1 L288,94.1 L306,102.4 L324,109.3 L342,114.4 L360,117.3 L378,118.1 L396,117.2 L414,115.0 L432,112.2 L450,109.1 L468,106.4 L486,104.3 L504,102.8 L522,101.8 L540,101.1 L558,100.1 L576,98.6 L594,96.2 L612,92.7 L630,88.3 L648,83.2 L666,77.9 L684,73.1 L702,69.4 L720,67.6 L738,68.0 L756,71.1 L774,76.7 L792,84.4 L810,93.7 L828,103.7 L846,113.3 L864,121.7 L882,127.8 L900,131.2 L918,131.4 L936,128.6 L954,123.1 L972,115.6 L990,106.9 L1008,97.9 L1026,89.6 L1044,82.7 L1062,77.6 L1080,74.7 L1098,73.9 L1116,74.8 L1134,77.0 L1152,79.8 L1170,82.9 L1188,85.6 L1206,87.7 L1224,89.2 L1242,90.2 L1260,90.9 L1278,91.9 L1296,93.4 L1314,95.8 L1332,99.3 L1350,103.7 L1368,108.8 L1386,114.1 L1404,118.9 L1422,122.6 L1440,124.4 L1458,124.0 L1476,120.9 L1494,115.3 L1512,107.6 L1530,98.3 L1548,88.3 L1566,78.7 L1584,70.3 L1602,64.2 L1620,60.8 L1638,60.6 L1656,63.4 L1674,68.9 L1692,76.4 L1710,85.1 L1728,94.1 L1746,102.4 L1764,109.3 L1782,114.4 L1800,117.3 L1818,118.1 L1836,117.2 L1854,115.0 L1872,112.2 L1890,109.1 L1908,106.4 L1926,104.3 L1944,102.8 L1962,101.8 L1980,101.1 L1998,100.1 L2016,98.6 L2034,96.2 L2052,92.7 L2070,88.3 L2088,83.2 L2106,77.9 L2124,73.1 L2142,69.4 L2160,67.6 L2178,68.0 L2196,71.1 L2214,76.7 L2232,84.4 L2250,93.7 L2268,103.7 L2286,113.3 L2304,121.7 L2322,127.8 L2340,131.2 L2358,131.4 L2376,128.6 L2394,123.1 L2412,115.6 L2430,106.9 L2448,97.9 L2466,89.6 L2484,82.7 L2502,77.6 L2520,74.7 L2538,73.9 L2556,74.8 L2574,77.0 L2592,79.8 L2610,82.9 L2628,85.6 L2646,87.7 L2664,89.2 L2682,90.2 L2700,90.9 L2718,91.9 L2736,93.4 L2754,95.8 L2772,99.3 L2790,103.7 L2808,108.8 L2826,114.1 L2844,118.9 L2862,122.6 L2880,124.4" stroke="('#6D8BFF', 0.45)" stroke-opacity="1"/></svg></div></div><div class="fx-bob" style="height:calc(43vh + 24px);animation-duration:10s;animation-delay:-9s"><div class="fx-wave" style="animation-duration:48s"><svg viewBox="0 0 2880 320" preserveAspectRatio="none"><defs><linearGradient id="fxg3" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4F7BFF" stop-opacity="0.3"/><stop offset="1" stop-color="#101F6E" stop-opacity="0.75"/></linearGradient></defs><path d="M0,143.8 L18,139.9 L36,134.0 L54,127.9 L72,122.7 L90,119.2 L108,117.4 L126,116.6 L144,115.7 L162,114.0 L180,111.1 L198,107.0 L216,102.9 L234,100.0 L252,99.7 L270,102.9 L288,109.7 L306,119.3 L324,130.1 L342,140.1 L360,147.2 L378,150.0 L396,147.8 L414,141.3 L432,131.8 L450,121.3 L468,111.9 L486,105.0 L504,101.6 L522,101.5 L540,103.8 L558,107.2 L576,110.4 L594,112.7 L612,113.8 L630,114.2 L648,115.0 L666,117.0 L684,120.8 L702,126.6 L720,133.5 L738,140.0 L756,144.6 L774,145.8 L792,142.6 L810,135.3 L828,124.9 L846,113.3 L864,102.6 L882,95.0 L900,91.7 L918,93.0 L936,98.4 L954,106.3 L972,115.0 L990,122.6 L1008,128.1 L1026,130.9 L1044,131.5 L1062,130.9 L1080,130.1 L1098,130.0 L1116,130.9 L1134,132.4 L1152,133.5 L1170,133.2 L1188,130.4 L1206,124.8 L1224,116.7 L1242,107.5 L1260,98.9 L1278,92.9 L1296,90.9 L1314,93.7 L1332,100.9 L1350,111.3 L1368,122.8 L1386,133.2 L1404,140.8 L1422,144.4 L1440,143.8 L1458,139.9 L1476,134.0 L1494,127.9 L1512,122.7 L1530,119.2 L1548,117.4 L1566,116.6 L1584,115.7 L1602,114.0 L1620,111.1 L1638,107.0 L1656,102.9 L1674,100.0 L1692,99.7 L1710,102.9 L1728,109.7 L1746,119.3 L1764,130.1 L1782,140.1 L1800,147.2 L1818,150.0 L1836,147.8 L1854,141.3 L1872,131.8 L1890,121.3 L1908,111.9 L1926,105.0 L1944,101.6 L1962,101.5 L1980,103.8 L1998,107.2 L2016,110.4 L2034,112.7 L2052,113.8 L2070,114.2 L2088,115.0 L2106,117.0 L2124,120.8 L2142,126.6 L2160,133.5 L2178,140.0 L2196,144.6 L2214,145.8 L2232,142.6 L2250,135.3 L2268,124.9 L2286,113.3 L2304,102.6 L2322,95.0 L2340,91.7 L2358,93.0 L2376,98.4 L2394,106.3 L2412,115.0 L2430,122.6 L2448,128.1 L2466,130.9 L2484,131.5 L2502,130.9 L2520,130.1 L2538,130.0 L2556,130.9 L2574,132.4 L2592,133.5 L2610,133.2 L2628,130.4 L2646,124.8 L2664,116.7 L2682,107.5 L2700,98.9 L2718,92.9 L2736,90.9 L2754,93.7 L2772,100.9 L2790,111.3 L2808,122.8 L2826,133.2 L2844,140.8 L2862,144.4 L2880,143.8 L2880,320 L0,320 Z" fill="url(#fxg3)"/><path class="fx-line" d="M0,143.8 L18,139.9 L36,134.0 L54,127.9 L72,122.7 L90,119.2 L108,117.4 L126,116.6 L144,115.7 L162,114.0 L180,111.1 L198,107.0 L216,102.9 L234,100.0 L252,99.7 L270,102.9 L288,109.7 L306,119.3 L324,130.1 L342,140.1 L360,147.2 L378,150.0 L396,147.8 L414,141.3 L432,131.8 L450,121.3 L468,111.9 L486,105.0 L504,101.6 L522,101.5 L540,103.8 L558,107.2 L576,110.4 L594,112.7 L612,113.8 L630,114.2 L648,115.0 L666,117.0 L684,120.8 L702,126.6 L720,133.5 L738,140.0 L756,144.6 L774,145.8 L792,142.6 L810,135.3 L828,124.9 L846,113.3 L864,102.6 L882,95.0 L900,91.7 L918,93.0 L936,98.4 L954,106.3 L972,115.0 L990,122.6 L1008,128.1 L1026,130.9 L1044,131.5 L1062,130.9 L1080,130.1 L1098,130.0 L1116,130.9 L1134,132.4 L1152,133.5 L1170,133.2 L1188,130.4 L1206,124.8 L1224,116.7 L1242,107.5 L1260,98.9 L1278,92.9 L1296,90.9 L1314,93.7 L1332,100.9 L1350,111.3 L1368,122.8 L1386,133.2 L1404,140.8 L1422,144.4 L1440,143.8 L1458,139.9 L1476,134.0 L1494,127.9 L1512,122.7 L1530,119.2 L1548,117.4 L1566,116.6 L1584,115.7 L1602,114.0 L1620,111.1 L1638,107.0 L1656,102.9 L1674,100.0 L1692,99.7 L1710,102.9 L1728,109.7 L1746,119.3 L1764,130.1 L1782,140.1 L1800,147.2 L1818,150.0 L1836,147.8 L1854,141.3 L1872,131.8 L1890,121.3 L1908,111.9 L1926,105.0 L1944,101.6 L1962,101.5 L1980,103.8 L1998,107.2 L2016,110.4 L2034,112.7 L2052,113.8 L2070,114.2 L2088,115.0 L2106,117.0 L2124,120.8 L2142,126.6 L2160,133.5 L2178,140.0 L2196,144.6 L2214,145.8 L2232,142.6 L2250,135.3 L2268,124.9 L2286,113.3 L2304,102.6 L2322,95.0 L2340,91.7 L2358,93.0 L2376,98.4 L2394,106.3 L2412,115.0 L2430,122.6 L2448,128.1 L2466,130.9 L2484,131.5 L2502,130.9 L2520,130.1 L2538,130.0 L2556,130.9 L2574,132.4 L2592,133.5 L2610,133.2 L2628,130.4 L2646,124.8 L2664,116.7 L2682,107.5 L2700,98.9 L2718,92.9 L2736,90.9 L2754,93.7 L2772,100.9 L2790,111.3 L2808,122.8 L2826,133.2 L2844,140.8 L2862,144.4 L2880,143.8" stroke="('#8FB0FF', 0.5)" stroke-opacity="1"/></svg></div></div><div class="fx-bob" style="height:calc(33vh + 24px);animation-duration:9s;animation-delay:-12s"><div class="fx-wave rev" style="animation-duration:36s"><svg viewBox="0 0 2880 320" preserveAspectRatio="none"><defs><linearGradient id="fxg4" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0E2F7A" stop-opacity="0.95"/><stop offset="1" stop-color="#050B22" stop-opacity="1.0"/></linearGradient></defs><path d="M0,161.1 L18,165.8 L36,165.9 L54,162.7 L72,158.6 L90,155.5 L108,154.0 L126,153.6 L144,152.4 L162,149.0 L180,143.2 L198,136.3 L216,130.8 L234,129.4 L252,133.5 L270,142.7 L288,154.3 L306,164.9 L324,171.3 L342,171.9 L360,167.0 L378,159.2 L396,151.3 L414,145.6 L432,143.1 L450,142.8 L468,143.1 L486,142.3 L504,140.1 L522,137.5 L540,136.5 L558,139.2 L576,146.0 L594,155.8 L612,165.7 L630,172.5 L648,173.6 L666,168.5 L684,159.0 L702,148.0 L720,138.9 L738,134.2 L756,134.1 L774,137.3 L792,141.4 L810,144.5 L828,146.0 L846,146.4 L864,147.6 L882,151.0 L900,156.8 L918,163.7 L936,169.2 L954,170.6 L972,166.5 L990,157.3 L1008,145.7 L1026,135.1 L1044,128.7 L1062,128.1 L1080,133.0 L1098,140.8 L1116,148.7 L1134,154.4 L1152,156.9 L1170,157.2 L1188,156.9 L1206,157.7 L1224,159.9 L1242,162.5 L1260,163.5 L1278,160.8 L1296,154.0 L1314,144.2 L1332,134.3 L1350,127.5 L1368,126.4 L1386,131.5 L1404,141.0 L1422,152.0 L1440,161.1 L1458,165.8 L1476,165.9 L1494,162.7 L1512,158.6 L1530,155.5 L1548,154.0 L1566,153.6 L1584,152.4 L1602,149.0 L1620,143.2 L1638,136.3 L1656,130.8 L1674,129.4 L1692,133.5 L1710,142.7 L1728,154.3 L1746,164.9 L1764,171.3 L1782,171.9 L1800,167.0 L1818,159.2 L1836,151.3 L1854,145.6 L1872,143.1 L1890,142.8 L1908,143.1 L1926,142.3 L1944,140.1 L1962,137.5 L1980,136.5 L1998,139.2 L2016,146.0 L2034,155.8 L2052,165.7 L2070,172.5 L2088,173.6 L2106,168.5 L2124,159.0 L2142,148.0 L2160,138.9 L2178,134.2 L2196,134.1 L2214,137.3 L2232,141.4 L2250,144.5 L2268,146.0 L2286,146.4 L2304,147.6 L2322,151.0 L2340,156.8 L2358,163.7 L2376,169.2 L2394,170.6 L2412,166.5 L2430,157.3 L2448,145.7 L2466,135.1 L2484,128.7 L2502,128.1 L2520,133.0 L2538,140.8 L2556,148.7 L2574,154.4 L2592,156.9 L2610,157.2 L2628,156.9 L2646,157.7 L2664,159.9 L2682,162.5 L2700,163.5 L2718,160.8 L2736,154.0 L2754,144.2 L2772,134.3 L2790,127.5 L2808,126.4 L2826,131.5 L2844,141.0 L2862,152.0 L2880,161.1 L2880,320 L0,320 Z" fill="url(#fxg4)"/><path class="fx-line" d="M0,161.1 L18,165.8 L36,165.9 L54,162.7 L72,158.6 L90,155.5 L108,154.0 L126,153.6 L144,152.4 L162,149.0 L180,143.2 L198,136.3 L216,130.8 L234,129.4 L252,133.5 L270,142.7 L288,154.3 L306,164.9 L324,171.3 L342,171.9 L360,167.0 L378,159.2 L396,151.3 L414,145.6 L432,143.1 L450,142.8 L468,143.1 L486,142.3 L504,140.1 L522,137.5 L540,136.5 L558,139.2 L576,146.0 L594,155.8 L612,165.7 L630,172.5 L648,173.6 L666,168.5 L684,159.0 L702,148.0 L720,138.9 L738,134.2 L756,134.1 L774,137.3 L792,141.4 L810,144.5 L828,146.0 L846,146.4 L864,147.6 L882,151.0 L900,156.8 L918,163.7 L936,169.2 L954,170.6 L972,166.5 L990,157.3 L1008,145.7 L1026,135.1 L1044,128.7 L1062,128.1 L1080,133.0 L1098,140.8 L1116,148.7 L1134,154.4 L1152,156.9 L1170,157.2 L1188,156.9 L1206,157.7 L1224,159.9 L1242,162.5 L1260,163.5 L1278,160.8 L1296,154.0 L1314,144.2 L1332,134.3 L1350,127.5 L1368,126.4 L1386,131.5 L1404,141.0 L1422,152.0 L1440,161.1 L1458,165.8 L1476,165.9 L1494,162.7 L1512,158.6 L1530,155.5 L1548,154.0 L1566,153.6 L1584,152.4 L1602,149.0 L1620,143.2 L1638,136.3 L1656,130.8 L1674,129.4 L1692,133.5 L1710,142.7 L1728,154.3 L1746,164.9 L1764,171.3 L1782,171.9 L1800,167.0 L1818,159.2 L1836,151.3 L1854,145.6 L1872,143.1 L1890,142.8 L1908,143.1 L1926,142.3 L1944,140.1 L1962,137.5 L1980,136.5 L1998,139.2 L2016,146.0 L2034,155.8 L2052,165.7 L2070,172.5 L2088,173.6 L2106,168.5 L2124,159.0 L2142,148.0 L2160,138.9 L2178,134.2 L2196,134.1 L2214,137.3 L2232,141.4 L2250,144.5 L2268,146.0 L2286,146.4 L2304,147.6 L2322,151.0 L2340,156.8 L2358,163.7 L2376,169.2 L2394,170.6 L2412,166.5 L2430,157.3 L2448,145.7 L2466,135.1 L2484,128.7 L2502,128.1 L2520,133.0 L2538,140.8 L2556,148.7 L2574,154.4 L2592,156.9 L2610,157.2 L2628,156.9 L2646,157.7 L2664,159.9 L2682,162.5 L2700,163.5 L2718,160.8 L2736,154.0 L2754,144.2 L2772,134.3 L2790,127.5 L2808,126.4 L2826,131.5 L2844,141.0 L2862,152.0 L2880,161.1" stroke="#A78BFA" stroke-opacity=".65"/></svg></div></div></div>
<!-- ===================== LOGIN GATE ===================== -->
<div class="login-gate" id="loginGate">
<div class="login-card">
<div class="badge-icon"><svg viewBox="0 0 24 24"><path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/><circle cx="12" cy="12" r="3"/></svg></div>
<h1>Admin Portal</h1>
<div class="sub">REX Insurance · Enter the admin passcode to continue</div>
<div class="login-error" id="loginError"></div>
<div class="field"><label>Your name</label><input type="text" id="loginName" placeholder="e.g. Ibrahim Musa"></div>
<div class="field"><label>Passcode</label><div class="pw-wrap">
  <input type="password" id="loginPasscode" placeholder="Enter passcode" autocomplete="current-password">
  <button type="button" class="pw-toggle" id="pwToggle" aria-label="Show or hide passcode">Show</button>
</div></div>
<button class="btn-primary" id="loginBtn" style="width:100%;">Log In</button>
<nav class="portal-switch" aria-label="Switch portal"><span class="ps-label">Switch portal</span><a href="./security-portal.html">Security Portal</a><a href="./frontdesk-portal.html">Front Desk Portal</a></nav>
</div>
</div>
<!-- ===================== APP SHELL ===================== -->
<div class="app-shell" id="appShell">
<div class="conn-banner" id="connBanner">Connecting to server — this can take up to a minute on first load...</div>
<div class="top-bar">
<div class="top-left">
<div class="badge-icon"><svg viewBox="0 0 24 24"><path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/><circle cx="12" cy="12" r="3"/></svg></div>
<div class="titles"><div class="company">REX Insurance</div><div class="portal">Admin Portal</div></div>
</div>
<nav class="portal-switch" aria-label="Switch portal"><span class="ps-label">Switch to</span><a href="./security-portal.html">Security</a><a href="./frontdesk-portal.html">Front Desk</a></nav>
<div class="top-right">
<span class="user-chip" id="userChip"></span>
<div id="clock"></div>
<button class="logout-btn" id="logoutBtn">Log Out</button>
</div>
</div>
<div class="shell">
<div class="sidebar">
<button class="nav-item active" data-view="dashboard"><svg viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="9" rx="1.5"/><rect x="14" y="3" width="7" height="5" rx="1.5"/><rect x="14" y="12" width="7" height="9" rx="1.5"/><rect x="3" y="16" width="7" height="5" rx="1.5"/></svg>Dashboard</button>
<button class="nav-item" data-view="users"><svg viewBox="0 0 24 24"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/></svg>Users & Roles</button>
<button class="nav-item" data-view="logs"><svg viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M9 13h6M9 17h6"/></svg>Visitor Logs</button>
<button class="nav-item" data-view="sessions"><svg viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="14" rx="2"/><path d="M8 21h8M12 17v4"/></svg>Session Control</button>
<button class="nav-item" data-view="reports"><svg viewBox="0 0 24 24"><path d="M3 3v18h18"/><path d="M7 15v3M12 11v7M17 7v11"/></svg>Reports</button>
</div>
<div class="content">
<!-- ===== DASHBOARD ===== -->
<div class="view active" id="view-dashboard">
<div class="view-title">Dashboard</div>
<div class="view-sub">Live overview of visitor activity and system performance</div>
<div class="stats-row">
<div class="stat-card"><div class="num" id="statToday">0</div><div class="label">Visitors today</div></div>
<div class="stat-card"><div class="num" id="statInside">0</div><div class="label">Currently inside</div></div>
<div class="stat-card"><div class="num" id="statPending">0</div><div class="label">Pending approvals</div></div>
<div class="stat-card"><div class="num" id="statMonth">0</div><div class="label">Visitors this month</div></div>
</div>
<div class="two-col">
<div class="panel"><div class="panel-header"><div><h2>Staff Performance</h2><span class="sub">Visits handled this week, by host</span></div></div><div id="perfChart"></div></div>
<div class="panel"><div class="panel-header"><div><h2>Recent Activity</h2><span class="sub">Latest system events</span></div></div><div id="activityFeed" style="padding-bottom:16px;"></div></div>
</div>
<div class="charts-row">
<div class="panel"><div class="panel-header"><div><h2>Visit Status</h2><span class="sub">All visits by current status</span></div></div><div class="chart-body" id="chartStatus"></div></div>
<div class="panel"><div class="panel-header"><div><h2>Visits per Day</h2><span class="sub">Last 7 days</span></div></div><div class="chart-body" id="chartDaily"></div></div>
<div class="panel"><div class="panel-header"><div><h2>Visits by Department</h2><span class="sub">All time</span></div></div><div class="chart-body" id="chartDept"></div></div>
</div>
</div>
<!-- ===== USERS & ROLES ===== -->
<div class="view" id="view-users">
<div class="view-title">Users & Roles</div>
<div class="view-sub">Staff directory — a record only, not connected to portal login</div>
<div class="panel">
<div class="panel-header"><div><h2>Staff Roster</h2><span class="sub" id="usersCount">0 members</span></div>
<button class="btn-add" id="addUserBtn"><svg viewBox="0 0 24 24"><path d="M12 5v14M5 12h14"/></svg>Add Staff Member</button>
</div>
<table><thead><tr><th>Name</th><th>Role</th></tr></thead><tbody id="usersTableBody"></tbody></table>
</div>
</div>
<!-- ===== VISITOR LOGS ===== -->
<div class="view" id="view-logs">
<div class="view-title">Visitor Logs</div>
<div class="view-sub">Complete historical record of every visit ever logged in the system</div>
<div class="panel">
<div class="panel-header">
<div><h2>All Visits</h2><span class="sub">Loaded in batches — search applies across the full history</span></div>
<div class="header-actions">
<span class="logs-count-chip" id="logsCountChip">0 of 0 loaded</span>
<div class="search-row"><svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/></svg><input type="text" id="logsSearch" placeholder="Search visitor, host, or department..."></div>
</div>
</div>
<table><thead><tr><th>Visitor</th><th>Department</th><th>Host</th><th>Check-in</th><th>Check-out</th><th>Status</th></tr></thead><tbody id="logsTableBody"></tbody></table>
<div id="logsFooter"></div>
</div>
</div>
<!-- ===== SESSION CONTROL ===== -->
<div class="view" id="view-sessions">
<div class="view-title">Session Control</div>
<div class="view-sub">See who's logged in and manage portal passcodes</div>
<div class="panel">
<div class="panel-header"><div><h2>Active Sessions</h2><span class="sub" id="sessionsCount">0 active</span></div></div>
<div id="sessionsList"></div>
</div>
<div class="panel">
<div class="panel-header"><div><h2>Passcodes</h2><span class="sub">Change the login passcode for any portal</span></div></div>
<div id="passcodeList"></div>
</div>
<div class="panel">
<div class="panel-header"><div><h2>Login History</h2><span class="sub">Most recent 50 logins</span></div></div>
<table><thead><tr><th>Name</th><th>Portal</th><th>Logged in</th><th>Logged out</th></tr></thead><tbody id="historyTableBody"></tbody></table>
</div>
</div>
<!-- ===== REPORTS ===== -->
<div class="view" id="view-reports">
<div class="view-title">Reports</div>
<div class="view-sub">Export visitor logs and analytics for compliance and record-keeping</div>
<div class="report-grid">
<div class="report-card"><div class="r-icon"><svg viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg></div><div><div class="r-title">Daily Visitor Log</div><div class="r-sub">All check-ins and check-outs for today</div><div class="report-actions"><button class="btn-tiny primary" data-report="Daily Visitor Log" data-format="PDF">Export PDF</button><button class="btn-tiny" data-report="Daily Visitor Log" data-format="Excel">Export Excel</button></div></div></div>
<div class="report-card"><div class="r-icon"><svg viewBox="0 0 24 24"><path d="M3 3v18h18"/><path d="M7 15v3M12 11v7M17 7v11"/></svg></div><div><div class="r-title">Monthly Visitor Count</div><div class="r-sub">Total visits broken down by month</div><div class="report-actions"><button class="btn-tiny primary" data-report="Monthly Visitor Count" data-format="PDF">Export PDF</button><button class="btn-tiny" data-report="Monthly Visitor Count" data-format="Excel">Export Excel</button></div></div></div>
<div class="report-card"><div class="r-icon"><svg viewBox="0 0 24 24"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/></svg></div><div><div class="r-title">Staff Visit Frequency</div><div class="r-sub">Which hosts receive the most visitors</div><div class="report-actions"><button class="btn-tiny primary" data-report="Staff Visit Frequency" data-format="PDF">Export PDF</button><button class="btn-tiny" data-report="Staff Visit Frequency" data-format="Excel">Export Excel</button></div></div></div>
<div class="report-card"><div class="r-icon"><svg viewBox="0 0 24 24"><path d="M9 12 11 14 15 10"/><circle cx="12" cy="12" r="9"/></svg></div><div><div class="r-title">Security & Front Desk Performance</div><div class="r-sub">Registration speed and approval turnaround</div><div class="report-actions"><button class="btn-tiny primary" data-report="Security & Front Desk Performance" data-format="PDF">Export PDF</button><button class="btn-tiny" data-report="Security & Front Desk Performance" data-format="Excel">Export Excel</button></div></div></div>
</div>
</div>
</div>
</div>
</div>
<!-- ===== Add Staff Modal ===== -->
<div class="modal-overlay" id="userModalOverlay">
<div class="modal">
<h3>Add Staff Member</h3>
<div class="modal-sub">Add to the staff roster directory.</div>
<div class="field"><label>Full name</label><input type="text" id="userName"><span class="error-text">Name is required.</span></div>
<div class="field"><label>Role</label><select id="userRole"><option value="security">Security Officer</option><option value="frontdesk">Front Desk Officer</option><option value="admin">Admin</option></select></div>
<div class="modal-actions"><button class="btn-secondary" id="cancelUser">Cancel</button><button class="btn-primary" id="saveUser">Save</button></div>
</div>
</div>
<!-- ===== Change Passcode Modal ===== -->
<div class="modal-overlay" id="passcodeModalOverlay">
<div class="modal">
<h3 id="passcodeModalTitle">Change Passcode</h3>
<div class="modal-sub">This immediately changes login access for that portal.</div>
<div class="field"><label>New passcode</label><input type="password" id="newPasscodeInput" placeholder="At least 4 characters" autocomplete="new-password"><span class="error-text">Passcode must be at least 4 characters.</span></div>
<div class="modal-actions"><button class="btn-secondary" id="cancelPasscode">Cancel</button><button class="btn-primary" id="savePasscode">Update Passcode</button></div>
</div>
</div>
<!-- ===== AI Guide ===== -->
<button class="guide-fab" id="guideFab" aria-label="Open help guide"><svg viewBox="0 0 24 24"><path d="M12 18h.01M9.09 9a3 3 0 1 1 5.83 1c0 2-3 2-3 4"/><circle cx="12" cy="12" r="9"/></svg></button>
<div class="guide-panel" id="guidePanel">
<div class="guide-head"><span class="t">Admin Portal Guide</span><button class="close-guide" id="closeGuide">&times;</button></div>
<div class="guide-body" id="guideBody"><div class="guide-msg bot">Hi! Ask me about managing users, checking the dashboard, session control, or reports.</div></div>
<div class="guide-quick" id="guideQuick">
<button data-q="How do I change a portal's passcode?">Change a passcode</button>
<button data-q="How do the visitor logs work?">Visitor logs</button>
</div>
<div class="guide-input-row"><input type="text" id="guideInput" placeholder="Ask a question..."><button id="guideSend"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 2 11 13M22 2l-7 20-4-9-9-4 20-7z"/></svg></button></div>
</div>
<div class="toast" id="toast"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="m8 12 3 3 5-6"/></svg><span id="toastText"></span></div>
<script>
const API_BASE = "https://rex-vms-backend.onrender.com/api";
const PORTAL = "admin";
const TOKEN_KEY = "rex_vms_token_admin";
const NAME_KEY = "rex_vms_name_admin";
let authToken = localStorage.getItem(TOKEN_KEY);
let userName = localStorage.getItem(NAME_KEY);

async function api(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, { ...options, headers: { "Content-Type": "application/json", ...(authToken ? { Authorization: `Bearer ${authToken}` } : {}), ...(options.headers || {}) } });
  if (res.status === 401) { clearSession(); showLoginGate(); throw new Error("Session expired. Please log in again."); }
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error || "Something went wrong.");
  return data;
}
function clearSession() { localStorage.removeItem(TOKEN_KEY); localStorage.removeItem(NAME_KEY); authToken = null; userName = null; stopSessionsPolling(); }
function showLoginGate() { document.getElementById("loginGate").style.display = "flex"; document.getElementById("appShell").classList.remove("ready"); }
function showAppShell() { document.getElementById("loginGate").style.display = "none"; document.getElementById("appShell").classList.add("ready"); document.getElementById("userChip").textContent = userName; initPortal(); }

async function warmUp() {
  const banner = document.getElementById("connBanner");
  banner.classList.add("show");
  try { await fetch(`${API_BASE}/ping`); } catch (e) {}
  banner.classList.remove("show");
}

(async function boot() {
  warmUp();
  if (authToken) {
    try { const v = await api("/auth/verify"); if (v.valid && v.portal === PORTAL) { userName = v.name; showAppShell(); return; } } catch (e) {}
  }
  showLoginGate();
})();

async function doLogin() {
  const btn = document.getElementById("loginBtn");
  const name = document.getElementById("loginName").value.trim();
  const passcode = document.getElementById("loginPasscode").value;
  const errBox = document.getElementById("loginError");
  errBox.classList.remove("show");
  if (!name || !passcode) {
    errBox.textContent = "Enter your name and the passcode.";
    errBox.classList.add("show");
    return;
  }
  btn.disabled = true; btn.textContent = "Logging in...";
  try {
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ portal: PORTAL, passcode, name })
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(data.error || "Server is waking up. Wait a few seconds and try again.");
    authToken = data.token; userName = data.name;
    localStorage.setItem(TOKEN_KEY, authToken);
    localStorage.setItem(NAME_KEY, userName);
    document.getElementById("loginPasscode").value = "";
    showAppShell();
  } catch (e) {
    errBox.textContent = e.message.includes("fetch") ? "Can't reach the server. Check your connection." : e.message;
    errBox.classList.add("show");
  } finally {
    btn.disabled = false; btn.textContent = "Log In";
  }
}
document.getElementById("loginBtn").addEventListener("click", doLogin);
["loginName", "loginPasscode"].forEach(id =>
  document.getElementById(id).addEventListener("keydown", e => { if (e.key === "Enter") doLogin(); })
);
document.getElementById("pwToggle").addEventListener("click", () => {
  const input = document.getElementById("loginPasscode");
  const show = input.type === "password";
  input.type = show ? "text" : "password";
  document.getElementById("pwToggle").textContent = show ? "Hide" : "Show";
});

document.getElementById("logoutBtn").addEventListener("click", async () => {
  try { await api("/auth/logout", { method: "POST" }); } catch (e) {}
  clearSession(); showLoginGate();
});

function updateClock() { document.getElementById("clock").textContent = new Date().toLocaleString("en-US", { weekday: "short", hour: "2-digit", minute: "2-digit", second: "2-digit" }); }
updateClock(); setInterval(updateClock, 1000);

let portalReady = false;
function initPortal() {
  if (portalReady) {
    loadDashboard(); loadRoster(); loadLogs(true); loadSessions(true);
    loadPasscodes(); loadHistory(); startSessionsPolling();
    return;
  }
  portalReady = true;
  document.querySelectorAll(".nav-item").forEach(item => {
    item.addEventListener("click", () => {
      document.querySelectorAll(".nav-item").forEach(i => i.classList.remove("active"));
      document.querySelectorAll(".view").forEach(v => v.classList.remove("active"));
      item.classList.add("active");
      document.getElementById("view-" + item.dataset.view).classList.add("active");
    });
  });
  loadDashboard();
  loadRoster();
  loadLogs(true);
  loadSessions(true);
  loadPasscodes();
  loadHistory();
  startSessionsPolling();
  document.getElementById("addUserBtn").addEventListener("click", () => {
    document.getElementById("userName").value = "";
    document.getElementById("userRole").value = "security";
    clearFieldError("userName");
    document.getElementById("userModalOverlay").classList.add("show");
  });
  document.getElementById("cancelUser").addEventListener("click", () => document.getElementById("userModalOverlay").classList.remove("show"));
  document.getElementById("saveUser").addEventListener("click", saveUser);
  document.getElementById("logsSearch").addEventListener("input", () => loadLogs(true));
  document.getElementById("cancelPasscode").addEventListener("click", () => document.getElementById("passcodeModalOverlay").classList.remove("show"));
  document.getElementById("savePasscode").addEventListener("click", savePasscodeChange);
  document.querySelectorAll("[data-report]").forEach(btn => {
    btn.addEventListener("click", () => exportReport(btn.dataset.report, btn.dataset.format, btn));
  });
}

function clearFieldError(id) { document.getElementById(id).classList.remove("invalid"); document.getElementById(id).closest(".field").classList.remove("error"); }
function markInvalid(id) { document.getElementById(id).classList.add("invalid"); document.getElementById(id).closest(".field").classList.add("error"); }

// ===== Dashboard =====
async function loadDashboard() {
  try {
    const s = await api("/admin/stats");
    document.getElementById("statToday").textContent = s.visitorsToday;
    document.getElementById("statInside").textContent = s.currentlyInside;
    document.getElementById("statPending").textContent = s.pendingApprovals;
    document.getElementById("statMonth").textContent = s.visitorsThisMonth;
    const max = Math.max(1, ...s.staffPerformance.map(p => p.visits));
    document.getElementById("perfChart").innerHTML = s.staffPerformance.map(p => `
      <div class="bar-row"><div class="bar-label">${escapeHtml(p.host)}</div><div class="bar-track"><div class="bar-fill" style="width:${(p.visits / max * 100).toFixed(0)}%"></div></div><div class="bar-num">${p.visits}</div></div>
    `).join("") || `<div style="font-size:13px;color:var(--text-tertiary);">No visit data yet this week.</div>`;
    document.getElementById("activityFeed").innerHTML = s.recentActivity.map(a => `
      <div style="padding:10px 0; border-bottom:1px solid var(--border); font-size:13px;">
        <div>${escapeHtml(a.visitor_name)} — ${a.status.replace("-"," ")} (host: ${escapeHtml(a.host)})</div>
        <div style="font-size:11px; color:var(--text-tertiary); margin-top:2px;">${new Date(a.created_at).toLocaleString("en-US",{month:"short",day:"numeric",hour:"2-digit",minute:"2-digit"})}</div>
      </div>
    `).join("") || `<div style="font-size:13px;color:var(--text-tertiary);">No activity yet.</div>`;
  } catch (e) { showToast(e.message, true); }
  loadCharts();
}

// ===== Users & Roles (roster) =====
const roleLabels = { security: "Security Officer", frontdesk: "Front Desk Officer", admin: "Admin" };
async function loadRoster() {
  try {
    const roster = await api("/admin/roster");
    document.getElementById("usersCount").textContent = `${roster.length} member${roster.length !== 1 ? "s" : ""}`;
    const body = document.getElementById("usersTableBody");
    if (roster.length === 0) { body.innerHTML = `<tr class="empty-row"><td colspan="2">No staff added yet.</td></tr>`; return; }
    body.innerHTML = roster.map(u => `
      <tr>
        <td><div class="name-cell">${escapeHtml(u.name)}</div><div class="sub-cell">ID #${String(u.id).padStart(3,"0")}</div></td>
        <td><span class="role-pill ${u.role}">${roleLabels[u.role]}</span></td>
      </tr>
    `).join("");
  } catch (e) { showToast(e.message, true); }
}
async function saveUser() {
  const name = document.getElementById("userName").value.trim();
  const role = document.getElementById("userRole").value;
  clearFieldError("userName");
  if (!/^[A-Za-z\s'-]{2,}$/.test(name)) { markInvalid("userName"); return; }
  try {
    await api("/admin/roster", { method: "POST", body: JSON.stringify({ name, role }) });
    document.getElementById("userModalOverlay").classList.remove("show");
    loadRoster();
    showToast(`${name} was added to the roster.`);
  } catch (e) { showToast(e.message, true); }
}

// ===== Dashboard charts (pure HTML/CSS) =====
const CHART_COLORS = ["#6B4C6E", "#1E7B4D", "#B8792A", "#3B82A0", "#B3261E", "#8A93A3", "#9B6BA0", "#5C9E6E"];
const STATUS_COLORS = { "checked-out": "#1E7B4D", "with-host": "#6B4C6E", approved: "#3B82A0", pending: "#B8792A", hold: "#9B8A5C", rejected: "#B3261E" };
function donutChart(el, items) {
  const total = items.reduce((a, i) => a + i.value, 0);
  if (!total) { el.innerHTML = `<div style="font-size:13px;color:var(--text-tertiary);">No visit data yet.</div>`; return; }
  let acc = 0;
  const stops = items.map(i => { const a = acc / total * 100; acc += i.value; return `${i.color} ${a}% ${acc / total * 100}%`; }).join(", ");
  el.innerHTML = `<div class="donut-wrap"><div class="donut" data-total="${total}" style="background:conic-gradient(${stops});"></div><div class="legend">${items.map(i => `<div><i style="background:${i.color}"></i>${escapeHtml(i.label)}<b>${i.value}</b></div>`).join("")}</div></div>`;
}
async function loadCharts() {
  try {
    const visits = await fetchAllVisits();
    const st = {}; visits.forEach(v => st[v.status] = (st[v.status] || 0) + 1);
    donutChart(document.getElementById("chartStatus"), Object.entries(st).sort((a, b) => b[1] - a[1]).map(([k, n], i) => ({ label: fmtStatus(k), value: n, color: STATUS_COLORS[k] || CHART_COLORS[i % CHART_COLORS.length] })));
    const days = [];
    for (let i = 6; i >= 0; i--) { const d = new Date(); d.setHours(0, 0, 0, 0); d.setDate(d.getDate() - i); days.push({ d, n: 0 }); }
    visits.forEach(v => { const t = new Date(v.checkin); t.setHours(0, 0, 0, 0); const x = days.find(y => y.d.getTime() === t.getTime()); if (x) x.n++; });
    const max = Math.max(1, ...days.map(x => x.n));
    document.getElementById("chartDaily").innerHTML = `<div class="col-chart">${days.map(x => `<div class="col"><div class="v">${x.n}</div><div class="b" style="height:${(x.n / max * 100).toFixed(0)}%"></div><div class="d">${x.d.toLocaleDateString("en-GB", { weekday: "short" })}</div></div>`).join("")}</div>`;
    const dp = {}; visits.forEach(v => dp[v.department] = (dp[v.department] || 0) + 1);
    let list = Object.entries(dp).sort((a, b) => b[1] - a[1]);
    if (list.length > 6) { const rest = list.slice(5).reduce((a, [, n]) => a + n, 0); list = list.slice(0, 5).concat([["Other", rest]]); }
    donutChart(document.getElementById("chartDept"), list.map(([k, n], i) => ({ label: k, value: n, color: CHART_COLORS[i % CHART_COLORS.length] })));
  } catch (e) { showToast(e.message, true); }
}

// ===== Report export (real data) =====
async function fetchAllVisits() {
  let all = [], offset = 0, total = Infinity;
  while (offset < total) {
    const data = await api(`/admin/visits?search=&limit=100&offset=${offset}`);
    total = data.total;
    if (!data.rows.length) break;
    all = all.concat(data.rows);
    offset += data.rows.length;
  }
  return all;
}
const fmtDT = d => d ? new Date(d).toLocaleString("en-GB", { day: "2-digit", month: "short", year: "numeric", hour: "2-digit", minute: "2-digit" }) : "—";
const fmtStatus = s => String(s || "").replace("-", " ");
const fmtMins = m => m == null ? "—" : (m >= 60 ? `${Math.floor(m / 60)}h ${Math.round(m % 60)}m` : `${Math.round(m)}m`);

function buildReport(name, visits) {
  if (name === "Daily Visitor Log") {
    const t = new Date(); t.setHours(0, 0, 0, 0);
    const rows = visits.filter(v => new Date(v.checkin) >= t).sort((a, b) => new Date(a.checkin) - new Date(b.checkin));
    return { subtitle: `Visits for ${new Date().toLocaleDateString("en-GB", { dateStyle: "full" })}`,
      head: ["Visitor", "Department", "Host", "Purpose", "Check-in", "Check-out", "Status"],
      rows: rows.map(v => [v.visitor_name, v.department, v.host, v.purpose, fmtDT(v.checkin), fmtDT(v.checkout), fmtStatus(v.status)]) };
  }
  if (name === "Monthly Visitor Count") {
    const m = {};
    visits.forEach(v => { const d = new Date(v.checkin); const k = d.getFullYear() * 100 + d.getMonth(); (m[k] = m[k] || { label: d.toLocaleString("en-GB", { month: "long", year: "numeric" }), n: 0 }).n++; });
    const keys = Object.keys(m).sort((a, b) => b - a);
    return { subtitle: "Total visits per month, all time",
      head: ["Month", "Total Visits"], rows: keys.map(k => [m[k].label, m[k].n]) };
  }
  if (name === "Staff Visit Frequency") {
    const h = {};
    visits.forEach(v => { const x = h[v.host] = h[v.host] || { n: 0, dept: v.department }; x.n++; });
    return { subtitle: "Visitors received per host, all time",
      head: ["Host", "Department", "Visits"], rows: Object.entries(h).sort((a, b) => b[1].n - a[1].n).map(([k, x]) => [k, x.dept, x.n]) };
  }
  // Security & Front Desk Performance
  const by = st => visits.filter(v => v.status === st).length;
  const durs = visits.filter(v => v.checkout && v.checkin).map(v => (new Date(v.checkout) - new Date(v.checkin)) / 60000).filter(x => x >= 0);
  const avg = durs.length ? durs.reduce((a, b) => a + b, 0) / durs.length : null;
  const dept = {};
  visits.forEach(v => { const x = dept[v.department] = dept[v.department] || { n: 0, d: [] }; x.n++; if (v.checkout) { const m = (new Date(v.checkout) - new Date(v.checkin)) / 60000; if (m >= 0) x.d.push(m); } });
  const rows = [["Total visits", visits.length, ""], ["Checked out", by("checked-out"), ""], ["Approved / with host", by("approved") + by("with-host"), ""],
    ["Pending / on hold", by("pending") + by("hold"), ""], ["Rejected", by("rejected"), ""], ["Average visit duration", fmtMins(avg), "check-in to check-out"]];
  Object.entries(dept).sort((a, b) => b[1].n - a[1].n).forEach(([k, x]) => rows.push([`Dept: ${k}`, x.n, x.d.length ? `avg ${fmtMins(x.d.reduce((a, b) => a + b, 0) / x.d.length)}` : "—"]));
  return { subtitle: "Visit outcomes and time on site, all time", head: ["Measure", "Value", "Note"], rows };
}

function downloadBlob(content, mime, filename) {
  const url = URL.createObjectURL(new Blob([content], { type: mime }));
  const a = document.createElement("a"); a.href = url; a.download = filename; document.body.appendChild(a); a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 2000);
}
function printPdf(title, r) {
  const f = document.createElement("iframe");
  f.style.cssText = "position:fixed;right:0;bottom:0;width:0;height:0;border:0;";
  document.body.appendChild(f);
  const th = r.head.map(h => `<th>${escapeHtml(h)}</th>`).join("");
  const tr = r.rows.map(row => `<tr>${row.map(c => `<td>${escapeHtml(String(c ?? ""))}</td>`).join("")}</tr>`).join("") || `<tr><td colspan="${r.head.length}">No records.</td></tr>`;
  f.contentDocument.open();
  f.contentDocument.write(`<html><head><title>${escapeHtml(title)}</title><style>body{font-family:Arial,sans-serif;padding:24px;color:#111}h1{font-size:18px;margin:0}p{font-size:12px;color:#555;margin:4px 0 16px}table{width:100%;border-collapse:collapse;font-size:11px}th,td{border:1px solid #ccc;padding:6px 8px;text-align:left}th{background:#eee}</style></head><body><h1>Rex Insurance Ltd — ${escapeHtml(title)}</h1><p>${escapeHtml(r.subtitle)} · Generated ${new Date().toLocaleString("en-GB")}</p><table><thead><tr>${th}</tr></thead><tbody>${tr}</tbody></table></body></html>`);
  f.contentDocument.close();
  setTimeout(() => { f.contentWindow.focus(); f.contentWindow.print(); setTimeout(() => f.remove(), 1500); }, 300);
}
async function exportReport(name, format, btn) {
  const label = btn.textContent; btn.disabled = true; btn.textContent = "Preparing…";
  try {
    const r = buildReport(name, await fetchAllVisits());
    const stamp = new Date().toISOString().slice(0, 10);
    const base = `${name.replace(/[^A-Za-z0-9]+/g, "_")}_${stamp}`;
    if (format === "PDF") { printPdf(name, r); showToast(`${name}: choose "Save as PDF" in the print window.`); }
    else {
      const th = r.head.map(h => `<th>${escapeHtml(h)}</th>`).join("");
      const tr = r.rows.map(row => `<tr>${row.map(c => `<td>${escapeHtml(String(c ?? ""))}</td>`).join("")}</tr>`).join("");
      const html = `<html xmlns:x="urn:schemas-microsoft-com:office:excel"><head><meta charset="utf-8"></head><body><table border="1"><thead><tr>${th}</tr></thead><tbody>${tr}</tbody></table></body></html>`;
      downloadBlob("\ufeff" + html, "application/vnd.ms-excel", `${base}.xls`);
      showToast(`${name} exported (${r.rows.length} row${r.rows.length !== 1 ? "s" : ""}).`);
    }
  } catch (e) { showToast(e.message, true); }
  finally { btn.disabled = false; btn.textContent = label; }
}

// ===== Visitor Logs (batched) =====
const BATCH_SIZE = 20;
let logsOffset = 0, logsTotal = 0;
async function loadLogs(reset) {
  if (reset) { logsOffset = 0; document.getElementById("logsTableBody").innerHTML = ""; }
  const q = document.getElementById("logsSearch").value.trim();
  try {
    const data = await api(`/admin/visits?search=${encodeURIComponent(q)}&limit=${BATCH_SIZE}&offset=${logsOffset}`);
    logsTotal = data.total;
    const body = document.getElementById("logsTableBody");
    if (reset && data.rows.length === 0) { body.innerHTML = `<tr class="empty-row"><td colspan="6">No visits match your search.</td></tr>`; }
    else {
      body.insertAdjacentHTML("beforeend", data.rows.map(v => `
        <tr>
          <td><div class="name-cell">${escapeHtml(v.visitor_name)}</div></td>
          <td>${escapeHtml(v.department)}</td>
          <td>${escapeHtml(v.host)}</td>
          <td>${formatDT(v.checkin)}</td>
          <td>${formatDT(v.checkout)}</td>
          <td><span class="visit-status-pill ${v.status}"><span class="dot"></span>${v.status.replace("-"," ")}</span></td>
        </tr>
      `).join(""));
    }
    logsOffset += data.rows.length;
    document.getElementById("logsCountChip").textContent = `${logsOffset} of ${logsTotal} loaded`;
    const footer = document.getElementById("logsFooter");
    if (logsOffset < logsTotal) {
      footer.innerHTML = `<div class="load-more-row"><button class="btn-load-more" id="loadMoreBtn">Load ${BATCH_SIZE} more (${logsTotal - logsOffset} remaining)</button></div>`;
      document.getElementById("loadMoreBtn").addEventListener("click", () => loadLogs(false));
    } else if (logsTotal > 0) {
      footer.innerHTML = `<div class="logs-fully-loaded">All ${logsTotal} records loaded — this is the complete history since the system began.</div>`;
    } else { footer.innerHTML = ""; }
  } catch (e) { showToast(e.message, true); }
}
function formatDT(str) { if (!str) return "—"; const d = new Date(str); return isNaN(d) ? "—" : d.toLocaleString("en-US",{month:"short",day:"numeric",year:"numeric",hour:"numeric",minute:"2-digit"}); }

// ============================================================
// Session Control — live-polled the same way Front Desk polls
// the visit board: 25s baseline, backs off by 5s each cycle with
// no change, capped at 110s, resets to 25s the instant something
// changes (including our own force-logout action). This is what
// makes Force Logout / another portal's log-out show up here
// without needing a manual refresh.
// ============================================================
const SESSIONS_POLL_MIN = 25000, SESSIONS_POLL_STEP = 5000, SESSIONS_POLL_MAX = 110000;
let sessionsPollInterval = SESSIONS_POLL_MIN;
let sessionsPollTimer = null;
let lastSessionsSnapshotKey = "";

function sessionsSnapshotKey(list) {
  return list.map(s => `${s.id}:${s.last_seen}`).join("|");
}

function startSessionsPolling() {
  stopSessionsPolling();
  sessionsPollTimer = setTimeout(sessionsPollTick, sessionsPollInterval);
}
function stopSessionsPolling() { if (sessionsPollTimer) clearTimeout(sessionsPollTimer); sessionsPollTimer = null; }

async function sessionsPollTick() {
  const changed = await loadSessions(false);
  // Login History reflects the same logout/force-logout events, so refresh it
  // on the same cadence rather than leaving it to go stale too.
  loadHistory();
  sessionsPollInterval = changed ? SESSIONS_POLL_MIN : Math.min(sessionsPollInterval + SESSIONS_POLL_STEP, SESSIONS_POLL_MAX);
  sessionsPollTimer = setTimeout(sessionsPollTick, sessionsPollInterval);
}

// Returns true if the fetched session list differs from what's on screen.
// isInitial suppresses the "changed" signal on first load so the very
// first poll tick doesn't treat "went from nothing to something" as a change.
async function loadSessions(isInitial) {
  try {
    const sessions = await api("/admin/sessions");
    const key = sessionsSnapshotKey(sessions);
    const changed = key !== lastSessionsSnapshotKey;
    lastSessionsSnapshotKey = key;

    document.getElementById("sessionsCount").textContent = `${sessions.length} active`;
    const list = document.getElementById("sessionsList");
    if (sessions.length === 0) {
      list.innerHTML = `<div style="font-size:13px;color:var(--text-tertiary);padding:12px 0;">No one is currently logged in.</div>`;
      return isInitial ? false : changed;
    }
    list.innerHTML = sessions.map(s => `
      <div class="session-card">
        <div><div class="s-name">${escapeHtml(s.display_name)} <span class="role-pill ${s.portal}" style="margin-left:6px;">${s.portal}</span></div>
        <div class="s-meta">Logged in ${new Date(s.created_at).toLocaleString("en-US",{month:"short",day:"numeric",hour:"2-digit",minute:"2-digit"})} · Last seen ${new Date(s.last_seen).toLocaleTimeString("en-US",{hour:"2-digit",minute:"2-digit"})}</div></div>
      </div>
    `).join("");
    return isInitial ? false : changed;
  } catch (e) { showToast(e.message, true); return false; }
}
// ===== Passcodes =====
let passcodeTargetPortal = null;
function loadPasscodes() {
  const portals = ["security", "frontdesk", "admin"];
  document.getElementById("passcodeList").innerHTML = portals.map(p => `
    <div class="concurrency-row">
      <div class="c-portal">${p}</div>
      <button class="icon-btn" data-changepass="${p}">Change Passcode</button>
    </div>
  `).join("");
  document.querySelectorAll("[data-changepass]").forEach(btn => btn.addEventListener("click", () => {
    passcodeTargetPortal = btn.dataset.changepass;
    document.getElementById("passcodeModalTitle").textContent = `Change ${passcodeTargetPortal} Passcode`;
    document.getElementById("newPasscodeInput").value = "";
    clearFieldError("newPasscodeInput");
    document.getElementById("passcodeModalOverlay").classList.add("show");
  }));
}
async function savePasscodeChange() {
  const val = document.getElementById("newPasscodeInput").value;
  clearFieldError("newPasscodeInput");
  if (val.length < 4) { markInvalid("newPasscodeInput"); return; }
  try {
    await api("/admin/passcode", { method: "POST", body: JSON.stringify({ portal: passcodeTargetPortal, newPasscode: val }) });
    document.getElementById("passcodeModalOverlay").classList.remove("show");
    showToast(`${passcodeTargetPortal} passcode updated.`);
  } catch (e) { showToast(e.message, true); }
}

// ===== Login history =====
async function loadHistory() {
  try {
    const rows = await api("/admin/login-history?limit=50");
    const body = document.getElementById("historyTableBody");
    if (rows.length === 0) { body.innerHTML = `<tr class="empty-row"><td colspan="4">No login history yet.</td></tr>`; return; }
    body.innerHTML = rows.map(r => `
      <tr><td class="name-cell">${escapeHtml(r.display_name)}</td><td><span class="role-pill ${r.portal}">${r.portal}</span></td>
      <td>${new Date(r.logged_in_at).toLocaleString("en-US",{month:"short",day:"numeric",hour:"2-digit",minute:"2-digit"})}</td>
      <td>${r.logged_out_at ? new Date(r.logged_out_at).toLocaleString("en-US",{month:"short",day:"numeric",hour:"2-digit",minute:"2-digit"}) : "—"}</td></tr>
    `).join("");
  } catch (e) { showToast(e.message, true); }
}

function showToast(msg, isError = false) {
  const toast = document.getElementById("toast");
  document.getElementById("toastText").textContent = msg;
  toast.classList.toggle("error", !!isError);
  toast.classList.add("show");
  setTimeout(() => toast.classList.remove("show"), 3000);
}

// ===== AI Guide =====
let guideReady = false, guideBusy = false;
function initGuide() {
  if (guideReady) return;
  guideReady = true;
  const fab = document.getElementById("guideFab"), panel = document.getElementById("guidePanel");
  fab.addEventListener("click", () => {
    panel.classList.toggle("show");
    if (panel.classList.contains("show")) document.getElementById("guideInput").focus();
  });
  document.getElementById("closeGuide").addEventListener("click", () => panel.classList.remove("show"));
  document.querySelectorAll("#guideQuick button").forEach(btn => btn.addEventListener("click", () => askGuide(btn.dataset.q)));
  document.getElementById("guideSend").addEventListener("click", sendGuideInput);
  document.getElementById("guideInput").addEventListener("keydown", (e) => { if (e.key === "Enter") sendGuideInput(); });
}
function sendGuideInput() {
  const input = document.getElementById("guideInput");
  const q = input.value.trim();
  if (!q || guideBusy) return;
  input.value = "";
  askGuide(q);
}
// Escapes first, then turns **bold** and line breaks into safe HTML
function formatGuideAnswer(text) {
  return escapeHtml(text).replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>").replace(/\n/g, "<br>");
}
async function askGuide(question) {
  if (guideBusy) return;
  guideBusy = true;
  const body = document.getElementById("guideBody");
  body.insertAdjacentHTML("beforeend", `<div class="guide-msg user">${escapeHtml(question)}</div>`);
  body.insertAdjacentHTML("beforeend", `<div class="guide-msg bot guide-typing" id="guideTyping">Thinking...</div>`);
  body.scrollTop = body.scrollHeight;
  try {
    const res = await fetch(`${API_BASE}/ai/ask`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ portal: PORTAL, question })
    });
    const data = await res.json().catch(() => ({}));
    const typing = document.getElementById("guideTyping"); if (typing) typing.remove();
    if (!res.ok) throw new Error(data.error || `The guide returned an error (${res.status}).`);
    if (!data.answer) throw new Error("The guide sent back an empty answer.");
    body.insertAdjacentHTML("beforeend", `<div class="guide-msg bot">${formatGuideAnswer(data.answer)}</div>`);
  } catch (e) {
    const typing = document.getElementById("guideTyping"); if (typing) typing.remove();
    const msg = e instanceof TypeError ? "Can't reach the server. Check your connection and try again." : e.message;
    body.insertAdjacentHTML("beforeend", `<div class="guide-msg bot">Sorry, I couldn't get an answer. (${escapeHtml(msg)})</div>`);
  } finally {
    guideBusy = false;
  }
  body.scrollTop = body.scrollHeight;
}
function escapeHtml(str) { const d = document.createElement("div"); d.textContent = str; return d.innerHTML; }

initGuide();
</script>
</body>
</html>