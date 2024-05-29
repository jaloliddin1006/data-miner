from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.session.middlewares.request_logging import logger
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from tgbot.models import User

from tgbot.bot.loader import bot
from django.conf import settings
from tgbot.bot.utils.extra_datas import make_title
from tgbot.bot.keyboards import reply
from tgbot.bot.states.main import Start
import os
from tgbot.models import Channel
from tgbot.bot.utils import check_channel_member
from tgbot.bot.keyboards.builders import regions

router = Router()


@router.message(CommandStart())
async def do_start(message: types.Message, state=FSMContext,hello=True):
    await state.clear()
    if not os.path.exists('media/voices'):
        os.makedirs('media/voices')
    """
            MARKDOWN V2                     |     HTML
    link:   [Google](https://google.com/)   |     <a href='https://google.com/'>Google</a>
    bold:   *Qalin text*                    |     <b>Qalin text</b>
    italic: _Yotiq shriftdagi text_         |     <i>Yotiq shriftdagi text</i>



                    **************     Note     **************
    Markdownda _ * [ ] ( ) ~ ` > # + - = | { } . ! belgilari to'g'ridan to'g'ri ishlatilmaydi!!!
    Bu belgilarni ishlatish uchun oldidan / qo'yish esdan chiqmasin. Masalan  .  ko'rinishi . belgisini ishlatish uchun yozilgan.
    """
    # telegram_id = message.chat.id
    # full_name = message.chat.full_name\
    if hello:
        pass
    checked = await check_channel_member.check_user(message.chat.id)
    if not checked:
    
        user_exists = User.objects.filter(telegram_id=message.chat.id).exists()
        if not user_exists:
            fullname = message.chat.full_name
            telegram_id = message.chat.id
            await state.update_data(fullname=fullname, telegram_id=telegram_id)
            nested_list = [[InlineKeyboardButton(text=regions[i], callback_data=regions[i]), InlineKeyboardButton(text=regions[i+1], callback_data=regions[i+1])] for i in range(0, len(regions), 2)]
            inline_kb = InlineKeyboardMarkup(inline_keyboard=nested_list)
            await message.answer("Assalomu alaykum \nIstiqomat qiladigan viloyatingizni tanlang:", reply_markup=inline_kb)
            await state.set_state(Start.location)
        else:
            await message.answer(f"Assalomu alaykum {make_title(message.chat.full_name)}!", parse_mode=ParseMode.MARKDOWN, reply_markup=reply.main)





@router.callback_query(Start.location)
async def process_location(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(location=callback_query.data)
    await callback_query.message.delete()
    sex_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Erkak", callback_data="erkak"),
        InlineKeyboardButton(text="Ayol", callback_data="ayol")]
    ])
    await callback_query.message.answer("Jinsingizni tanlang:", reply_markup=sex_keyboard)
    await state.set_state(Start.sex)


@router.callback_query(Start.sex)
async def process_sex(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(sex=callback_query.data)
    await callback_query.message.delete()
    user_data = await state.get_data()

    user, created = await User.objects.aget_or_create(
        telegram_id=user_data['telegram_id'],
        full_name=user_data['fullname'],
        username=callback_query.message.chat.username,
        location=user_data['location'],
        sex=user_data['sex']
        
    )
    if created:
        user_path = f'media/voices/{user.telegram_id}/'
        if not os.path.exists(user_path):
            os.mkdir(user_path)
        count = await User.objects.acount()
        msg = (f"[{make_title(user.full_name)}](tg://user?id={user.telegram_id}) bazaga qo'shildi.\nBazada {count} ta foydalanuvchi bor.")
    else:
        msg = f"[{make_title(user.full_name)}](tg://user?id={user.telegram_id}) bazaga oldin qo'shilgan"
    for admin in settings.ADMINS:
        try:
            await bot.send_message(
                chat_id=admin,
                text=msg,
                parse_mode=ParseMode.MARKDOWN
            )
        except Exception as error:
            logger.info(f"Data did not send to admin: {admin}. Error: {error}")

    await callback_query.message.answer("Ma'lumotlariningiz saqlandi!", reply_markup=reply.main)
    await state.clear()









