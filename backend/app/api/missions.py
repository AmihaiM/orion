from uuid import UUID
from fastapi import APIRouter, HTTPException
from app.db.supabase import get_supabase
from app.schemas.mission import MissionDetail, MissionsResponse

router = APIRouter(prefix="/missions", tags=["missions"])


@router.get("", response_model=MissionsResponse)
def list_missions():
    try:
        db = get_supabase()
        res = (
            db.table("exercises")
            .select("id,title,level,unit,source_type,visibility,created_at")
            .order("created_at", desc=True)
            .execute()
        )
        return {"missions": res.data or []}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/{mission_id}", response_model=MissionDetail)
def get_mission(mission_id: UUID):
    try:
        db = get_supabase()
        mission_res = (
            db.table("exercises")
            .select("id,title,level,unit,source_type,visibility,created_at")
            .eq("id", str(mission_id))
            .execute()
        )

        if not mission_res.data:
            raise HTTPException(status_code=404, detail="Mission not found")

        sentences_res = (
            db.table("sentences")
            .select("id,sentence_order,english_text,hebrew_text,difficulty,tags")
            .eq("exercise_id", str(mission_id))
            .order("sentence_order")
            .execute()
        )

        return {"mission": mission_res.data[0], "sentences": sentences_res.data or []}
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
