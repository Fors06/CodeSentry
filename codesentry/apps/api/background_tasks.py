"""
Фоновая обработка PR — замена очереди Celery/Redis для локального,
однопроцессного запуска. Использует FastAPI BackgroundTasks.
"""

from pathlib import Path

from apps.ai_review.review_pipeline import AIReviewPipeline
from apps.git_integration.repo_manager import get_diff_for_pr, get_or_clone_repo
from apps.metrics.complexity import average_complexity
from apps.metrics.tech_debt import calculate_tech_debt_index
from apps.persistence.repository import FindingRepository, MetricRepository, PRRepository
from apps.static_analysis.normalizer import from_bandit, from_ruff
from apps.static_analysis.runners import run_bandit, run_ruff
from core.logging_config import get_logger
from core.schemas import MetricPoint

logger = get_logger(__name__)


def process_pull_request(pr_id: str, repo_url: str, repo_name: str, base: str, head: str) -> None:
    """Полный пайплайн анализа одного PR. Вызывается как фоновая задача."""
    pr_repo = PRRepository()
    finding_repo = FindingRepository()
    metric_repo = MetricRepository()

    pr = pr_repo.get(pr_id)
    if not pr:
        logger.error("PR %s не найден для обработки", pr_id)
        return

    pr.status = "analyzing"
    pr_repo.save(pr)

    try:
        local_path = get_or_clone_repo(repo_url, repo_name)
        diff = get_diff_for_pr(local_path, base, head)

        static_findings = from_ruff(run_ruff(Path(local_path))) + from_bandit(run_bandit(Path(local_path)))
        ai_findings = AIReviewPipeline().review_diff(diff)
        all_findings = static_findings + ai_findings

        finding_repo.save(pr_id, all_findings)

        complexity = average_complexity(Path(local_path))
        tech_debt = calculate_tech_debt_index(all_findings, complexity)
        metric_repo.append(
            MetricPoint(
                date=pr.created_at.date().isoformat(),
                tech_debt_index=tech_debt,
                avg_complexity=complexity,
            )
        )

        pr.status = "analyzed"
        pr_repo.save(pr)
        logger.info("PR %s проанализирован: %d находок", pr_id, len(all_findings))
    except Exception:
        logger.exception("Ошибка при обработке PR %s", pr_id)
        pr.status = "error"
        pr_repo.save(pr)
