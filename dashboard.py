import streamlit as st
import sqlite3


st.set_page_config(
    page_title="Investigation Support System",
    page_icon="🕵️",
    layout="wide",
    initial_sidebar_state="expanded"
)


conn = sqlite3.connect("detections.db")
cursor = conn.cursor()


cursor.execute("SELECT COUNT(*) FROM detections")
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



cursor.execute("""
SELECT
    track_id,
    name,
    confidence,
    detected_time
FROM detections
ORDER BY detected_time DESC
LIMIT 5
""")

recent_detections = cursor.fetchall()

conn.close()


st.title("🕵️ Investigation Support System")
st.caption("AI-powered Surveillance Dashboard")

st.divider()


left_col, right_col = st.columns([2, 1])


# LEFT COLUMN


with left_col:

    st.subheader("📋 Recent Detections")

    st.divider()

    if len(recent_detections) == 0:

        st.info("No detections found.")

    else:

        for detection in recent_detections:

            track_id = detection[0]
            name = detection[1]
            confidence = detection[2]
            detected_time = detection[3]

            with st.container(border=True):

                st.write(f"### 👤 {name}")

                st.write(f"🆔 Track ID : {track_id}")

                st.write(f"🕒 {detected_time}")

                st.write(
                    f"🎯 Confidence : {confidence:.2f}"
                )

                st.progress(
                    int(confidence * 100)
                )

# RIGHT COLUMN


with right_col:

    st.subheader("📊 Statistics")

    st.metric(
        "👥 Total Detections",
        total_detections
    )

    st.metric(
        "✅ Known Persons",
        known_persons
    )

    st.metric(
        "❓ Unknown Persons",
        unknown_persons
    )

    st.success("🟢 System Running")