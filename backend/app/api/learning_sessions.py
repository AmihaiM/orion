from fastapi import APIRouter, HTTPException

from app.db.supabase import get_supabase
from app.schemas.learning_session import (
    CreateLearningSessionRequest,
    LearningSessionResponse,
)

router = APIRouter(prefix="/learning-sessions", tags=["learning_sessions"])


@router.post("", response_model=LearningSessionResponse)
def create_learning_session(payload: CreateLearningSessionRequest):
    supabase = get_supabase()

    student_res = (
        supabase.table("app_users")
        .select("id,role")
        .eq("id", str(payload.student_id))
        .eq("role", "student")
        .execute()
    )

    if not student_res.data:
        raise HTTPException(status_code=404, detail="Student not found")

    mission_res = (
        supabase.table("exercises")
        .select("id,title")
        .eq("id", str(payload.mission_id))
        .execute()
    )

    if not mission_res.data:
        raise HTTPException(status_code=404, detail="Mission not found")

    insert_payload = {
        "student_id": str(payload.student_id),
        "exercise_id": str(payload.mission_id),
        "assignment_id": str(payload.assignment_id) if payload.assignment_id else None,
        "status": "active",
    }

    session_res = (
        supabase.table("learning_sessions")
        .insert(insert_payload)
        .execute()
    )

    if not session_res.data:
        raise HTTPException(status_code=500, detail="Failed to create session")

    row = session_res.data[0]

    return {
        "id": row["id"],
        "student_id": row["student_id"],
        "mission_id": row["exercise_id"],
        "assignment_id": row.get("assignment_id"),
        "status": row["status"],
        "started_at": row["started_at"],
    }