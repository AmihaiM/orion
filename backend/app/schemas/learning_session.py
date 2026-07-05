from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class CreateLearningSessionRequest(BaseModel):
    student_id: UUID
    mission_id: UUID
    assignment_id: Optional[UUID] = None


class LearningSessionResponse(BaseModel):
    id: UUID
    student_id: UUID
    mission_id: UUID
    assignment_id: Optional[UUID] = None
    status: str
    started_at: datetime