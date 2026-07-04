# FastAPI Foundation Migration

## Goal
Replace the current Flask foundation with a clean FastAPI backend.

## Run locally

```bash
cd backend
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

Open:
- http://127.0.0.1:8000/
- http://127.0.0.1:8000/health
- http://127.0.0.1:8000/missions
- http://127.0.0.1:8000/docs

## Commit

```bash
git checkout -b feature/fastapi-foundation
git add backend/app backend/requirements.txt backend/.env.example README_FASTAPI_MIGRATION.md
git commit -m "refactor: migrate api foundation to FastAPI"
git push -u origin feature/fastapi-foundation
```
