import streamlit as st


def render_common_sidebar() -> None:
    """Render the common sidebar with Contacts and Focus areas."""
    with st.sidebar:
        st.image("data/Headshot_Marc_Poehler.jpeg")
        st.subheader("Marc Pöhler – AI Software Engineer")
        st.subheader("Contact")
        st.link_button("📧 Email", "mailto:marcpoehler@aol.com")
        st.link_button("💼 LinkedIn", "https://www.linkedin.com/in/marc-poehler")
        st.link_button("💻 GitHub", "https://github.com/MarcPoehler/ai-portfolio")
        st.divider()
        st.subheader("Availability")
        st.markdown(
            "- 🔎 Open to: **AI Software Engineer / Backend Engineer (GenAI) / Prompt Engineer / AI Consultant**\n"
            "- 📍 Base: **St. Gallen**\n"
            "- 🏢 On-site: **Zürich, St. Gallen, Winterthur**\n"
            "- 🗣️ Languages: **English, German**"
        )
