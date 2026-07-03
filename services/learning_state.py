from dataclasses import dataclass, asdict
from enum import Enum

class LearningStage(str, Enum):
    DISCOVER = "discover"
    PRACTICE = "practice"
    MASTER_CHALLENGE = "master_challenge"
    FINAL_EXAM = "final_exam"
    COMPLETE = "complete"

@dataclass
class SentenceState:
    stage: LearningStage = LearningStage.DISCOVER
    practice_attempts: int = 0
    cloze_attempts: int = 0
    mastery_attempts: int = 0
    total_attempts: int = 0
    threshold: int = 85
    max_attempts: int = 5
    accuracy_score: int = 0
    fluency_status: str = "unknown"
    mastery_status: str = "not_started"

    def to_dict(self):
        d = asdict(self)
        d["stage"] = self.stage.value
        return d


def next_stage_after_attempt(state: SentenceState, passed: bool) -> SentenceState:
    state.total_attempts += 1
    if state.stage == LearningStage.DISCOVER:
        state.stage = LearningStage.PRACTICE
        return state

    if state.stage == LearningStage.PRACTICE:
        state.practice_attempts += 1
        if passed:
            state.mastery_status = "practice_passed"
            state.stage = LearningStage.MASTER_CHALLENGE
        elif state.total_attempts >= state.max_attempts:
            state.mastery_status = "not_mastered_max_attempts"
            state.stage = LearningStage.COMPLETE
        return state

    if state.stage == LearningStage.MASTER_CHALLENGE:
        state.cloze_attempts += 1
        if passed:
            state.mastery_status = "mastered"
            state.stage = LearningStage.COMPLETE
        elif state.total_attempts >= state.max_attempts:
            state.mastery_status = "not_mastered_max_attempts"
            state.stage = LearningStage.COMPLETE
        return state

    return state
