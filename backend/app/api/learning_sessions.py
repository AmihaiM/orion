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
@router.get("/{session_id}/next")
def get_next_learning_step(session_id: str):
    supabase = get_supabase()

    session_res = (
        supabase.table("learning_sessions")
        .select("id, student_id, exercise_id, status")
        .eq("id", session_id)
        .execute()
    )

    if not session_res.data:
        raise HTTPException(status_code=404, detail="Session not found")

    session = session_res.data[0]
    mission_id = session["exercise_id"]
    student_id = session["student_id"]

    sentences_res = (
        supabase.table("sentences")
        .select("id, sentence_order, english_text, hebrew_text, difficulty, tags")
        .eq("exercise_id", mission_id)
        .order("sentence_order")
        .execute()
    )

    sentences = sentences_res.data or []

    if not sentences:
        raise HTTPException(status_code=404, detail="No sentences found for mission")

    results_res = (
        supabase.table("sentence_results")
        .select("*")
        .eq("session_id", session_id)
        .eq("student_id", student_id)
        .eq("exercise_id", mission_id)
        .execute()
    )

    results_by_sentence = {
        row["sentence_id"]: row for row in (results_res.data or [])
    }

    for sentence in sentences:
        result = results_by_sentence.get(sentence["id"])

        if not result:
            return {
                "session_id": session_id,
                "mission_id": mission_id,
                "next_action": "SHOW_SENTENCE",
                "reason": "not_started",
                "sentence": sentence,
                "progress": {
                    "total_sentences": len(sentences),
                    "mastered_count": sum(
                        1 for r in results_by_sentence.values()
                        if r.get("mastered") is True
                    ),
                },
            }

        if result.get("mastered") is not True and result.get("mastery_status") != "needs_review":
            return {
                "session_id": session_id,
                "mission_id": mission_id,
                "next_action": "RETRY_SENTENCE",
                "reason": "in_progress",
                "sentence": sentence,
                "sentence_result": result,
                "progress": {
                    "total_sentences": len(sentences),
                    "mastered_count": sum(
                        1 for r in results_by_sentence.values()
                        if r.get("mastered") is True
                    ),
                },
            }

    review_items = [
        sentence for sentence in sentences
        if results_by_sentence.get(sentence["id"], {}).get("mastery_status") == "needs_review"
    ]

    if review_items:
        return {
            "session_id": session_id,
            "mission_id": mission_id,
            "next_action": "REVIEW_SENTENCE",
            "reason": "review_queue",
            "sentence": review_items[0],
            "progress": {
                "total_sentences": len(sentences),
                "mastered_count": sum(
                    1 for r in results_by_sentence.values()
                    if r.get("mastered") is True
                ),
            },
        }

    return {
        "session_id": session_id,
        "mission_id": mission_id,
        "next_action": "MISSION_COMPLETED",
        "reason": "all_sentences_mastered",
        "sentence": None,
        "progress": {
            "total_sentences": len(sentences),
            "mastered_count": len(sentences),
        },
        "message": "Mission completed! Excellent work 🎉",
    }