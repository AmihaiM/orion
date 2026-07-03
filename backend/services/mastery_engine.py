from dataclasses import dataclass


@dataclass
class MasteryInput:
    accuracy_score: float
    fluency_score: float
    pause_score: float
    attempt_number: int


class MasteryEngine:
    """Domain-agnostic mastery scoring.

    Speech recognition is infrastructure. Mastery is calculated here.
    """

    def calculate(self, data: MasteryInput) -> dict:
        retry_score = max(0, 100 - ((data.attempt_number - 1) * 15))
        mastery_score = (
            data.accuracy_score * 0.45
            + data.fluency_score * 0.25
            + data.pause_score * 0.15
            + retry_score * 0.15
        )
        mastered = mastery_score >= 85 and data.accuracy_score >= 85
        return {
            "mastery_score": round(mastery_score, 2),
            "mastered": mastered,
            "retry_score": retry_score,
        }
