from pydantic import BaseModel


class MasteryInput(BaseModel):
    accuracy_score: int
    fluency_score: int = 100
    pause_penalty: int = 0
    attempt_number: int = 1


class MasteryResult(BaseModel):
    mastery_score: int
    mastered: bool


def calculate_mastery(data: MasteryInput, threshold: int = 85) -> MasteryResult:
    retry_penalty = max(0, (data.attempt_number - 1) * 5)
    score = round(
        data.accuracy_score * 0.55
        + data.fluency_score * 0.25
        + max(0, 100 - data.pause_penalty) * 0.10
        + max(0, 100 - retry_penalty) * 0.10
    )
    return MasteryResult(mastery_score=score, mastered=score >= threshold)
