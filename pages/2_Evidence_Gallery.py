import streamlit as st
import os
from datetime import datetime
from PIL import Image
from style import inject_style
from ui.sidebar import render_sidebar


# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="Evidence Gallery — Investigation Support System",
    page_icon="📸",
    layout="wide"
)

inject_style()
render_sidebar()

# ---------------- HEADER ---------------- #

st.markdown("""
<div class="isys-eyebrow"><span class="isys-dot"></span>ARCHIVE // CAPTURED EVIDENCE</div>
<div class="isys-title">Evidence Gallery</div>
<div class="isys-sub">Browse and search all captured evidence images</div>
<div class="isys-rule"></div>
""", unsafe_allow_html=True)

# ---------------- LOAD IMAGES ---------------- #

image_folder = "detections"

images = []

if os.path.exists(image_folder):

    images = [
        os.path.join(image_folder, image)
        for image in os.listdir(image_folder)
        if image.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

    images.sort(
        key=os.path.getmtime,
        reverse=True
    )

total_count = len(images)

# ---------------- SEARCH ---------------- #

search = st.text_input(
    "Search by filename",
    placeholder="e.g. track_014 or 2026-07-12"
)

if search:
    images = [
        image for image in images
        if search.lower() in os.path.basename(image).lower()
    ]

# ---------------- SUMMARY ---------------- #

st.markdown(
    f'<div class="isys-section">Captured Frames '
    f'<span class="count">{len(images)} of {total_count} shown</span></div>',
    unsafe_allow_html=True
)
st.write("")

# ---------------- GRID ---------------- #

if len(images) == 0:

    st.markdown(
        '<div class="empty-state">NO EVIDENCE IMAGES FOUND<br>check the <b>detections</b> folder or adjust your search</div>',
        unsafe_allow_html=True
    )

else:

    cols = st.columns(3)

    for index, image_path in enumerate(images):

        with cols[index % 3]:

            with st.container(key=f"evidence_{index}"):

                is_latest = index == 0 and not search

                if is_latest:
                    st.markdown('<div class="evidence-tag">Latest</div>', unsafe_allow_html=True)

                image = Image.open(image_path)

                st.image(
                    image,
                    use_container_width=True
                )

                filename = os.path.basename(image_path)
                captured_at = datetime.fromtimestamp(
                    os.path.getmtime(image_path)
                ).strftime("%Y-%m-%d %H:%M:%S")

                st.markdown(
                    f'<div class="evidence-caption">{filename}</div>'
                    f'<div class="evidence-time">CAPTURED {captured_at}</div>',
                    unsafe_allow_html=True
                )