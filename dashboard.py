import streamlit as st
import sqlite3
from style import inject_style
from ui.sidebar import render_sidebar



# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="Investigation Support System",
    page_icon="🕵️",
    layout="wide",
    initial_sidebar_state="expanded"
)
inject_style()

render_sidebar()


# ---------------- DATABASE ---------------- #

conn = sqlite3.connect("detections.db")
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM detections")
total_detections = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM detections WHERE name != 'Unknown'")
known_persons = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM detections WHERE name = 'Unknown'")
unknown_persons = cursor.fetchone()[0]

cursor.execute("""
SELECT track_id, name, confidence, detected_time
FROM detections
ORDER BY detected_time DESC
LIMIT 5
""")
recent_detections = cursor.fetchall()

conn.close()

# ---------------- HEADER ---------------- #

st.markdown("""
<div class="isys-eyebrow"><span class="isys-dot"></span>LIVE FEED // NETWORK ONLINE</div>
<div class="isys-title">Investigation Support System</div>
<div class="isys-sub">AI-powered surveillance dashboard &mdash; automated detection log</div>
<div class="isys-rule"></div>
""", unsafe_allow_html=True)

# ---------------- LAYOUT ---------------- #

left_col, right_col = st.columns([2, 1], gap="large")

# ==================================================
# LEFT COLUMN — RECENT DETECTIONS
# ==================================================

with left_col:

    st.markdown(
        f'<div class="isys-section">Recent Detections '
        f'<span class="count">{len(recent_detections)} logged</span></div>',
        unsafe_allow_html=True
    )
    st.write("")

    if len(recent_detections) == 0:
        st.markdown(
            '<div class="empty-state">NO DETECTIONS ON RECORD<br>awaiting next signal from feed</div>',
            unsafe_allow_html=True
        )
    else:
        for track_id, name, confidence, detected_time in recent_detections:
            is_known = name != "Unknown"
            status_class = "known" if is_known else "unknown"
            badge_text = "Identified" if is_known else "Unidentified"
            pct = max(0, min(100, int(confidence * 100)))

            st.markdown(f"""
            <div class="case-card {status_class}">
                <div class="cb2"></div>
                <div class="case-top">
                    <div>
                        <div class="case-name">{name}</div>
                        <div class="case-meta">CASE #{track_id} &nbsp;&middot;&nbsp; {detected_time}</div>
                    </div>
                    <div class="badge {status_class}">{badge_text}</div>
                </div>
                <div class="conf-row">
                    <div class="conf-label">CONFIDENCE</div>
                    <div class="conf-track"><div class="conf-fill {status_class}" style="width:{pct}%;"></div></div>
                    <div class="conf-value">{confidence:.2f}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ==================================================
# RIGHT COLUMN — STATISTICS
# ==================================================

with right_col:

    st.markdown('<div class="isys-section">System Statistics</div>', unsafe_allow_html=True)
    st.write("")

    st.markdown(f"""
    <div class="readout-panel">
        <div class="readout-label">Total Detections</div>
        <div class="readout-value plain">{total_detections}</div>
    </div>
    <div class="readout-panel">
        <div class="readout-label">Identified Persons</div>
        <div class="readout-value green">{known_persons}</div>
    </div>
    <div class="readout-panel">
        <div class="readout-label">Unidentified Persons</div>
        <div class="readout-value amber">{unknown_persons}</div>
    </div>
    <div class="status-panel"><span class="isys-dot"></span>System Operational</div>
    """, unsafe_allow_html=True)