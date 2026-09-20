"""
Эндпоинт агента, который умеет создавать/редактировать/удалять файлы
в песочнице AGENT_WORKSPACE_DIR (см. .env). Доступ строго ограничен этой
папкой на уровне apps/agent_tools/file_tools.py — выйти за её пределы нельзя.
"""

from pydantic import BaseModel, Field

from fastapi import APIRouter

from apps.agent_tools import file_tools
from apps.agent_tools.agent import FileAgent
from apps.agent_tools.analysis import FileAnalyzer
from core.config import get_settings

router = APIRouter(prefix="/api/agent", tags=["agent"])


class AgentRunRequest(BaseModel):
    task: str = Field(..., description="Задача на естественном языке, например: 'создай файл notes.txt с планом на неделю'")


class AgentStepResponse(BaseModel):
    tool_name: str
    arguments: dict
    result: str


class AgentRunResponse(BaseModel):
    answer: str
    steps: list[AgentStepResponse]


@router.post("/run", response_model=AgentRunResponse)
def run_agent(request: AgentRunRequest) -> AgentRunResponse:
    settings = get_settings()
    agent = FileAgent(workspace_root=settings.agent_workspace_dir)
    result = agent.run(request.task)
    return AgentRunResponse(
        answer=result.answer,
        steps=[
            AgentStepResponse(tool_name=s.tool_name, arguments=s.arguments, result=s.result)
            for s in result.steps
        ],
    )


@router.get("/workspace")
def get_workspace_info() -> dict:
    settings = get_settings()
    return {"workspace_dir": str(settings.agent_workspace_dir.resolve())}


@router.get("/tree")
def get_tree(relative_dir: str = ".") -> dict:
    """Полный рекурсивный список файлов рабочей папки."""
    settings = get_settings()
    files = file_tools.list_files_recursive(settings.agent_workspace_dir, relative_dir)
    return {"files": files, "count": len(files)}


@router.get("/search/name")
def search_by_name(pattern: str, relative_dir: str = ".") -> dict:
    """Поиск файлов/папок по имени (подстрока, регистронезависимо, рекурсивно)."""
    settings = get_settings()
    matches = file_tools.search_by_name(settings.agent_workspace_dir, pattern, relative_dir)
    return {"pattern": pattern, "matches": matches, "count": len(matches)}


@router.get("/search/content")
def search_by_content(query: str, relative_dir: str = ".") -> dict:
    """Поиск текста внутри содержимого файлов (рекурсивно)."""
    settings = get_settings()
    matches = file_tools.search_by_content(settings.agent_workspace_dir, query, relative_dir)
    return {"query": query, "matches": matches, "count": len(matches)}


@router.get("/explain/file")
def explain_file(relative_path: str) -> dict:
    """Объяснение простым языком, что делает конкретный файл."""
    settings = get_settings()
    analyzer = FileAnalyzer(settings.agent_workspace_dir)
    explanation = analyzer.explain_file(relative_path)
    return {"file": relative_path, "explanation": explanation}


@router.get("/explain/folder")
def explain_folder(relative_dir: str = ".") -> dict:
    """Общий обзор простым языком, что за файлы в папке и как они связаны."""
    settings = get_settings()
    analyzer = FileAnalyzer(settings.agent_workspace_dir)
    explanation = analyzer.explain_folder(relative_dir)
    return {"folder": relative_dir, "explanation": explanation}
