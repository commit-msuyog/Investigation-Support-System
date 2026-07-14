import streamlit as st
import os
from PIL import Image

st.set_page_config(
    page_title="Evidence Gallery",
    page_icon="📸",
    layout="wide"
)

st.title("📸 Evidence Gallery")
st.caption("View all captured evidence images.")
st.divider()

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

search = st.text_input(
    "🔍 Search by filename"
)

if search:

    images = [
        image for image in images
        if search.lower() in os.path.basename(image).lower()
    ]

if len(images) == 0:

    st.info("No evidence images found.")

else:

    cols = st.columns(3)

    for index, image_path in enumerate(images):

        with cols[index % 3]:

            image = Image.open(image_path)

            st.image(
                image,
                use_container_width=True
            )

            st.caption(
                os.path.basename(image_path)
            )