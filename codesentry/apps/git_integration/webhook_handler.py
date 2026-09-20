"""
Приём событий GitHub. В офлайн/локальном режиме события можно
эмулировать локально (см. scripts/seed_demo_data.py) или пробрасывать
через localtunnel/ngrok для реального тестирования вебхуков.
"""

import hashlib
import hmac
from uuid import uuid4

from core.config import get_settings
from core.logging_config import get_logger
from core.schemas import PullRequest

logger = get_logger(__name__)


def verify_signature(payload_body: bytes, signature_header: str | None) -> bool:
    settings = get_settings()
    if not signature_header:
        return False
    expected = "sha256=" + hmac.new(
        settings.github_webhook_secret.encode(), payload_body, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature_header)


def parse_pull_request_event(payload: dict) -> PullRequest:
    pr_data = payload["pull_request"]
    return PullRequest(
        id=str(pr_data.get("id", uuid4())),
        title=pr_data["title"],
        author=pr_data["user"]["login"],
        repo=payload["repository"]["full_name"],
        created_at=pr_data["created_at"],
        status="pending",
        files_changed=[],
    )
