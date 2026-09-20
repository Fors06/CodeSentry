"""Общие зависимости FastAPI (репозитории и т.д.)."""

from functools import lru_cache

from apps.persistence.repository import FindingRepository, MetricRepository, PRRepository


@lru_cache
def get_pr_repository() -> PRRepository:
    return PRRepository()


@lru_cache
def get_finding_repository() -> FindingRepository:
    return FindingRepository()


@lru_cache
def get_metric_repository() -> MetricRepository:
    return MetricRepository()
