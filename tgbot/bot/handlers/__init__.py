from aiogram import Router

from tgbot.bot.filters import ChatPrivateFilter, IsAdminFilter


def setup_routers() -> Router:
    from .users import start, help, echo, record, check, admin, statistic, feedback, settings, channel_confirm
    from .errors import error_handler

    router = Router()

    # Agar kerak bo'lsa, o'z filteringizni o'rnating
    start.router.message.filter(ChatPrivateFilter())
    record.router.message.filter(ChatPrivateFilter())
    check.router.message.filter(ChatPrivateFilter())
    statistic.router.message.filter(ChatPrivateFilter())
    feedback.router.message.filter(ChatPrivateFilter())
    admin.router.message.filter(IsAdminFilter())

    router.include_routers(
                    admin.router, start.router, record.router, 
                    check.router, statistic.router, help.router,  
                    settings.router, channel_confirm.router, feedback.router,
                    echo.router, error_handler.router,  
                )

    return router
