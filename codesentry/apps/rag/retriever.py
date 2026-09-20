"""Поиск релевантного контекста кода по запросу (косинусное сходство, без БД)."""

import numpy as np

from .embedder import Embedder
from .index_store import IndexStore


def _cosine_similarity(query_vec: np.ndarray, matrix: np.ndarray) -> np.ndarray:
    if matrix.size == 0:
        return np.array([])
    query_norm = query_vec / (np.linalg.norm(query_vec) + 1e-10)
    matrix_norm = matrix / (np.linalg.norm(matrix, axis=1, keepdims=True) + 1e-10)
    return matrix_norm @ query_norm


class Retriever:
    def __init__(self, repo_name: str, embedder: Embedder | None = None) -> None:
        self.repo_name = repo_name
        self.embedder = embedder or Embedder()
        self.store = IndexStore(repo_name)

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        vectors, metadata = self.store.load()
        if len(metadata) == 0:
            return []

        query_vec = np.array(self.embedder.embed_text(query), dtype=np.float32)
        similarities = _cosine_similarity(query_vec, vectors)
        top_indices = np.argsort(similarities)[::-1][:top_k]

        return [
            {**metadata[i], "score": float(similarities[i])}
            for i in top_indices
            if i < len(metadata)
        ]
