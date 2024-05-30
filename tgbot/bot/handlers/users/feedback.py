from aiogram import F, Router, types
from aiogram.types import CallbackQuery, Voice
from aiogram.fsm.context import FSMContext

from tgbot.models import Feedback, User
from tgbot.bot.keyboards import reply, builders
from tgbot.bot.states.main import FeedBackState

router = Router()

@router.message(F.text.in_(['💬 Fikr qoldirish', '/feedback']))
async def feedback_func(message: types.Message, state: FSMContext):
    await state.set_state(FeedBackState.feed)
    await message.answer("Bot to'g'risida savol, taklif yoki botda kuzatilgan qandaydir muammolar yoki bot haqida fikringizni yozib qoldirishingiz mumkin.", reply_markup=reply.back_btn)


@router.message(FeedBackState.feed, F.text)
async def feed_handler(message: types.Message, state: FSMContext):
    text = message.text
    if text == '❌ Bekor qilish':
        await message.answer("Bosh menu", reply_markup=reply.main)
        await state.clear()
        return
    
    user = await User.objects.aget(telegram_id=message.from_user.id)
    await Feedback.objects.acreate(user=user, feedback=text)

    await message.reply("Fikr qoldirganingiz uchun tashakkur! \nOvoz yozishda davom eting...", reply_markup=reply.main)
    await state.clear()

