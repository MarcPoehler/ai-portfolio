import streamlit as st
import pandas as pd
import json
import os
from sidebar import render_common_sidebar


DATA_FILE = os.path.join("data", "skills", "skills.json")

@st.cache_data(show_spinner=False)
def load_skills(path: str) -> pd.DataFrame:
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    # Basic validation
    if "categories" not in raw or not isinstance(raw["categories"], list):
        raise ValueError("skills.json missing 'categories' list")
    rows = []
    for category_index, category in enumerate(raw["categories"]):
        name = category.get("name")
        skills = category.get("skills", [])
        if not name or not isinstance(skills, list):
            raise ValueError("Invalid category entry")
        for skill_item in skills:
            skill_name = skill_item.get("name")
            lvl = skill_item.get("level")
            if not skill_name or not isinstance(lvl, int) or not (1 <= lvl <= 5):
                raise ValueError(f"Invalid skill entry in category '{name}'")
            rows.append({"category": name, "skill": skill_name, "level": lvl, "category_order": category_index})
    df_local = pd.DataFrame(rows)
    return df_local

def render_dots(level: int, max_dots: int = 5) -> str:
    filled = max(0, min(max_dots, int(level)))
    empty = max_dots - filled
    return " ".join(["●"] * filled + ["○"] * empty)

def render_category(category_name: str):
    st.subheader(category_name)
    sub = df[df["category"] == category_name].sort_values("skill")
    for row in sub.itertuples():
        c1, c2 = st.columns([2,1])
        with c1:
            st.write(row.skill)
        with c2:
            st.write(render_dots(int(row.level)))

# Gate check
if "auth_gate" not in st.session_state:
    st.warning("Please sign in on the Welcome page first.")
    st.stop()

# Entry point
st.set_page_config(page_title="Skills", page_icon="📊", layout="wide")
st.title("📊 Skill Stats")
st.caption(
    "Self‑assessed proficiency across my core focus areas: AI & LLM Engineering and Backend."
)
render_common_sidebar()
st.divider()


try:
    df = load_skills(DATA_FILE)
except Exception as e:  # noqa: BLE001
    st.error(f"Failed to load skills data: {e}")
    st.stop()

categories_ordered = list(df.sort_values(["category_order", "category"])["category"].unique())
mid = (len(categories_ordered) + 1) // 2
left_categories = categories_ordered[:mid]
right_categories = categories_ordered[mid:]

col_left, col_right = st.columns(2, gap="large")

with col_left:
    for category in left_categories:
        render_category(category)
with col_right:
    for category in right_categories:
        render_category(category)
