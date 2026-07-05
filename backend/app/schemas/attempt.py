from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class CreateAttemptRequest(BaseModel):
    student_id: UUID
    mission_id: UUID
    sentence_id: UUID
    session_id: UUID
    stage: str = Field(default="practice")
    spoken_text: Optional[str] = None
    accuracy_score: Optional[int] = None
    passed: Optional[bool] = None
    recording_duration_ms: int = 0
    silence_ms: int = 0
    words_per_minute: int = 0
    fluency_status: Optional[str] = None


class AttemptResponse(BaseModel):
    id: UUID
    student_id: UUID
    mission_id: UUID
    sentence_id: UUID
    session_id: UUID
    stage: str
    spoken_text: Optional[str]
    accuracy_score: Optional[int]
    passed: Optional[bool]
    fluency_status: Optional[str]
    created_at: datetime