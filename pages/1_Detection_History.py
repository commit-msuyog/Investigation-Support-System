import streamlit as st
import sqlite3
from style import inject_style
from ui.sidebar import render_sidebar

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="History — Investigation Support System",
    page_icon="🗂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_style()
render_sidebar()

# ---------------- HEADER ---------------- #

st.markdown("""
<div class="isys-eyebrow"><span class="isys-dot"></span>ARCHIVE // FULL DETECTION LOG</div>
<div class="isys-title">Detection History</div>
<div class="isys-sub">Search, filter, and page through every logged detection</div>
<div class="isys-rule"></div>
""", unsafe_allow_html=True)

# ---------------- DATABASE ---------------- #

conn = sqlite3.connect("detections.db")
cursor = conn.cursor()

cursor.execute("""
SELECT track_id, name, confidence, detected_time
FROM detections
ORDER BY detected_time DESC
""")
all_rows = cursor.fetchall()

cursor.execute("SELECT MIN(detected_time), MAX(detected_time) FROM detections")
min_time, max_time = cursor.fetchone()

conn.close()

# ---------------- FILTER BAR ---------------- #

with st.container(key="filter_bar"):
    f1, f2, f3, f4 = st.columns([2, 1.2, 1.2, 1.2])

    with f1:
        search_term = st.text_input("Search by name", placeholder="e.g. J. Rivera")
    with f2:
        status_filter = st.selectbox("Status", ["All", "Identified", "Unidentified"])
    with f3:
        sort_field = st.selectbox("Sort by", ["Time (newest)", "Time (oldest)", "Confidence (high→low)", "Confidence (low→high)"])
    with f4:
        min_conf = st.selectbox("Min. confidence", ["Any", "0.50+", "0.70+", "0.90+"])

# ---------------- APPLY FILTERS ---------------- #

rows = all_rows

if search_term:
    rows = [r for r in rows if search_term.lower() in r[1].lower()]

if status_filter == "Identified":
    rows = [r for r in rows if r[1] != "Unknown"]
elif status_filter == "Unidentified":
    rows = [r for r in rows if r[1] == "Unknown"]

conf_thresholds = {"Any": 0.0, "0.50+": 0.5, "0.70+": 0.7, "0.90+": 0.9}
threshold = conf_thresholds[min_conf]
rows = [r for r in rows if r[2] >= threshold]

if sort_field == "Time (newest)":
    rows = sorted(rows, key=lambda r: r[3], reverse=True)
elif sort_field == "Time (oldest)":
    rows = sorted(rows, key=lambda r: r[3])
elif sort_field == "Confidence (high→low)":
    rows = sorted(rows, key=lambda r: r[2], reverse=True)
else:
    rows = sorted(rows, key=lambda r: r[2])

# ---------------- SUMMARY ---------------- #

st.markdown(
    f'<div class="isys-section">Archive '
    f'<span class="count">{len(rows)} of {len(all_rows)} records &middot; range {min_time or "—"} to {max_time or "—"}</span></div>',
    unsafe_allow_html=True
)
st.write("")

# ---------------- PAGINATION STATE ---------------- #

PAGE_SIZE = 15
total_pages = max(1, (len(rows) - 1) // PAGE_SIZE + 1)

if "history_page" not in st.session_state:
    st.session_state.history_page = 1

# clamp page if filters shrank the result set
st.session_state.history_page = min(st.session_state.history_page, total_pages)

page = st.session_state.history_page
start = (page - 1) * PAGE_SIZE
end = start + PAGE_SIZE
page_rows = rows[start:end]

# ---------------- TABLE ---------------- #

if len(rows) == 0:
    st.markdown(
        '<div class="empty-state">NO RECORDS MATCH THE CURRENT FILTERS<br>adjust search or filter criteria above</div>',
        unsafe_allow_html=True
    )
else:
    row_parts = []
    for track_id, name, confidence, detected_time in page_rows:
        is_known = name != "Unknown"
        status_class = "known" if is_known else "unknown"
        badge_text = "Identified" if is_known else "Unidentified"
        pct = max(0, min(100, int(confidence * 100)))

        row_parts.append(
            "<tr>"
            f"<td>{detected_time}</td>"
            f"<td>#{track_id}</td>"
            f'<td class="hist-name">{name}</td>'
            f'<td><span class="badge {status_class}">{badge_text}</span></td>'
            "<td>"
            f'<span class="mini-track"><span class="mini-fill {status_class}" style="width:{pct}%; display:block;"></span></span>{confidence:.2f}'
            "</td>"
            "</tr>"
        )
    table_rows_html = "".join(row_parts)

    table_html = (
        '<table class="hist-table">'
        "<thead><tr>"
        "<th>Timestamp</th><th>Case ID</th><th>Name</th><th>Status</th><th>Confidence</th>"
        "</tr></thead>"
        f"<tbody>{table_rows_html}</tbody>"
        "</table>"
    )
    st.markdown(table_html, unsafe_allow_html=True)

    st.write("")

    # ---------------- PAGINATION CONTROLS ---------------- #

    p1, p2, p3 = st.columns([1, 3, 1])

    with p1:
        if st.button("← Prev", disabled=(page <= 1)):
            st.session_state.history_page -= 1
            st.rerun()

    with p2:
        st.markdown(
            f'<div class="page-info" style="text-align:center; padding-top:8px;">'
            f'PAGE {page} OF {total_pages} &nbsp;&middot;&nbsp; SHOWING {start + 1}–{min(end, len(rows))} OF {len(rows)}'
            f'</div>',
            unsafe_allow_html=True
        )

    with p3:
        if st.button("Next →", disabled=(page >= total_pages)):
            st.session_state.history_page += 1
            st.rerun()