"""Обёртки над внешними линтерами/анализаторами: ruff, bandit, radon."""

import json
import subprocess
from pathlib import Path

from core.logging_config import get_logger

logger = get_logger(__name__)


def run_ruff(target: Path) -> list[dict]:
    """Запускает ruff в формате JSON и возвращает список сырых находок."""
    try:
        result = subprocess.run(
            ["ruff", "check", "--output-format=json", str(target)],
            capture_output=True,
            text=True,
            timeout=60,
        )
        if not result.stdout.strip():
            return []
        return json.loads(result.stdout)
    except (subprocess.TimeoutExpired, json.JSONDecodeError) as exc:
        logger.warning("ruff завершился с ошибкой: %s", exc)
        return []


def run_bandit(target: Path) -> list[dict]:
    """Запускает bandit (поиск уязвимостей) в формате JSON."""
    try:
        result = subprocess.run(
            ["bandit", "-f", "json", "-r", str(target)],
            capture_output=True,
            text=True,
            timeout=60,
        )
        data = json.loads(result.stdout or "{}")
        return data.get("results", [])
    except (subprocess.TimeoutExpired, json.JSONDecodeError) as exc:
        logger.warning("bandit завершился с ошибкой: %s", exc)
        return []


def run_radon_complexity(target: Path) -> dict:
    """Запускает radon cc (цикломатическая сложность) в формате JSON."""
    try:
        result = subprocess.run(
            ["radon", "cc", "-j", str(target)],
            capture_output=True,
            text=True,
            timeout=60,
        )
        return json.loads(result.stdout or "{}")
    except (subprocess.TimeoutExpired, json.JSONDecodeError) as exc:
        logger.warning("radon завершился с ошибкой: %s", exc)
        return {}
