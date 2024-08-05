from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.session.middlewares.request_logging import logger
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from tgbot.models import User
from asgiref.sync import sync_to_async

from tgbot.bot.loader import bot
from django.conf import settings
from tgbot.bot.utils.extra_datas import make_title
from tgbot.bot.keyboards import reply, builders
from tgbot.bot.states.main import Start
import os


router = Router()

@router.message(CommandStart())
async def do_start(message: Message, state=FSMContext):
    telegram_id = message.from_user.id
    full_name = message.from_user.full_name
    
    await message.answer(f"Assalomu alaykum {full_name}!", parse_mode=ParseMode.MARKDOWN, reply_markup=reply.rmk)

    user, created = await User.objects.aget_or_create(
        telegram_id=telegram_id,
        full_name=full_name,
        username=message.from_user.username
    )
    if created:
        count = await User.objects.acount()
        await message.answer("Iltimos, o'zingizning joylashuvingizni tanlang:", reply_markup=await builders.get_region_btn('none'))
        await state.set_state(Start.location)
        msg = (f"[{user.full_name}](tg://user?id={telegram_id}) bazaga qo'shildi\.\nBazada {count} ta foydalanuvchi bor\.")
    else:
        await message.answer("Botdan foydalanishingiz mumkin", reply_markup=reply.main)
        msg = f"[{full_name}](tg://user?id={telegram_id}) bazaga oldin qo'shilgan"
        if not user.is_active:
            await sync_to_async(User.objects.filter(telegram_id=telegram_id).update)(is_active=True)
        await state.clear()
        
    for admin in settings.ADMINS:
        try:
            await bot.send_message(
                chat_id=admin,
                text=msg,
                parse_mode=ParseMode.MARKDOWN
            )
        except Exception as error:
            logger.info(f"Data did not send to admin: {admin}. Error: {error}")
            continue
        

@router.callback_query(Start.location, F.data.startswith('set_region_'))
async def process_location(call: CallbackQuery, state: FSMContext):
    await state.update_data(location=call.data.split("_")[-1])
    await call.message.delete()

    await call.message.answer("Jinsingizni tanlang:", reply_markup=await builders.get_gender_btn('none'))
    await state.set_state(Start.sex)


@router.callback_query(Start.sex, F.data.startswith('set_gender_'))
async def process_sex(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    user_data = await state.get_data()

    user = await User.objects.aget(telegram_id=call.from_user.id)
    user.location = user_data.get('location')
    user.sex = call.data.split("_")[-1]
    await user.asave()
    
    await call.answer("Ma'lumotlar saqlandi", show_alert=True)
    await call.message.answer("Ma'lumotlar saqlandi. Botdan foydalanishingiz mumkin.", reply_markup=reply.main)
    await state.clear()









