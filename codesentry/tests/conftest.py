"""Общие фикстуры для всех тестов проекта."""

import shutil
import tempfile
from pathlib import Path

import pytest

from core.config import get_settings


@pytest.fixture
def tmp_data_dir(monkeypatch):
    """Подменяет data_dir на временную папку, чтобы тесты не трогали реальные данные."""
    tmp_dir = Path(tempfile.mkdtemp())
    monkeypatch.setenv("DATA_DIR", str(tmp_dir))
    get_settings.cache_clear()
    settings = get_settings()
    yield settings
    get_settings.cache_clear()
    shutil.rmtree(tmp_dir, ignore_errors=True)
