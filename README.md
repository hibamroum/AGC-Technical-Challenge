# Women’s Public Safety Assistant (FastAPI + Mistral)

Issue: **Women’s safety in public spaces** (streets, transit, etc.).

## Endpoints
- `POST /api/v1/chat` — ask a safety question (WRITE)
- `GET  /api/v1/history` — read session history (READ)
- `DELETE /api/v1/history` — clear session history
- `GET  /healthz` — liveness

**Headers**
- `X-Session-Id: <your-session-id>` (recommended for saving chat)

## Run
```bash
cp .env.example .env   # fill MISTRAL_API_KEY
pip install -r requirements.txt
uvicorn app.main:app --reload
