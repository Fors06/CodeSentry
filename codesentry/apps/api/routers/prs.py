"""REST-эндпоинты для списка PR и деталей по конкретному PR."""

from fastapi import APIRouter, Depends, HTTPException

from apps.api.dependencies import get_pr_repository
from apps.persistence.repository import PRRepository
from core.schemas import PullRequest

router = APIRouter(prefix="/api/prs", tags=["pull-requests"])


@router.get("", response_model=list[PullRequest])
def list_prs(repo: PRRepository = Depends(get_pr_repository)) -> list[PullRequest]:
    return repo.list()


@router.get("/{pr_id}", response_model=PullRequest)
def get_pr(pr_id: str, repo: PRRepository = Depends(get_pr_repository)) -> PullRequest:
    pr = repo.get(pr_id)
    if not pr:
        raise HTTPException(status_code=404, detail="PR не найден")
    return pr
