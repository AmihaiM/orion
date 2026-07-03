from flask import Blueprint, request, jsonify
from services.speech_engine import accuracy
from services.mastery_engine import MasteryEngine, MasteryInput

bp = Blueprint("attempts", __name__, url_prefix="/api/attempts")


@bp.post("/score")
def score_attempt():
    data = request.get_json(force=True)
    expected = data.get("expected_text", "")
    spoken = data.get("spoken_text", "")
    attempt_number = int(data.get("attempt_number", 1))

    acc = accuracy(expected, spoken)
    # placeholder until audio timing is integrated
    fluency_score = float(data.get("fluency_score", 80))
    pause_score = float(data.get("pause_score", 80))

    mastery = MasteryEngine().calculate(MasteryInput(acc, fluency_score, pause_score, attempt_number))
    return jsonify({
        "accuracy_score": acc,
        "spoken_text": spoken,
        **mastery,
    })
