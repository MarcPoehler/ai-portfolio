AI Portfolio Backend (FastAPI + Clean Architecture)
=================================================

Minimal backend powering the interactive AI portfolio chat. It exposes a single chat endpoint that enriches a user question with profile context and obtains a structured answer from an OpenAI model.

Status: short‑lived demo / showcase (not intended for long‑term production). Robustness measures are intentionally lightweight.

---
Table of Contents
-----------------
1. Features
2. Architecture Overview
3. API
4. Project Structure
5. Roadmap (Light)
6. License

---
1. Features
-----------
* FastAPI service with a single `/v1/chat` JSON endpoint
* Clean Architecture layering: domain → application (use case) → infrastructure → presentation
* PII detection (simple regex) with blocking + masking
* Deterministic structured LLM output (JSON) via pydantic schema coercion fallback
* Follow‑up question suggestions (static catalog + random selection)

Non‑Goals (for this demo): advanced logging, tracing, persistence, auth, rate limiting.

---
2. Architecture Overview
------------------------
Layer responsibilities:
* domain: pure entities, errors, ports (interfaces)
* application: use case orchestration + DTOs + suggestion logic
* infrastructure: concrete adapters (OpenAI service, file repository, regex PII)
* presentation: FastAPI router + exception mapping
* container: wiring / dependency assembly

Flow (happy path):
`POST /v1/chat` → controller → use case → repository (profile context) → optional PII masking → OpenAI service → structured Answer → follow‑ups added → response DTO.

---
3. API
------
### Chat
`POST /v1/chat`
Request:
```json
{ "message": "How do you align technical design with business impact?" }
```
Successful Response:
```json
{
	"answer": "I align design...",
	"highlights": ["Impact tracking", "Stakeholder mapping"],
	"follow_up_questions": ["What metrics do you define?", "How do you validate?", "An example iteration?"]
}
```
PII Block (example):
```json
{
	"detail": {
		"error": "PII_BLOCKED",
		"message": "Input contains disallowed PII",
		"findings": [ {"category": "EMAIL", "value": "..."} ]
	}
}
```

---
4. Project Structure
--------------------
```
backend/
	application/
	domain/
	infrastructure/
	presentation/
	container.py
	config.py
start.py          # FastAPI app factory
```

---
5. Roadmap (Light)
------------------
Short‑lived project; only consider if extending:
* Deterministic seed for follow‑up selection
* Streaming responses
* Basic request logging & metrics
* Auth (API key) if publicly exposed longer

---
6. License
----------
See `LICENSE` (MIT).

---
Questions / Contact
-------------------
See Streamlit sidebar for contact links.

