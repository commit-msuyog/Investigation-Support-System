import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt


st.set_page_config(
    page_title="Analytics",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Analytics")
st.caption("Detection Statistics & Insights")
st.divider()



conn = sqlite3.connect("detections.db")

df = pd.read_sql_query(
    "SELECT * FROM detections",
    conn
)

conn.close()


if df.empty:
    st.warning("No detection data available.")
    st.stop()


total = len(df)

known = len(df[df["name"] != "Unknown"])

unknown = len(df[df["name"] == "Unknown"])

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("👥 Total Detections", total)

with col2:
    st.metric("✅ Known Persons", known)

with col3:
    st.metric("❓ Unknown Persons", unknown)

st.divider()


left_col, right_col = st.columns(2)

# PIE CHART

with left_col:

    st.subheader("Known vs Unknown")

    fig, ax = plt.subplots(figsize=(5,5))

    ax.pie(
        [known, unknown],
        labels=["Known", "Unknown"],
        autopct="%1.1f%%",
        startangle=90
    )

    ax.axis("equal")

    st.pyplot(fig)

# BAR CHART

with right_col:

    st.subheader("Top Detected Persons")

    person_counts = (
        df["name"]
        .value_counts()
        .head(5)
    )

    fig, ax = plt.subplots(figsize=(6,5))

    ax.bar(
        person_counts.index,
        person_counts.values
    )

    ax.set_xlabel("Person")

    ax.set_ylabel("Detections")

    st.pyplot(fig)

st.divider()



st.subheader("Detection Summary")

summary = (
    df["name"]
    .value_counts()
    .reset_index()
)

summary.columns = [
    "Person",
    "Detections"
]

st.dataframe(
    summary,
    use_container_width=True,
    hide_index=True
)