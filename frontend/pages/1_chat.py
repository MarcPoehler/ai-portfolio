import os
import json
from pathlib import Path
import requests
import streamlit as st
from sidebar import render_common_sidebar


# Resolve backend base URL (priority: Streamlit secrets -> env var -> localhost fallback)
BACKEND_URL = (
    (st.secrets.get("BACKEND_URL") if hasattr(st, "secrets") else None)
    or os.getenv("BACKEND_URL")
    or "http://127.0.0.1:8000"
)

# Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Avatars
_data_dir = Path(__file__).resolve().parents[2] / "data"
_avatar = _data_dir / "thinking_bitmoji.webp"
ASSISTANT_AVATAR = str(_avatar) if _avatar.exists() else "🤖"
USER_AVATAR = "🧑‍💻"


# Helper Functions
def full_width_columns(n: int):
    """Create columns that stretch the available width.

    """
    return st.columns(n, gap="small", width="stretch")

def stretch_button(label: str, **kwargs):
    """Button that stretches container width."""
    return st.button(label, width="stretch", **kwargs)

def send_sync(prompt: str) -> dict:
    """Send prompt; gracefully handle PII blocking (400)."""
    r = requests.post(
        f"{BACKEND_URL}/v1/chat",
        headers={"Content-Type": "application/json"},
        data=json.dumps({"message": prompt}),
        timeout=120,
    )
    if r.status_code == 400:
        try:
            detail = r.json().get("detail", {})
        except Exception:
            detail = {}
        if detail.get("error") == "PII_BLOCKED":
            return {"pii_blocked": True, **detail}
    r.raise_for_status()
    return r.json()

def _render_pii_warning(detail: dict):
    findings = detail.get("findings", [])
    cats = sorted({f.get("category", "UNKNOWN") for f in findings})
    cat_str = ", ".join(cats) if cats else "(unspecified)"
    msg = detail.get("message", "Input contains disallowed PII")
    st.warning(f"{msg}. Categories: {cat_str}. Your input was not sent to the model.")

def process_prompt(prompt: str):
    """Queue a user (or follow-up) prompt and create a stable assistant placeholder.

    This avoids layout shift: we append a pending assistant message first, then on the next
    script run we perform the API call inside that reserved bubble.
    """

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.messages.append({
        "role": "assistant",
        "content": "",
        "pending": True,
    })

    st.session_state.pending_prompt = prompt
    st.session_state.pending_in_progress = False
    st.rerun()


# Entry point
st.set_page_config(page_title="Chat with me!", page_icon="💬", layout="wide")
st.title("💬 Chat with me!")
st.caption(
    "This chatbot has extended knowledge of my work as an AI Software Engineer and earlier experience. Ask everything you like. Just make sure to be appropriate and don't share sensitive data."
)
render_common_sidebar()
st.divider()

# Suggestionss
if not any(m.get("role") == "user" for m in st.session_state.messages):
    st.markdown("#### 💡 Suggestions")

    example_prompts = [
        "How did you enable AI‑assisted content production at simpleclub?",
        "How do you align technical design with business impact?",
        "Describe the free‑text evaluation or media asset generation prototypes you built.",
    ]

    BUTTON_HEIGHT = 84
    st.markdown(
        f"""
        <style>
        /* Inside .suggestion-wrap only: make all st.button same height, centered, wrapping */
        .suggestion-wrap div.stButton > button {{
            height: {BUTTON_HEIGHT}px;
            width: 100%;
            white-space: normal;
        overflow-wrap: anywhere;   /* break very long words */
        display: flex;
        align-items: center;       /* center vertically */
        justify-content: center;   /* center horizontally */
            text-align: center;
            padding: 8px 12px;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="suggestion-wrap">', unsafe_allow_html=True)
    PER_ROW = 3
    rows = [example_prompts[i:i+PER_ROW] for i in range(0, len(example_prompts), PER_ROW)]

    for r, row in enumerate(rows):
        cols = full_width_columns(PER_ROW)
        for c, prompt in enumerate(row):
            key = f"sugg_{r}_{c}"
            with cols[c]:
                if stretch_button(prompt, key=key):
                    process_prompt(prompt)
    st.markdown('</div>', unsafe_allow_html=True)


# Chat History & Follow-up Buttons
last_assistant_index = None
for index in reversed(range(len(st.session_state.messages))):
    if st.session_state.messages[index]["role"] == "assistant":
        last_assistant_index = index
        break

pending_index = None
for index, m in enumerate(st.session_state.messages):
    if m.get("pending") and m.get("role") == "assistant":
        pending_index = index
        break

for index, m in enumerate(st.session_state.messages):
    if m["role"] == "assistant":
        if m.get("pending"):
            with st.chat_message("assistant", avatar=ASSISTANT_AVATAR):
                if not st.session_state.get("pending_in_progress"):
                    st.session_state.pending_in_progress = True
                    with st.spinner("Thinking…"):
                        try:
                            resp = send_sync(st.session_state.get("pending_prompt", ""))
                            if resp.get("pii_blocked"):
                                _render_pii_warning(resp)
                                st.session_state.messages.pop(index)
                            else:
                                answer = resp.get("answer", "")
                                highlights = resp.get("highlights", []) or []
                                followups = resp.get("follow_up_questions", []) or []
                                st.session_state.messages[index] = {
                                    "role": "assistant",
                                    "content": answer,
                                    "highlights": highlights,
                                    "follow_up_questions": followups,
                                }
                        except Exception as e:
                            st.session_state.messages[index] = {
                                "role": "assistant",
                                "content": f"⚠️ Error: {e}",
                            }
                        finally:
                            # Clean flags
                            st.session_state.pop("pending_prompt", None)
                            st.session_state.pending_in_progress = False
                    st.rerun()
                else:
                    with st.spinner("Thinking…"):
                        st.write("")
        else:
            with st.chat_message("assistant", avatar=ASSISTANT_AVATAR):
                st.markdown(m.get("content", ""))
                if m.get("highlights"):
                    with st.expander("Highlights", expanded=False):
                        for h in m["highlights"]:
                            st.markdown(f"- {h}")
                # Only render follow-ups for latest finalized assistant message (no pending)
                if index == last_assistant_index and pending_index is None:
                    followups = m.get("follow_up_questions") or []
                    if followups:
                        st.markdown("#### Follow-up questions")
                        cols = full_width_columns(len(followups)) if len(followups) <= 3 else None
                        for item, follow_up_question in enumerate(followups):
                            key = f"followup_{index}_{item}"
                            if cols:
                                with cols[item]:
                                    if stretch_button(follow_up_question, key=key):
                                        process_prompt(follow_up_question)
                            else:
                                if stretch_button(follow_up_question, key=key):
                                    process_prompt(follow_up_question)
    else:
        with st.chat_message("user", avatar=USER_AVATAR):
            st.markdown(m.get("content", ""))

# Chat input
if user_input := st.chat_input("Ask something about the candidate…"):
    process_prompt(user_input)
