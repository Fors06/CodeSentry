"""REST-эндпоинт для находок по PR."""

from fastapi import APIRouter, Depends

from apps.api.dependencies import get_finding_repository
from apps.persistence.repository import FindingRepository
from core.schemas import FindingsForPR

router = APIRouter(prefix="/api/findings", tags=["findings"])


@router.get("/{pr_id}", response_model=FindingsForPR)
def get_findings(pr_id: str, repo: FindingRepository = Depends(get_finding_repository)) -> FindingsForPR:
    return repo.get(pr_id)


@router.get("", response_model=list[FindingsForPR])
def list_all_findings(repo: FindingRepository = Depends(get_finding_repository)) -> list[FindingsForPR]:
    return repo.list_all()
