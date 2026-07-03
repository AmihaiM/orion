from flask import Blueprint, jsonify, request
from services.supabase_client import get_supabase
from services.scoring import accuracy_score, word_feedback, fluency_metrics

learning_bp = Blueprint("learning", __name__)

@learning_bp.post("/attempt")
def record_attempt():
    data = request.get_json(force=True)
    student_id = data.get("student_id")
    exercise_id = data.get("exercise_id")
    sentence_id = data.get("sentence_id")
    stage = data.get("stage", "practice")
    spoken = data.get("spoken_text", "")
    duration_ms = int(data.get("duration_ms") or 0)
    silence_ms = int(data.get("silence_ms") or 0)
    threshold = int(data.get("threshold") or 85)

    if not all([student_id, exercise_id, sentence_id]):
        return jsonify({"error": "student_id_exercise_id_sentence_id_required"}), 400

    sb = get_supabase()
    sent = sb.table("sentences").select("english_text").eq("id", sentence_id).single().execute().data
    target = sent["english_text"]
    score = accuracy_score(spoken, target)
    passed = score >= threshold
    fluency = fluency_metrics(spoken, duration_ms, silence_ms)

    row = {
        "student_id": student_id,
        "exercise_id": exercise_id,
        "sentence_id": sentence_id,
        "stage": stage,
        "spoken_text": spoken,
        "accuracy_score": score,
        "passed": passed,
        "recording_duration_ms": duration_ms,
        "silence_ms": silence_ms,
        "words_per_minute": fluency["words_per_minute"],
        "fluency_status": fluency["fluency_status"],
    }
    saved = sb.table("learning_attempts").insert(row).execute().data[0]
    return jsonify({
        "attempt": saved,
        "target": target,
        "score": score,
        "passed": passed,
        "words": word_feedback(spoken, target),
        **fluency,
    })
