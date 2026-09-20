"""Клонирование/обновление репозиториев на локальный диск через GitPython."""

from pathlib import Path

import git

from core.config import get_settings
from core.logging_config import get_logger

logger = get_logger(__name__)


def get_or_clone_repo(repo_url: str, repo_name: str) -> Path:
    """Клонирует репозиторий, если его ещё нет локально, иначе делает pull."""
    settings = get_settings()
    safe_name = repo_name.replace("/", "__")
    local_path = settings.repos_cache_dir / safe_name

    if local_path.exists():
        logger.info("Обновляю существующий репозиторий: %s", repo_name)
        repo = git.Repo(local_path)
        repo.remotes.origin.pull()
    else:
        logger.info("Клонирую репозиторий: %s -> %s", repo_url, local_path)
        git.Repo.clone_from(repo_url, local_path)

    return local_path


def get_diff_for_pr(local_path: Path, base_branch: str, head_branch: str) -> str:
    repo = git.Repo(local_path)
    diff = repo.git.diff(f"{base_branch}...{head_branch}")
    return diff
