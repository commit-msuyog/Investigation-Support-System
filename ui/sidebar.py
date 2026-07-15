"""
Shared sidebar for the Investigation Support System.
Call render_sidebar() from every page (after inject_style()) so the
navigation, status, and developer profile stay identical across pages.

NOTE: HTML passed to st.markdown must not contain blank lines in the
middle of a block, or Streamlit's markdown parser stops treating it as
raw HTML and renders the tags as literal text. Every multi-line
st.markdown() call below is kept as one continuous block for that reason.
"""

import streamlit as st

ICON_LINKEDIN = """<svg viewBox="0 0 24 24"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-4 0v7h-4v-7a6 6 0 0 1 6-6z"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/></svg>"""
ICON_GITHUB = """<svg viewBox="0 0 24 24"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.9c0-1.1.35-1.8.75-2.15-2.6-.3-5.35-1.3-5.35-5.8 0-1.3.45-2.35 1.2-3.2-.1-.3-.5-1.5.1-3.1 0 0 1-.3 3.3 1.2a11.2 11.2 0 0 1 6 0c2.3-1.5 3.3-1.2 3.3-1.2.6 1.6.2 2.8.1 3.1.75.85 1.2 1.9 1.2 3.2 0 4.5-2.75 5.5-5.35 5.8.4.35.75 1.05.75 2.15V19"/></svg>"""
ICON_MAIL = """<svg viewBox="0 0 24 24"><rect x="2" y="4" width="20" height="16" rx="1"/><path d="M2 6l10 7 10-7"/></svg>"""


def render_sidebar():
    with st.sidebar:

        # ---------------- Navigation ---------------- #
        st.markdown('<div class="isys-section">Navigation</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="isys-alert info">ⓘ USE THE PAGES ABOVE TO NAVIGATE THE APPLICATION</div>',
            unsafe_allow_html=True
        )

        st.markdown('<div class="isys-rule"></div>', unsafe_allow_html=True)

        # ---------------- About developer ---------------- #
        st.markdown('<div class="isys-section">About Developer</div>', unsafe_allow_html=True)

        st.markdown(
            '<div class="sidebar-name">Suyog Verma</div>'
            '<div class="social-row">'
            f'<a class="social-icon-link" href="https://www.linkedin.com/in/suyog01/" target="_blank" title="LinkedIn">{ICON_LINKEDIN}</a>'
            f'<a class="social-icon-link" href="https://github.com/commit-msuyog" target="_blank" title="GitHub">{ICON_GITHUB}</a>'
            f'<a class="social-icon-link" href="mailto:suyogverma0057@gmail.com" title="Email">{ICON_MAIL}</a>'
            "</div>",
            unsafe_allow_html=True
        )

        st.markdown('<div class="isys-rule"></div>', unsafe_allow_html=True)

        # ---------------- Tech stack ---------------- #
        st.markdown('<div class="isys-section">Tech Stack</div>', unsafe_allow_html=True)
        stack = ["Python", "YOLOv8", "OpenCV", "Face Recognition", "SQLite", "Streamlit"]
        pills_html = "".join(f'<span class="tech-pill">{item}</span>' for item in stack)
        st.markdown(f'<div class="tech-pill-row">{pills_html}</div>', unsafe_allow_html=True)

        st.markdown('<div class="isys-rule"></div>', unsafe_allow_html=True)

        # ---------------- Footer ---------------- #
        st.markdown(
            '<div class="sidebar-footer">VERSION 1.0.0<br>© 2026 SUYOG VERMA</div>',
            unsafe_allow_html=True
        )