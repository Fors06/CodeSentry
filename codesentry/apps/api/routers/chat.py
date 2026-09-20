"""Эндпоинт вопросов к кодовой базе через RAG (retrieval-augmented generation)."""

from fastapi import APIRouter

from apps.ai_review.ollama_client import OllamaClient
from apps.rag.retriever import Retriever
from core.schemas import AskRequest, AskResponse

router = APIRouter(prefix="/api", tags=["chat"])

_QA_PROMPT = """Ответь на вопрос разработчика, используя приведённый контекст кода.
Если ответа нет в контексте, честно скажи об этом.

Контекст:
{context}

Вопрос: {question}
"""


@router.post("/ask", response_model=AskResponse)
def ask(request: AskRequest) -> AskResponse:
    repo_name = request.repo or "default"
    retriever = Retriever(repo_name=repo_name)
    matches = retriever.search(request.question, top_k=5)

    context = "\n\n".join(f"# {m['file']}\n{m.get('text', '')}" for m in matches)
    prompt = _QA_PROMPT.format(context=context or "(контекст не найден)", question=request.question)

    answer = OllamaClient().generate(prompt)
    return AskResponse(answer=answer, sources=[m["file"] for m in matches])
