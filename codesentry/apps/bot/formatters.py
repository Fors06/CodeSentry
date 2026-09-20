"""Форматирование сообщений для Telegram/Slack-уведомлений."""

from core.schemas import Finding, PullRequest

_SEVERITY_EMOJI = {
    "low": "🔵",
    "medium": "🟡",
    "high": "🟠",
    "critical": "🔴",
}


def format_pr_analyzed_message(pr: PullRequest, findings: list[Finding]) -> str:
    lines = [f"✅ Анализ PR завершён: *{pr.title}*", f"Репозиторий: `{pr.repo}`", ""]
    if not findings:
        lines.append("Находок не обнаружено 🎉")
    else:
        lines.append(f"Найдено проблем: {len(findings)}")
        for f in sorted(findings, key=lambda x: x.severity.value, reverse=True)[:5]:
            emoji = _SEVERITY_EMOJI.get(f.severity.value, "⚪")
            lines.append(f"{emoji} `{f.file}:{f.line}` — {f.message}")
    return "\n".join(lines)
