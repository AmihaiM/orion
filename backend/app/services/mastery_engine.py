from datetime import datetime, timezone
from app.db.supabase import get_supabase

MAX_ATTEMPTS_PER_SENTENCE = 5


def evaluate_mastery_decision(scoring: dict, previous_attempts: list[dict]) -> dict:
    failed_before = sum(1 for a in previous_attempts if a.get("passed") is False)
    passed_before = sum(1 for a in previous_attempts if a.get("passed") is True)
    attempt_number = len(previous_attempts) + 1

    if scoring["passed"]:
        if failed_before > 0:
            total_passes_after_failures = passed_before + 1
            required_passes = failed_before + 1

            if total_passes_after_failures < required_passes:
                remaining = required_passes - total_passes_after_failures
                return {
                    "attempt_number": attempt_number,
                    "next_action": "RETRY_SENTENCE",
                    "needs_review": False,
                    "mastered": False,
                    "mastery_status": "reinforcement",
                    "message": f"Excellent correction! Repeat it {remaining} more time(s) to make it stick 💪",
                }

        return {
            "attempt_number": attempt_number,
            "next_action": "NEXT_SENTENCE",
            "needs_review": False,
            "mastered": True,
            "mastery_status": "mastered",
            "message": "Excellent! Great speaking. Let's continue 🚀",
        }

    if attempt_number >= MAX_ATTEMPTS_PER_SENTENCE:
        return {
            "attempt_number": attempt_number,
            "next_action": "NEXT_SENTENCE",
            "needs_review": True,
            "mastered": False,
            "mastery_status": "needs_review",
            "message": "Good effort. We'll review this sentence again later 💪",
        }

    return {
        "attempt_number": attempt_number,
        "next_action": "RETRY_SENTENCE",
        "needs_review": False,
        "mastered": False,
        "mastery_status": "in_progress",
        "message": "Good try. Stay on this sentence and try again 😊",
    }


def update_sentence_result(payload, scoring, decision):
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

    previous_total = current.get("total_attempts", 0) if current else 0
    previous_practice = current.get("practice_attempts", 0) if current else 0
    previous_best = current.get("best_accuracy_score", 0) if current else 0

    data = {
        "student_id": str(payload.student_id),
        "exercise_id": str(payload.mission_id),
        "sentence_id": str(payload.sentence_id),
        "session_id": str(payload.session_id),
        "practice_attempts": previous_practice + 1,
        "total_attempts": previous_total + 1,
        "best_accuracy_score": max(previous_best or 0, scoring["accuracy_score"]),
        "mastery_status": decision["mastery_status"],
        "fluency_status": "ok" if decision["mastered"] else "needs_practice",
        "mastered": decision["mastered"],
        "finished_at": datetime.now(timezone.utc).isoformat()
        if decision["mastered"] or decision["needs_review"]
        else None,
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