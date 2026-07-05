from datetime import datetime, timezone
from app.db.supabase import get_supabase

MAX_ATTEMPTS_PER_SENTENCE = 5


def update_sentence_result(payload, scoring, attempt_number, decision):
    supabase = get_supabase()

    existing = (
        supabase.table("sentence_results")
        .select("*")
        .eq("student_id", str(payload.student_id))
        .eq("exercise_id", str(payload.mission_id))
        .eq("sentence_id", str(payload.sentence_id))
        .eq("session_id", str(payload.session_id))
        .execute()
    )

    current = existing.data[0] if existing.data else None

    best_score = max(
        current.get("best_accuracy_score") or 0 if current else 0,
        scoring["accuracy_score"],
    )

    total_attempts = (current.get("total_attempts") or 0 if current else 0) + 1
    practice_attempts = (current.get("practice_attempts") or 0 if current else 0) + 1

    mastered = scoring["passed"]
    needs_review = decision["needs_review"]

    mastery_status = (
        "mastered" if mastered else
        "needs_review" if needs_review else
        "in_progress"
    )

    data = {
        "student_id": str(payload.student_id),
        "exercise_id": str(payload.mission_id),
        "sentence_id": str(payload.sentence_id),
        "session_id": str(payload.session_id),
        "practice_attempts": practice_attempts,
        "total_attempts": total_attempts,
        "best_accuracy_score": best_score,
        "mastery_status": mastery_status,
        "fluency_status": "ok" if mastered else "needs_practice",
        "mastered": mastered,
        "finished_at": datetime.now(timezone.utc).isoformat() if mastered or needs_review else None,
    }

    if current:
        res = (
            supabase.table("sentence_results")
            .update(data)
            .eq("id", current["id"])
            .execute()
        )
    else:
        res = supabase.table("sentence_results").insert(data).execute()

    return res.data[0] if res.data else data