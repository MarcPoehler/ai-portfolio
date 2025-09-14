import streamlit as st
from sidebar import render_common_sidebar


# Entry point
st.set_page_config(page_title="Curriculum Vitae", page_icon="📄", layout="centered")
st.title("📄 Curriculum Vitae")
render_common_sidebar()

pdf_path = "data/CV_Marc_Poehler.pdf"

with open(pdf_path, "rb") as file:
    pdf_bytes = file.read()
st.download_button(
    "📥 Download CV as PDF",
    data=pdf_bytes,
    file_name="CV_Marc_Poehler.pdf",
    mime="application/pdf",
    width="stretch",
)
st.pdf(pdf_path, height=900)
