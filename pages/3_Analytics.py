import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from style import inject_style
from ui.sidebar import render_sidebar


# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="Analytics — Investigation Support System",
    page_icon="📈",
    layout="wide"
)

inject_style()
render_sidebar()

# =====================================
# CHART THEME (matches style.py palette)
# =====================================

BG = "#0a0c0e"
PANEL = "#12151a"
PANEL_2 = "#171b21"
BORDER = "#242a32"
TEXT = "#dce1e6"
MUTED = "#7c8792"
GREEN = "#35d488"
AMBER = "#f2a93b"

plt.rcParams["font.family"] = "monospace"


def style_ax(fig, ax):
    fig.patch.set_facecolor(PANEL)
    ax.set_facecolor(PANEL)
    ax.tick_params(colors=MUTED, labelsize=9)
    for spine in ax.spines.values():
        spine.set_color(BORDER)
    ax.xaxis.label.set_color(MUTED)
    ax.yaxis.label.set_color(MUTED)
    ax.title.set_color(TEXT)
    ax.grid(axis="y", color=BORDER, linewidth=0.6, alpha=0.6)
    ax.set_axisbelow(True)


# =====================================
# HEADER
# =====================================

st.markdown("""
<div class="isys-eyebrow"><span class="isys-dot"></span>ANALYTICS // DETECTION TRENDS</div>
<div class="isys-title">Analytics</div>
<div class="isys-sub">Detection statistics and pattern insights</div>
<div class="isys-rule"></div>
""", unsafe_allow_html=True)

# =====================================
# DATABASE
# =====================================

conn = sqlite3.connect("detections.db")

df = pd.read_sql_query(
    "SELECT * FROM detections",
    conn
)

conn.close()

# =====================================
# NO DATA CHECK
# =====================================

if df.empty:
    st.markdown(
        '<div class="empty-state">NO DETECTION DATA AVAILABLE<br>analytics will populate once detections are logged</div>',
        unsafe_allow_html=True
    )
    st.stop()

# =====================================
# BASIC STATISTICS
# =====================================

total = len(df)
known = len(df[df["name"] != "Unknown"])
unknown = len(df[df["name"] == "Unknown"])
known_pct = (known / total * 100) if total else 0

st.markdown('<div class="isys-section">Overview</div>', unsafe_allow_html=True)
st.write("")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="readout-panel">
        <div class="readout-label">Total Detections</div>
        <div class="readout-value plain">{total}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="readout-panel">
        <div class="readout-label">Identified Persons</div>
        <div class="readout-value green">{known}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="readout-panel">
        <div class="readout-label">Unidentified Persons</div>
        <div class="readout-value amber">{unknown}</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.markdown('<div class="isys-rule"></div>', unsafe_allow_html=True)

# =====================================
# CHARTS
# =====================================

st.markdown('<div class="isys-section">Detection Breakdown</div>', unsafe_allow_html=True)
st.write("")

left_col, right_col = st.columns(2)

# ---------- PIE CHART ----------

with left_col:

    st.markdown(
        '<div class="readout-label" style="margin-bottom:10px;">Identified vs Unidentified</div>',
        unsafe_allow_html=True
    )

    fig, ax = plt.subplots(figsize=(5, 5))
    fig.patch.set_facecolor(PANEL)

    wedges, texts, autotexts = ax.pie(
        [known, unknown],
        labels=["Identified", "Unidentified"],
        autopct="%1.1f%%",
        startangle=90,
        colors=[GREEN, AMBER],
        wedgeprops={"edgecolor": PANEL, "linewidth": 2},
        textprops={"color": TEXT, "fontsize": 10}
    )
    for autotext in autotexts:
        autotext.set_color(BG)
        autotext.set_fontweight("bold")

    ax.axis("equal")

    st.pyplot(fig)

# ---------- BAR CHART ----------

with right_col:

    st.markdown(
        '<div class="readout-label" style="margin-bottom:10px;">Top Detected Persons</div>',
        unsafe_allow_html=True
    )

    person_counts = (
        df["name"]
        .value_counts()
        .head(5)
    )

    fig, ax = plt.subplots(figsize=(6, 5))

    bar_colors = [AMBER if p == "Unknown" else GREEN for p in person_counts.index]

    ax.bar(
        person_counts.index,
        person_counts.values,
        color=bar_colors,
        edgecolor=PANEL,
        linewidth=0.5
    )

    ax.set_xlabel("PERSON")
    ax.set_ylabel("DETECTIONS")
    style_ax(fig, ax)
    plt.setp(ax.get_xticklabels(), rotation=20, ha="right")

    st.pyplot(fig)

# ---------- TIME SERIES ----------

if "detected_time" in df.columns:

    st.write("")
    st.markdown('<div class="isys-rule"></div>', unsafe_allow_html=True)
    st.markdown('<div class="isys-section">Detections Over Time</div>', unsafe_allow_html=True)
    st.write("")

    ts = df.copy()
    ts["detected_time"] = pd.to_datetime(ts["detected_time"], errors="coerce")
    ts = ts.dropna(subset=["detected_time"])

    if not ts.empty:
        daily_counts = (
            ts.set_index("detected_time")
            .resample("D")
            .size()
        )

        fig, ax = plt.subplots(figsize=(12, 4))

        ax.plot(
            daily_counts.index,
            daily_counts.values,
            color=GREEN,
            linewidth=1.8,
            marker="o",
            markersize=4,
            markerfacecolor=GREEN,
            markeredgecolor=PANEL
        )
        ax.fill_between(
            daily_counts.index,
            daily_counts.values,
            color=GREEN,
            alpha=0.12
        )

        ax.set_xlabel("DATE")
        ax.set_ylabel("DETECTIONS")
        style_ax(fig, ax)
        fig.autofmt_xdate()

        st.pyplot(fig)

st.write("")
st.markdown('<div class="isys-rule"></div>', unsafe_allow_html=True)

# =====================================
# TABLE
# =====================================

st.markdown('<div class="isys-section">Detection Summary</div>', unsafe_allow_html=True)
st.write("")

summary = (
    df["name"]
    .value_counts()
    .reset_index()
)
summary.columns = ["Person", "Detections"]
max_count = summary["Detections"].max()

row_parts = []
for _, row in summary.iterrows():
    is_known = row["Person"] != "Unknown"
    status_class = "known" if is_known else "unknown"
    pct = int((row["Detections"] / max_count) * 100) if max_count else 0

    row_parts.append(
        "<tr>"
        f'<td class="hist-name">{row["Person"]}</td>'
        "<td>"
        f'<span class="mini-track" style="width:140px;"><span class="mini-fill {status_class}" style="width:{pct}%; display:block;"></span></span>{row["Detections"]}'
        "</td>"
        "</tr>"
    )
table_rows_html = "".join(row_parts)

table_html = (
    '<table class="hist-table">'
    "<thead><tr><th>Person</th><th>Detections</th></tr></thead>"
    f"<tbody>{table_rows_html}</tbody>"
    "</table>"
)
st.markdown(table_html, unsafe_allow_html=True)