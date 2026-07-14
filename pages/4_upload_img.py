import streamlit as st
import os
from PIL import Image

st.set_page_config(
    page_title="Register Person",
    page_icon="👤",
    layout="wide"
)

st.title("👤 Register New Person")
st.caption("Add a new face to the investigation system.")
st.divider()

# INPUTS

name = st.text_input(
    "Person Name"
)

uploaded_image = st.file_uploader(
    "Upload Face Image",
    type=["jpg", "jpeg", "png"]
)

# IMAGE PREVIEW


if uploaded_image is not None:

    image = Image.open(uploaded_image)

    st.image(
        image,
        caption="Image Preview",
        width=300
    )


# REGISTER BUTTON

if st.button("✅ Register Person", use_container_width=True):

    if name.strip() == "":
        st.error("Please enter a person's name.")

    elif uploaded_image is None:
        st.error("Please upload an image.")

    else:

        os.makedirs("known_faces", exist_ok=True)

        file_extension = uploaded_image.name.split(".")[-1]

        save_path = os.path.join(
            "known_faces",
            f"{name}.{file_extension}"
        )

        with open(save_path, "wb") as file:

            file.write(uploaded_image.getbuffer())

        st.success(f"{name} registered successfully!")

        st.info(
            "Restart the Detection Engine to load the new face."
        )