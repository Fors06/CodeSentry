from unittest.mock import MagicMock

import numpy as np

from apps.rag.retriever import Retriever


def test_search_returns_empty_when_no_index(tmp_data_dir):
    retriever = Retriever(repo_name="test/repo", embedder=MagicMock())
    results = retriever.search("что делает эта функция?")
    assert results == []


def test_search_ranks_by_similarity(tmp_data_dir):
    from apps.rag.index_store import IndexStore

    mock_embedder = MagicMock()
    mock_embedder.embed_text.return_value = [1.0, 0.0]

    store = IndexStore("test/repo")
    store.save(
        vectors=[[1.0, 0.0], [0.0, 1.0]],
        metadata=[{"file": "a.py", "text": "relevant"}, {"file": "b.py", "text": "irrelevant"}],
    )

    retriever = Retriever(repo_name="test/repo", embedder=mock_embedder)
    results = retriever.search("query", top_k=1)
    assert results[0]["file"] == "a.py"
