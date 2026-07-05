from fastapi import APIRouter, HTTPException
from app.services.mastery_engine import update_sentence_result

from app.db.supabase import get_supabase
from app.schemas.attempt import CreateAttemptRequest, AttemptResponse
from app.services.scoring_engine import (
    score_sentence,
    decide_next_action,
    praise_message,
)

router = APIRouter(prefix="/attempts", tags=["attempts"])


@router.post("")
def create_attempt(payload: CreateAttemptRequest):
    supabase = get_supabase()

    sentence_res = (
        supabase.table("sentences")
        .select("id, english_text")
        .eq("id", str(payload.sentence_id))
        .execute()
    )

    if not sentence_res.data:
        raise HTTPException(status_code=404, detail="Sentence not found")

    expected_text = sentence_res.data[0]["english_text"]

    previous_attempts_res = (
        supabase.table("learning_attempts")
        .select("id")
        .eq("session_id", str(payload.session_id))
        .eq("sentence_id", str(payload.sentence_id))
        .execute()
    )

    attempt_number = len(previous_attempts_res.data or []) + 1

    scoring = score_sentence(
        expected_text=expected_text,
        spoken_text=payload.spoken_text or "",
    )

    decision = decide_next_action(
        passed=scoring["passed"],
        attempt_number=attempt_number,
    )

    message = praise_message(
        passed=scoring["passed"],
        attempt_number=attempt_number,
        needs_review=decision["needs_review"],
    )

    insert_payload = {
        "student_id": str(payload.student_id),
        "exercise_id": str(payload.mission_id),
        "sentence_id": str(payload.sentence_id),
        "session_id": str(payload.session_id),
        "stage": payload.stage,
        "spoken_text": payload.spoken_text,
        "accuracy_score": scoring["accuracy_score"],
        "passed": scoring["passed"],
        "recording_duration_ms": payload.recording_duration_ms,
        "silence_ms": payload.silence_ms,
        "words_per_minute": payload.words_per_minute,
        "fluency_status": "needs_review" if decision["needs_review"] else "ok",
    }

    res = supabase.table("learning_attempts").insert(insert_payload).execute()

    if not res.data:
        raise HTTPException(status_code=500, detail="Failed to create attempt")

    row = res.data[0]
    
    sentence_result = update_sentence_result(
    payload=payload,
    scoring=scoring,
    attempt_number=attempt_number,
    decision=decision,
)

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
        "attempt_number": attempt_number,
        "next_action": decision["next_action"],
        "needs_review": decision["needs_review"],
        "message": message,
        "missing_words": scoring["missing_words"],
        "extra_words": scoring["extra_words"],
        "sentence_result": sentence_result,
    }