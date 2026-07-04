from datetime import datetime
from typing import Any, List, Optional
from uuid import UUID
from pydantic import BaseModel


class MissionSummary(BaseModel):
    id: UUID
    title: str
    level: Optional[str] = None
    unit: Optional[str] = None
    source_type: Optional[str] = None
    visibility: Optional[str] = None
    created_at: Optional[datetime] = None


class Sentence(BaseModel):
    id: UUID
    sentence_order: int
    english_text: str
    hebrew_text: Optional[str] = None
    difficulty: Optional[str] = None
    tags: List[str] = []


class MissionDetail(BaseModel):
    mission: MissionSummary
    sentences: List[Sentence]


class MissionsResponse(BaseModel):
    missions: List[MissionSummary]
