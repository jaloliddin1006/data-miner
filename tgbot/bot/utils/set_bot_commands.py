from aiogram import Bot
from aiogram.methods.set_my_commands import BotCommand
from aiogram.types import BotCommandScopeAllPrivateChats


async def set_default_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Botni ishga tushirish"),
        BotCommand(command="/help", description="Yordam"),
        BotCommand(command="/record", description="Ovoz yozishni boshlash"),
        BotCommand(command="/checking", description="Tekshirish"),
        BotCommand(command="/stat", description="Statistikani ko'rish"),
        BotCommand(command="/feedback", description="Fikr bildirish"),
        BotCommand(command="/settings", description="Ma'lumotlarim bo'limi"),
    ]
    await bot.set_my_commands(commands=commands, scope=BotCommandScopeAllPrivateChats())
