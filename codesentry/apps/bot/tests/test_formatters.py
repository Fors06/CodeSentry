from datetime import datetime, timezone

from apps.bot.formatters import format_pr_analyzed_message
from core.schemas import Finding, FindingSource, PullRequest, Severity


def test_format_message_no_findings():
    pr = PullRequest(
        id="1", title="Test", author="a", repo="o/r", created_at=datetime.now(timezone.utc)
    )
    message = format_pr_analyzed_message(pr, [])
    assert "не обнаружено" in message


def test_format_message_with_findings():
    pr = PullRequest(
        id="1", title="Test", author="a", repo="o/r", created_at=datetime.now(timezone.utc)
    )
    findings = [
        Finding(id="1", file="a.py", line=1, severity=Severity.HIGH, source=FindingSource.AI_REVIEW, message="msg")
    ]
    message = format_pr_analyzed_message(pr, findings)
    assert "a.py:1" in message
