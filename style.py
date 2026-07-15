"""
Shared visual design system for the Investigation Support System.
Import inject_style() at the top of every page so the console aesthetic
(colors, type, cards, table, filters) stays identical across pages.
"""

import streamlit as st

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@500;600;700&family=IBM+Plex+Mono:wght@400;500;600&family=Inter:wght@400;500;600&display=swap');

:root {
    --bg: #0a0c0e;
    --panel: #12151a;
    --panel-2: #171b21;
    --border: #242a32;
    --text: #dce1e6;
    --muted: #7c8792;
    --green: #35d488;
    --amber: #f2a93b;
    --red: #e5484d;
}

.stApp {
    background:
        repeating-linear-gradient(0deg, rgba(255,255,255,0.012) 0px, rgba(255,255,255,0.012) 1px, transparent 1px, transparent 3px),
        var(--bg);
}

html, body, [class*="css"] { font-family: 'Inter', sans-serif; color: var(--text); }

#MainMenu, footer, header { visibility: hidden; }

.block-container { padding-top: 2rem; max-width: 1200px; }

/* ---------- Sidebar nav ---------- */
[data-testid="stSidebar"] {
    background: var(--panel);
    border-right: 1px solid var(--border);
}
[data-testid="stSidebarNav"] a span {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

/* ---------- Header ---------- */
.isys-eyebrow {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.22em;
    color: var(--green);
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 6px;
}
.isys-dot {
    width: 7px; height: 7px; border-radius: 50%;
    background: var(--green);
    box-shadow: 0 0 8px var(--green);
    animation: pulse 1.8s infinite ease-in-out;
}
@keyframes pulse { 0%,100% { opacity: 1; } 50% { opacity: 0.25; } }

.isys-title {
    font-family: 'Oswald', sans-serif;
    font-weight: 700;
    font-size: 2.6rem;
    text-transform: uppercase;
    letter-spacing: 0.03em;
    line-height: 1.05;
    margin: 0;
}
.isys-sub {
    font-family: 'IBM Plex Mono', monospace;
    color: var(--muted);
    font-size: 0.85rem;
    margin-top: 6px;
}
.isys-rule {
    height: 1px;
    background: linear-gradient(90deg, var(--border), transparent);
    margin: 22px 0 28px 0;
}

/* ---------- Section labels ---------- */
.isys-section {
    font-family: 'Oswald', sans-serif;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-size: 1rem;
    font-weight: 600;
    color: var(--text);
    display: flex;
    align-items: baseline;
    gap: 10px;
    margin-bottom: 4px;
}
.isys-section span.count {
    font-family: 'IBM Plex Mono', monospace;
    color: var(--muted);
    font-size: 0.78rem;
    font-weight: 400;
    letter-spacing: 0;
}

/* ---------- Case card (recent detections list) ---------- */
.case-card {
    position: relative;
    background: var(--panel);
    border: 1px solid var(--border);
    padding: 18px 20px;
    margin-bottom: 14px;
    border-radius: 2px;
}
.case-card::before, .case-card::after,
.case-card .cb2::before, .case-card .cb2::after {
    content: ""; position: absolute; width: 14px; height: 14px;
    border-color: var(--border-accent, var(--green));
}
.case-card.unknown { --border-accent: var(--amber); }
.case-card.known { --border-accent: var(--green); }
.case-card::before { top: -1px; left: -1px; border-top: 2px solid var(--border-accent); border-left: 2px solid var(--border-accent); }
.case-card::after { top: -1px; right: -1px; border-top: 2px solid var(--border-accent); border-right: 2px solid var(--border-accent); }
.case-card .cb2::before { bottom: -1px; left: -1px; border-bottom: 2px solid var(--border-accent); border-left: 2px solid var(--border-accent); }
.case-card .cb2::after { bottom: -1px; right: -1px; border-bottom: 2px solid var(--border-accent); border-right: 2px solid var(--border-accent); }

.case-top { display: flex; justify-content: space-between; align-items: flex-start; }
.case-name { font-family: 'Oswald', sans-serif; font-size: 1.25rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.01em; }
.case-meta { font-family: 'IBM Plex Mono', monospace; font-size: 0.78rem; color: var(--muted); margin-top: 4px; }

.badge {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.1em;
    padding: 3px 9px;
    border-radius: 2px;
    border: 1px solid;
    white-space: nowrap;
    text-transform: uppercase;
}
.badge.known { color: var(--green); border-color: var(--green); background: rgba(53,212,136,0.08); }
.badge.unknown { color: var(--amber); border-color: var(--amber); background: rgba(242,169,59,0.08); }

.conf-row { display: flex; align-items: center; gap: 10px; margin-top: 14px; }
.conf-label { font-family: 'IBM Plex Mono', monospace; font-size: 0.72rem; color: var(--muted); letter-spacing: 0.08em; min-width: 92px; }
.conf-track { flex: 1; height: 5px; background: var(--panel-2); border-radius: 3px; overflow: hidden; }
.conf-fill { height: 100%; border-radius: 3px; }
.conf-fill.known { background: var(--green); }
.conf-fill.unknown { background: var(--amber); }
.conf-value { font-family: 'IBM Plex Mono', monospace; font-size: 0.78rem; color: var(--text); min-width: 40px; text-align: right; }

/* ---------- Empty state ---------- */
.empty-state {
    border: 1px dashed var(--border);
    padding: 40px 20px;
    text-align: center;
    font-family: 'IBM Plex Mono', monospace;
    color: var(--muted);
    font-size: 0.85rem;
    letter-spacing: 0.05em;
}

/* ---------- Readouts (stats) ---------- */
.readout-panel {
    background: var(--panel);
    border: 1px solid var(--border);
    padding: 20px 22px;
    margin-bottom: 12px;
}
.readout-label { font-family: 'IBM Plex Mono', monospace; font-size: 0.7rem; letter-spacing: 0.14em; color: var(--muted); text-transform: uppercase; }
.readout-value { font-family: 'Oswald', sans-serif; font-size: 2.4rem; font-weight: 600; line-height: 1.15; margin-top: 2px; }
.readout-value.green { color: var(--green); }
.readout-value.amber { color: var(--amber); }
.readout-value.plain { color: var(--text); }

.status-panel {
    border: 1px solid var(--border);
    background: var(--panel);
    padding: 16px 20px;
    display: flex; align-items: center; gap: 10px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.78rem;
    letter-spacing: 0.1em;
    color: var(--green);
    text-transform: uppercase;
    margin-top: 6px;
}

/* ---------- Filter bar (History page) ---------- */
div[class*="st-key-filter_bar"] {
    background: var(--panel);
    border: 1px solid var(--border);
    padding: 16px 18px 4px 18px;
    margin-bottom: 20px;
}
[data-testid="stTextInput"] input,
[data-testid="stDateInput"] input,
div[data-baseweb="select"] > div {
    background: var(--panel-2) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.82rem !important;
    border-radius: 2px !important;
}
[data-testid="stWidgetLabel"] p {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.68rem !important;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--muted) !important;
}

/* ---------- History table ---------- */
.hist-table { width: 100%; border-collapse: collapse; border: 1px solid var(--border); }
.hist-table thead th {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--muted);
    text-align: left;
    padding: 10px 14px;
    border-bottom: 1px solid var(--border);
    background: var(--panel);
}
.hist-table tbody td {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.82rem;
    padding: 11px 14px;
    border-bottom: 1px solid var(--border);
    color: var(--text);
    vertical-align: middle;
}
.hist-table tbody tr:nth-child(odd) { background: var(--panel); }
.hist-table tbody tr:nth-child(even) { background: var(--panel-2); }
.hist-table tbody tr:hover { background: #1b2028; }
.hist-name { font-family: 'Oswald', sans-serif; font-weight: 600; text-transform: uppercase; letter-spacing: 0.01em; font-size: 0.92rem; }
.mini-track { width: 90px; height: 4px; background: var(--panel-2); border-radius: 3px; overflow: hidden; display: inline-block; vertical-align: middle; margin-right: 8px; }
.mini-fill { height: 100%; border-radius: 3px; }
.mini-fill.known { background: var(--green); }
.mini-fill.unknown { background: var(--amber); }

/* ---------- Evidence gallery ---------- */
div[class*="st-key-evidence_"] {
    position: relative;
    background: var(--panel);
    border: 1px solid var(--border);
    padding: 10px 10px 14px 10px;
    margin-bottom: 18px;
    transition: border-color 0.15s ease;
}
div[class*="st-key-evidence_"]:hover { border-color: var(--green); }
div[class*="st-key-evidence_"]::before, div[class*="st-key-evidence_"]::after {
    content: ""; position: absolute; width: 12px; height: 12px; z-index: 2;
}
div[class*="st-key-evidence_"]::before { top: -1px; left: -1px; border-top: 2px solid var(--green); border-left: 2px solid var(--green); }
div[class*="st-key-evidence_"]::after { top: -1px; right: -1px; border-top: 2px solid var(--green); border-right: 2px solid var(--green); }
div[class*="st-key-evidence_"] img { border-radius: 1px; }

.evidence-caption {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.78rem;
    color: var(--text);
    margin-top: 10px;
    word-break: break-all;
}
.evidence-time {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    color: var(--muted);
    letter-spacing: 0.06em;
    margin-top: 2px;
}
.evidence-tag {
    position: absolute;
    top: 8px; right: 8px;
    z-index: 3;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--bg);
    background: var(--green);
    padding: 2px 7px;
    border-radius: 2px;
}

/* ---------- Chart panel (Analytics) ---------- */
div[class*="st-key-chart_"] {
    background: var(--panel);
    border: 1px solid var(--border);
    border-top: 2px solid var(--green);
    padding: 20px 22px 8px 22px;
    margin-bottom: 20px;
}
div[class*="st-key-tstat_"] {
    background: var(--panel);
    border: 1px solid var(--border);
    padding: 18px 20px;
}

/* ---------- Form panel (Register page) ---------- */
div[class*="st-key-register_form"] {
    background: var(--panel);
    border: 1px solid var(--border);
    padding: 24px 26px 8px 26px;
    margin-bottom: 18px;
}

/* ---------- File uploader ---------- */
[data-testid="stFileUploaderDropzone"] {
    background: var(--panel-2) !important;
    border: 1px dashed var(--border) !important;
    border-radius: 2px !important;
}
[data-testid="stFileUploaderDropzone"] button {
    background: var(--panel) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.72rem !important;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}
[data-testid="stFileUploaderDropzone"] small,
[data-testid="stFileUploaderDropzone"] div {
    color: var(--muted) !important;
    font-family: 'IBM Plex Mono', monospace !important;
}

/* ---------- Preview frame (Register page) ---------- */
div[class*="st-key-preview_frame"] {
    position: relative;
    background: var(--panel);
    border: 1px solid var(--border);
    padding: 10px;
    margin: 10px 0 18px 0;
    display: inline-block;
}
div[class*="st-key-preview_frame"]::before, div[class*="st-key-preview_frame"]::after {
    content: ""; position: absolute; width: 12px; height: 12px; z-index: 2;
}
div[class*="st-key-preview_frame"]::before { top: -1px; left: -1px; border-top: 2px solid var(--green); border-left: 2px solid var(--green); }
div[class*="st-key-preview_frame"]::after { bottom: -1px; right: -1px; border-bottom: 2px solid var(--green); border-right: 2px solid var(--green); }
div[class*="st-key-preview_frame"] img { border-radius: 1px; }

/* ---------- Primary action button ---------- */
.stButton > button[kind="primary"] {
    background: var(--green) !important;
    border: 1px solid var(--green) !important;
    color: var(--bg) !important;
    font-weight: 600 !important;
}
.stButton > button[kind="primary"]:hover {
    background: #2bc07a !important;
    border-color: #2bc07a !important;
    color: var(--bg) !important;
}

/* ---------- Custom alert banners ---------- */
.isys-alert {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.82rem;
    padding: 12px 16px;
    border: 1px solid var(--border);
    border-left: 3px solid var(--border-accent);
    background: var(--panel);
    margin: 14px 0;
    letter-spacing: 0.02em;
}
.isys-alert.success { --border-accent: var(--green); color: var(--green); }
.isys-alert.error { --border-accent: var(--red); color: var(--red); }
.isys-alert.info { --border-accent: var(--muted); color: var(--text); }

/* ---------- Sidebar profile block ---------- */
.sidebar-title {
    font-family: 'Oswald', sans-serif;
    font-weight: 700;
    font-size: 1.35rem;
    text-transform: uppercase;
    letter-spacing: 0.02em;
    line-height: 1.2;
    margin: 0;
}
.sidebar-name {
    font-family: 'Oswald', sans-serif;
    font-weight: 700;
    font-size: 1.1rem;
    text-transform: uppercase;
    letter-spacing: 0.02em;
    margin-top: 2px;
}
.sidebar-role {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    color: var(--green);
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 10px;
}
.sidebar-bio {
    font-family: 'Inter', sans-serif;
    font-size: 0.82rem;
    color: var(--muted);
    line-height: 1.55;
    margin-bottom: 16px;
}
.social-row {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 8px;
    margin: 10px 0 4px 0;
}
.social-icon-link {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 30px;
    height: 30px;
    flex-shrink: 0;
    border: 1px solid var(--border);
    border-radius: 2px;
    background: var(--panel-2);
    color: var(--muted);
    text-decoration: none;
    margin-right: 6px;
    transition: all 0.15s ease;
}
.social-icon-link svg {
    width: 14px;
    height: 14px;
    fill: none;
    stroke: currentColor;
    stroke-width: 2;
}
.social-icon-link:hover {
    border-color: var(--green);
    color: var(--green);
    background: rgba(53, 212, 136, 0.08);
}
.tech-pill-row {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 8px;
}
.tech-pill {
    display: inline-block;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.04em;
    padding: 4px 10px;
    border: 1px solid var(--border);
    border-radius: 2px;
    background: var(--panel-2);
    color: var(--muted);
    margin: 0 8px 8px 0;
    white-space: nowrap;
}
.sidebar-footer {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    color: var(--muted);
    letter-spacing: 0.05em;
    line-height: 1.6;
}

/* ---------- Pagination ---------- */
.page-info {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.75rem;
    color: var(--muted);
    letter-spacing: 0.05em;
}
.stButton > button {
    background: var(--panel) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    border-radius: 2px !important;
    padding: 4px 14px !important;
}
.stButton > button:hover { border-color: var(--green) !important; color: var(--green) !important; }
.stButton > button:disabled { opacity: 0.3 !important; }
</style>
"""


def inject_style():
    st.markdown(CSS, unsafe_allow_html=True)