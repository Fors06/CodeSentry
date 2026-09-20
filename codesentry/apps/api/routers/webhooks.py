"""Приём GitHub webhook (или локальной эмуляции для офлайн-тестов)."""

from fastapi import APIRouter, BackgroundTasks, Header, HTTPException, Request

from apps.api.background_tasks import process_pull_request
from apps.api.dependencies import get_pr_repository
from apps.git_integration.webhook_handler import parse_pull_request_event, verify_signature
from core.logging_config import get_logger

router = APIRouter(prefix="/webhooks", tags=["webhooks"])
logger = get_logger(__name__)


@router.post("/github")
async def github_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    x_hub_signature_256: str | None = Header(default=None),
) -> dict:
    body = await request.body()
    if not verify_signature(body, x_hub_signature_256):
        raise HTTPException(status_code=401, detail="Неверная подпись webhook")

    payload = await request.json()
    if "pull_request" not in payload:
        return {"status": "ignored"}

    pr = parse_pull_request_event(payload)
    get_pr_repository().save(pr)

    repo_url = payload["repository"]["clone_url"]
    base = payload["pull_request"]["base"]["ref"]
    head = payload["pull_request"]["head"]["ref"]

    background_tasks.add_task(process_pull_request, pr.id, repo_url, pr.repo, base, head)
    logger.info("PR %s поставлен в очередь на анализ", pr.id)
    return {"status": "accepted", "pr_id": pr.id}
