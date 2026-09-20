"""
Общие Pydantic-схемы — единый "контракт" между всеми модулями
(persistence, api, ai_review, rag, web) в отсутствие схемы БД.
Любое изменение этих моделей должно обсуждаться со всей командой.
"""

from datetime import datetime
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class FindingSource(str, Enum):
    STATIC_ANALYSIS = "static_analysis"
    AI_REVIEW = "ai_review"


class PullRequest(BaseModel):
    id: str
    title: str
    author: str
    repo: str
    created_at: datetime
    status: Literal["pending", "analyzing", "analyzed", "error"] = "pending"
    files_changed: list[str] = Field(default_factory=list)


class Finding(BaseModel):
    id: str
    file: str
    line: int
    severity: Severity
    source: FindingSource
    message: str


class FindingsForPR(BaseModel):
    pr_id: str
    findings: list[Finding] = Field(default_factory=list)


class MetricPoint(BaseModel):
    date: str  # YYYY-MM-DD
    tech_debt_index: float
    avg_complexity: float


class AskRequest(BaseModel):
    question: str
    repo: str | None = None


class AskResponse(BaseModel):
    answer: str
    sources: list[str] = Field(default_factory=list)
