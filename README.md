# AI Portfolio – Interactive Candidate Showcase

An end‑to‑end, minimal yet production‑ready showcase of an AI Software Engineer profile. Visitors chat with a model grounded in curated profile data, explore a CV, view skill stats, and get dynamic follow‑up questions – all while applying pragmatic safeguards (PII handling, validation, clean architecture, JSON‑structured LLM responses).

> FastAPI backend + Streamlit frontend. Clean boundaries. Human‑friendly answers. Small footprint. Easy to deploy.

---
## ✨ Highlights
- **Conversational Profile Chat** – Answers always in first‑person voice ("I") with curated highlights.
- **Follow‑Up Question Suggestions** – Injected after each answer (backend logic, not LLM hallucination).
- **Profile Grounding** – Combines narrative markdown + structured JSON.
- **PII Policy** – Regex detector; block or mask based on severity threshold (configurable).
- **Strict JSON LLM Contract** – Schema‑validated responses reduce parsing surprises.
- **Separation of Concerns** – Domain ports, use cases, infrastructure adapters, presentation layer.
- **Fast Startup & Lean Dependencies** – No ORM, no database, file‑based profile.
- **Deploy Friendly** – Works on Render (backend) + Streamlit Cloud (frontend) out of the box.

---
## 🧱 Architecture Overview
```
frontend/ (Streamlit) --> calls --> FastAPI /v1/chat
                                           |
                           +-------------------------------+
                           |  Application Layer            |
User Input --> Controller -> Use Case (AnswerQuestion) ----> LLM Service (OpenAI)
                           |        |                       ^
                           |        +-> PII Processing      |
                           |        +-> Follow-up selection |
                           +-------------------------------+
                                  |                
                                  v
                             Profile Repository (file-based)
```
Supporting layers:
- `domain/` – Entities + errors + ports (LLM, profile repo, PII detector)
- `infrastructure/` – OpenAI client + regex PII detector + file repo
- `application/` – Use cases + follow-up selection
- `presentation/` – FastAPI router + error handlers
- `frontend/` – Streamlit pages (chat, CV, stats)

---
## ⚙️ Tech Stack
| Layer      | Tools |
|------------|-------|
| Backend    | FastAPI, Uvicorn, Pydantic v2, OpenAI SDK, Tenacity |
| Frontend   | Streamlit (multi‑page + navigation), Requests |
| Testing    | Pytest |
| Infra Ops  | Render, Streamlit Cloud |

---
## 🚀 Quick Start (Local)
Backend (API):
```
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...   # set your key
uvicorn start:app --reload
```
Frontend (Streamlit):
```
cd frontend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export BACKEND_URL=http://127.0.0.1:8000
streamlit run streamlit_app.py
```
Visit: http://localhost:8501

---
## 🧠 LLM Response Contract
Backend sends a system prompt enforcing a JSON schema derived from the `Answer` Pydantic model:
```json
{
  "type": "object",
  "properties": {
    "answer": {"type": "string"},
    "highlights": {"type": "array"},
    "follow_up_questions": {"type": "array"}
  },
  "required": ["answer","highlights","follow_up_questions"]
}
```
If decoding fails, raw content is wrapped into a fallback `Answer` with empty arrays.

---
## 🛣️ Possible Next Steps
- Add analytics/logging (token counts, latency histograms)
- Rate limiting / API key auth layer
- Deterministic follow-up selection (avoid repeats)
- Richer skill stats (charts powered from structured profile JSON)
- Multi-model fallback or streaming responses

---
## 📄 License
MIT (see `LICENSE`).

---
## 🙌 Acknowledgements
Built as a concise demonstration of clean layering + LLM grounding with minimal overhead.

Enjoy exploring.