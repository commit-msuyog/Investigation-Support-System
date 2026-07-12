import streamlit as st
import sqlite3

st.set_page_config(
    page_title="Investigation Support System",
    page_icon="🕵️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🕵️ Investigation Support System")

conn = sqlite3.connect("detections.db")

cursor = conn.cursor()

cursor.execute(
    "SELECT COUNT(*) FROM detections"
)

total_detections = cursor.fetchone()[0]

cursor.execute("""
SELECT COUNT(*)
FROM detections
WHERE name != 'Unknown'
""")

known_persons = cursor.fetchone()[0]

cursor.execute("""
SELECT COUNT(*)
FROM detections
WHERE name = 'Unknown'
""")

unknown_persons = cursor.fetchone()[0]

st.caption("AI-powered Surveillance & Investigation Dashboard")

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "👥 Total Detections",
        total_detections
    )

with col2:
    st.metric(
        "✅ Known Persons",
        known_persons
    )

with col3:
    st.metric(
        "❓ Unknown Persons",
        unknown_persons
    )

conn.close()