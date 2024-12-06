from typing import Optional, Tuple

from telegram import Update
from telegram.ext import (
    Application,
    AIORateLimiter
)

from .handlers import add_handlers
from ..config import TELEGRAM_BOT_TOKEN, TELEBOT_CONNECT_TIMEOUT, TELEBOT_READ_TIMEOUT, TELEBOT_WRITE_TIMEOUT, \
    TELEBOT_API_SERVER, TELEBOT_LOCAL_FILE_MODE, TELEBOT_MAX_RETRY


def new_bot(
        token: str = TELEGRAM_BOT_TOKEN,
        arbitrary_callback_data: Optional[bool] = True,
        connect_timeout: Optional[int] = TELEBOT_CONNECT_TIMEOUT,
        read_timeout: Optional[int] = TELEBOT_READ_TIMEOUT,
        write_timeout: Optional[int] = TELEBOT_WRITE_TIMEOUT,
        base_url: Optional[str] = TELEBOT_API_SERVER,
        base_file_url: Optional[str] = TELEBOT_API_SERVER,
        local_mode: Optional[bool] = TELEBOT_LOCAL_FILE_MODE,
        max_retry: Optional[int] = TELEBOT_MAX_RETRY,
        add_response_handlers: Optional[bool] = True,
) -> Application:
    application = (
        Application.builder()
        .token(token)
        .arbitrary_callback_data(arbitrary_callback_data)
        .connect_timeout(connect_timeout)
        .read_timeout(read_timeout)
        .write_timeout(write_timeout)
        .base_url(base_url)
        .base_file_url(base_file_url)
        .local_mode(local_mode)
        .rate_limiter(AIORateLimiter(max_retries=max_retry))
        .build()
    )
    if add_response_handlers:
        add_handlers(application)
    return application


async def set_webhook(
        application: Application,
        url: str,
        max_connections: Optional[int] = None,
        allowed_updates: Optional[Tuple[str]] = None,
) -> None:
    await application.bot.set_webhook(url, max_connections=max_connections, allowed_updates=allowed_updates)


async def delete_webhook(application: Application) -> None:
    await application.bot.delete_webhook()


def run_bot_polling() -> None:
    application = new_bot()
    application.run_polling(allowed_updates=Update.ALL_TYPES)
