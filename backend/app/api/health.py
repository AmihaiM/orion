from fastapi import APIRouter, HTTPException
from app.db.supabase import get_supabase

router = APIRouter(tags=["health"])


@router.get("/health")
def health():
    try:
        db = get_supabase()
        db.table("organizations").select("id").limit(1).execute()
        return {"api": "ok", "supabase": "ok"}
    except Exception as exc:
        raise HTTPException(status_code=500, detail={"api": "ok", "supabase": "failed", "error": str(exc)})
