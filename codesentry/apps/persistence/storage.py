"""
Низкоуровневое чтение/запись JSON-файлов с блокировкой (filelock),
чтобы конкурентная запись из нескольких фоновых задач не портила данные.
Это ЕДИНСТВЕННОЕ место в проекте, где происходит прямая работа с файлами данных.
"""

import json
from pathlib import Path
from typing import Any

from filelock import FileLock


def _lock_path(path: Path) -> Path:
    return path.with_suffix(path.suffix + ".lock")


def read_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    with FileLock(str(_lock_path(path)), timeout=5):
        return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with FileLock(str(_lock_path(path)), timeout=5):
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2, default=str), encoding="utf-8")


def list_json_files(directory: Path) -> list[Path]:
    if not directory.exists():
        return []
    return sorted(p for p in directory.glob("*.json"))


def delete_json(path: Path) -> None:
    lock = _lock_path(path)
    with FileLock(str(lock), timeout=5):
        if path.exists():
            path.unlink()
    if lock.exists():
        lock.unlink()
