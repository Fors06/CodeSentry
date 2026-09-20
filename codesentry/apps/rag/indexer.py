"""Обход репозитория, разбиение файлов на чанки и построение индекса для RAG."""

from pathlib import Path

from core.logging_config import get_logger

from .embedder import Embedder
from .index_store import IndexStore

logger = get_logger(__name__)

CHUNK_LINES = 60
SUPPORTED_EXTENSIONS = {".py"}


def _chunk_file(path: Path) -> list[str]:
    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    return [
        "\n".join(lines[i : i + CHUNK_LINES]) for i in range(0, len(lines), CHUNK_LINES) if lines[i : i + CHUNK_LINES]
    ]


def index_repository(repo_path: Path, repo_name: str, embedder: Embedder | None = None) -> int:
    """Индексирует все .py файлы репозитория. Возвращает количество проиндексированных чанков."""
    embedder = embedder or Embedder()
    chunks: list[str] = []
    metadata: list[dict] = []

    for file_path in repo_path.rglob("*"):
        if file_path.suffix not in SUPPORTED_EXTENSIONS or not file_path.is_file():
            continue
        for i, chunk in enumerate(_chunk_file(file_path)):
            chunks.append(chunk)
            metadata.append({"file": str(file_path.relative_to(repo_path)), "chunk_index": i})

    if not chunks:
        logger.warning("Нет файлов для индексации в %s", repo_path)
        return 0

    vectors = embedder.embed_batch(chunks)
    for meta, chunk in zip(metadata, chunks, strict=True):
        meta["text"] = chunk

    IndexStore(repo_name).save(vectors, metadata)
    logger.info("Проиндексировано %d чанков из %s", len(chunks), repo_name)
    return len(chunks)
