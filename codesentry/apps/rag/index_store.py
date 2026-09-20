"""
Хранилище векторного индекса без внешней БД: эмбеддинги и метаданные
сохраняются в обычные файлы на диске (numpy + JSON).
"""

import json
from pathlib import Path

import numpy as np

from core.config import get_settings


class IndexStore:
    def __init__(self, repo_name: str) -> None:
        settings = get_settings()
        safe_name = repo_name.replace("/", "__")
        self._vectors_path = settings.embeddings_dir / f"{safe_name}.npy"
        self._meta_path = settings.embeddings_dir / f"{safe_name}_meta.json"

    def save(self, vectors: list[list[float]], metadata: list[dict]) -> None:
        arr = np.array(vectors, dtype=np.float32)
        np.save(self._vectors_path, arr)
        self._meta_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")

    def load(self) -> tuple[np.ndarray, list[dict]]:
        if not self._vectors_path.exists() or not self._meta_path.exists():
            return np.empty((0, 0), dtype=np.float32), []
        vectors = np.load(self._vectors_path)
        metadata = json.loads(self._meta_path.read_text(encoding="utf-8"))
        return vectors, metadata

    def exists(self) -> bool:
        return self._vectors_path.exists() and self._meta_path.exists()
