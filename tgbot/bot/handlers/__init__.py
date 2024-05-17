from aiogram import Router

from tgbot.bot.filters import ChatPrivateFilter


def setup_routers() -> Router:
    from .users import start, help, echo, record, check
    from .errors import error_handler

    router = Router()

    # Agar kerak bo'lsa, o'z filteringizni o'rnating
    start.router.message.filter(ChatPrivateFilter())
    record.router.message.filter(ChatPrivateFilter())
    check.router.message.filter(ChatPrivateFilter())

    router.include_routers(start.router, record.router, check.router, help.router, echo.router, error_handler.router)

    return router
