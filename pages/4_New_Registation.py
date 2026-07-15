import streamlit as st
import os
from PIL import Image
from style import inject_style
from ui.sidebar import render_sidebar

st.set_page_config(
    page_title="Register Person — Investigation Support System",
    page_icon="👤",
    layout="wide"
)

inject_style()
render_sidebar()

st.markdown("""
<div class="isys-eyebrow"><span class="isys-dot"></span>REGISTRATION // ADD KNOWN FACE</div>
<div class="isys-title">Register New Person</div>
<div class="isys-sub">Add a new face to the identification database</div>
<div class="isys-rule"></div>
""", unsafe_allow_html=True)

st.markdown('<div class="isys-section">Person Details</div>', unsafe_allow_html=True)
st.write("")

with st.container(key="register_form"):

    st.markdown('<div class="form-panel">', unsafe_allow_html=True)

    name = st.text_input(
        "Person Name",
        placeholder="e.g. J. Rivera"
    )

    uploaded_image = st.file_uploader(
        "Upload Face Image",
        type=["jpg", "jpeg", "png"]
    )

    st.markdown('</div>', unsafe_allow_html=True)


if uploaded_image is not None:

    st.markdown('<div class="isys-section">Preview</div>', unsafe_allow_html=True)

    with st.container(key="preview_frame"):
        image = Image.open(uploaded_image)
        st.image(image, width=300)

    st.markdown(
        f'<div class="case-meta" style="margin-top:-10px;">FILE: {uploaded_image.name}</div>',
        unsafe_allow_html=True
    )

st.write("")


if st.button("Register Person", type="primary", use_container_width=True):

    if name.strip() == "":
        st.markdown(
            '<div class="isys-alert error">✕ PLEASE ENTER A PERSON\'S NAME</div>',
            unsafe_allow_html=True
        )

    elif uploaded_image is None:
        st.markdown(
            '<div class="isys-alert error">✕ PLEASE UPLOAD AN IMAGE</div>',
            unsafe_allow_html=True
        )

    else:

        os.makedirs("known_faces", exist_ok=True)

        file_extension = uploaded_image.name.split(".")[-1]

        save_path = os.path.join(
            "known_faces",
            f"{name}.{file_extension}"
        )

        with open(save_path, "wb") as file:
            file.write(uploaded_image.getbuffer())

        st.markdown(
            f'<div class="isys-alert success">✓ {name.upper()} REGISTERED SUCCESSFULLY</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="isys-alert info">ⓘ RESTART THE DETECTION ENGINE TO LOAD THE NEW FACE</div>',
            unsafe_allow_html=True
        )