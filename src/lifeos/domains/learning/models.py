from datetime import datetime, timezone
from enum import StrEnum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class LearningMemoryType(StrEnum):
    CONCEPT = "concept"
    SKILL = "skill"
    PROJECT = "project"
    QUESTION = "question"
    MISTAKE = "mistake"
    INSIGHT = "insight"


class LearningMemory(BaseModel):
    id: UUID = Field(default_factory=uuid4)

    memory_type: LearningMemoryType

    title: str = Field(min_length=1)
    content: str = Field(min_length=1)

    topics: list[str] = Field(default_factory=list)
    project: str | None = None
    source: str | None = None

    confidence: float | None = Field(
        default=None,
        ge=0,
        le=1,
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )