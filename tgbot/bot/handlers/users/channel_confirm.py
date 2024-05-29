from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from tgbot.bot.keyboards import reply
from aiogram.enums.parse_mode import ParseMode

router = Router()


@router.callback_query(lambda c: c.data == 'confirm')
async def callback_confirm(callback_query: CallbackQuery, state=FSMContext):
    pass
