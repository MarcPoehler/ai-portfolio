import streamlit as st


nav = st.navigation([
    st.Page("pages/0_welcome.py", title="Welcome!", icon="👋"),
    st.Page("pages/1_chat.py", title="Chat with me!", icon="💬"),
    st.Page("pages/2_cv.py", title="Curriculum Vitae", icon="📄"),
    st.Page("pages/3_stats.py", title="Skill Stats", icon="📊"),
])

nav.run()
