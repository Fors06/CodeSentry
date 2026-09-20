from datetime import datetime, timezone

from core.schemas import Finding, FindingSource, PullRequest, Severity


def test_save_and_get_pr(tmp_data_dir):
    from apps.persistence.repository import PRRepository

    repo = PRRepository()
    pr = PullRequest(
        id="pr-1",
        title="Test PR",
        author="alice",
        repo="org/repo",
        created_at=datetime.now(timezone.utc),
    )
    repo.save(pr)

    loaded = repo.get("pr-1")
    assert loaded is not None
    assert loaded.title == "Test PR"


def test_save_and_get_findings(tmp_data_dir):
    from apps.persistence.repository import FindingRepository

    repo = FindingRepository()
    findings = [
        Finding(
            id="f1",
            file="a.py",
            line=1,
            severity=Severity.HIGH,
            source=FindingSource.AI_REVIEW,
            message="Проблема",
        )
    ]
    repo.save("pr-1", findings)
    loaded = repo.get("pr-1")
    assert len(loaded.findings) == 1
    assert loaded.findings[0].severity == Severity.HIGH
