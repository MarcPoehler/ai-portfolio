import streamlit as st
from sidebar import render_common_sidebar

# Entry point
st.set_page_config(page_title="Welcome!", page_icon="👋", layout="centered")
st.title("👋 Welcome!")
render_common_sidebar()

st.markdown(
    """
    Welcome to my interactive AI‑Portfolio!

    This app gives a glimpse into how I integrate AI — blending LLMs and (backend-)engineering into prototypes that can scale into real products.

    What you can do here:
    - Chat with an AI about my background, projects, and skills.
    - Browse and download my CV as a PDF.
    - Explore the source code on GitHub and connect on LinkedIn via the links in the left sidebar.

    Under the hood:
    - Frontend: Streamlit
    - API: FastAPI
    - LLM: OpenAI Chat Completions (tool‑calling)
    - Architecture: Clean Architecture (domain • use cases • adapters)

    If you’re interested in me or my work, I’d love to hear from you.
    """
)
