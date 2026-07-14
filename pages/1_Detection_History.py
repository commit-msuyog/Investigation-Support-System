import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(
    page_title="Detection History",
    page_icon="📂",
    layout="wide"
)

st.title("📂 Detection History")

st.caption("View and search all recorded detections.")

st.divider()

# DATABASE


conn = sqlite3.connect("detections.db")

query = """
SELECT
    track_id,
    name,
    confidence,
    detected_time
FROM detections
ORDER BY detected_time DESC
"""

df = pd.read_sql_query(query, conn)

conn.close()

# SEARCH

search = st.text_input(
    "🔍 Search by Name"
)

if search:

    df = df[
        df["name"].str.contains(
            search,
            case=False,
            na=False
        )
    ]

# TABLE


st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)