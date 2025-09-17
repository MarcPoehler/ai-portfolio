import streamlit as st
from sidebar import render_common_sidebar

def _get_allowed_credentials():
    usernames = st.secrets.get("VALID_USERNAMES", [])
    password = st.secrets.get("VALID_PASSWORDS", None)
    return usernames, password

allowed_users, allowed_password = _get_allowed_credentials()

# Access gate (validate before rendering)
if "auth_gate" not in st.session_state:
    with st.form("auth_gate_form", clear_on_submit=False):
        st.markdown("### Please enter your access details")
        input_user = st.text_input("User", key="auth_user", autocomplete="username")
        input_password = st.text_input("Password", key="auth_password", type="password", autocomplete="current-password")
        submitted = st.form_submit_button("Sign in")
        if submitted:
            errors = []
            if allowed_users and input_user not in allowed_users:
                errors.append("Unknown user")
                st.error("Unknown user")
            if allowed_password is not None and input_password != allowed_password:
                errors.append("Invalid password")
                st.error("Invalid password")
            elif not errors:
                st.session_state.auth_gate = {"user": input_user, "password": input_password}
                st.rerun()
    if "auth_gate" not in st.session_state:
        st.stop()

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
