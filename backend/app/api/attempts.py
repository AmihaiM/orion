from fastapi import APIRouter, HTTPException

from app.db.supabase import get_supabase
from app.schemas.attempt import CreateAttemptRequest, AttemptResponse

router = APIRouter(prefix="/attempts", tags=["attempts"])


@router.post("", response_model=AttemptResponse)
def create_attempt(payload: CreateAttemptRequest):
    supabase = get_supabase()

    insert_payload = {
        "student_id": str(payload.student_id),
        "exercise_id": str(payload.mission_id),
        "sentence_id": str(payload.sentence_id),
        "session_id": str(payload.session_id),
        "stage": payload.stage,
        "spoken_text": payload.spoken_text,
        "accuracy_score": payload.accuracy_score,
        "passed": payload.passed,
        "recording_duration_ms": payload.recording_duration_ms,
        "silence_ms": payload.silence_ms,
        "words_per_minute": payload.words_per_minute,
        "fluency_status": payload.fluency_status,
    }

    res = supabase.table("learning_attempts").insert(insert_payload).execute()

    if not res.data:
        raise HTTPException(status_code=500, detail="Failed to create attempt")

    row = res.data[0]

    return {
        "id": row["id"],
        "student_id": row["student_id"],
        "mission_id": row["exercise_id"],
        "sentence_id": row["sentence_id"],
        "session_id": row["session_id"],
        "stage": row["stage"],
        "spoken_text": row.get("spoken_text"),
        "accuracy_score": row.get("accuracy_score"),
        "passed": row.get("passed"),
        "fluency_status": row.get("fluency_status"),
        "created_at": row["created_at"],
    }