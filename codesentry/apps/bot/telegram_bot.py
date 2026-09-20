"""Telegram-бот для уведомлений о находках. Работает локально, требует токен."""

from telegram import Bot

from core.config import get_settings
from core.logging_config import get_logger

logger = get_logger(__name__)


class NotificationBot:
    def __init__(self) -> None:
        settings = get_settings()
        self._token = settings.telegram_bot_token
        self._bot: Bot | None = Bot(token=self._token) if self._token else None

    async def send_message(self, chat_id: str, text: str) -> None:
        if not self._bot:
            logger.warning("TELEGRAM_BOT_TOKEN не задан — уведомление не отправлено: %s", text[:80])
            return
        await self._bot.send_message(chat_id=chat_id, text=text, parse_mode="Markdown")
