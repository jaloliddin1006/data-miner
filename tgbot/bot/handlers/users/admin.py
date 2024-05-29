from aiogram import F, Router, types
from aiogram.types import CallbackQuery, Voice
from aiogram.fsm.context import FSMContext
from asgiref.sync import sync_to_async
from django.db.models import Count, Sum
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.session.middlewares.request_logging import logger
from tgbot.utils import get_admins

from tgbot.models import User, Voice, Text, TextPassed, VoiceCheck
from tgbot.bot.loader import bot
from tgbot.bot.keyboards import reply, builders, inline
from tgbot.bot.states.main import MessageState

router = Router()


@router.message(F.text == '/users')
async def feedback_func(message: types.Message, state: FSMContext):
    all_users = await User.objects.acount()
    text = "Hurmatli admin!\n\n"
    text += f"Bot foydalanuvchilari soni: {all_users}"

    await message.reply(text)
    await message.answer("Adminning boshqa funksiyalari tez orada qo'shiladi :)")


@router.message(F.text=='/message')
async def message_format_func(message: types.Message, state=FSMContext):
    await state.set_state(MessageState.message)
    await state.update_data(format='HTML')
    
    await message.answer("Foydalanuvchilarga yubormoqchi bo'lgan xabaringizni yozing:", reply_markup=reply.rmk)
    # await message.answer("Xabaringiz formatini tanlang (now: HTML)", reply_markup=inline.message_format)




@router.message(MessageState.message, F.text)
async def message_format_func(message: types.Message, state=FSMContext):

    users = await sync_to_async(
        lambda: list(User.objects.all().values_list('telegram_id', flat=True)),
        thread_sensitive=True
    )()
    msg = message.text
    msg_f = ParseMode.HTML

    # admins = await get_admins()

    for user in users:
        try:
            await bot.send_message(
                chat_id=user,
                text=msg,
                parse_mode=msg_f
            )
        except Exception as error:
            logger.info(f"Message did not send to user: {user}. Error: {error}")

    await message.answer(f"Xabar yuborildi!", reply_markup=reply.main)
    await state.clear()



@router.message(MessageState.message, ~F.text)
async def message_format_func(message: types.Message, state=FSMContext):
    await message.answer("Hozirda faqat matnli xabar yubora olasiz!!!", reply_markup=reply.main)
    await state.clear()



# @router.callback_query(MessageState.message)
# async def pagination_handler(call: CallbackQuery, state: FSMContext):
#     data = await state.get_data()
#     msg_format = data.get("format")
#     if msg_format == 'HTML':
#         msg_f = 'MARKDOWN'
#     else:
#         msg_f = 'HTML'

#     await call.message.edit_text(f"Xabaringiz formatini tanlang (now: {msg_f})")
#     await state.update_data(format=msg_f)




# @router.message(MessageState.message, F.text)
# async def message_format_func(message: types.Message, state=FSMContext):
#     await state.set_state(MessageState.check)
#     data = await state.get_data()
#     msg_format = data.get("format")
   
#     if msg_format == 'HTML':
#         msg_f = ParseMode.HTML
#     else:
#         msg_f = ParseMode.MARKDOWN

#     msg = message.text
#     await message.answer(msg, parse_mode=msg_f, reply_markup=inline.message_check)
#     await state.update_data(message_text=msg)



# @router.callback_query(MessageState.check, F.data=='send')
# async def pagination_handler(call: CallbackQuery, state: FSMContext):
#     data = await state.get_data()
#     msg_format = data.get("format")
#     msg = data.get("message_text")

#     users = await sync_to_async(
#         lambda: list(User.objects.all().values_list('telegram_id', flat=True)),
#         thread_sensitive=True
#     )()
#     print(users)

#     if msg_format == 'HTML':
#         msg_f = ParseMode.HTML
#     else:
#         msg_f = ParseMode.MARKDOWN
#     admins = get_admins()
#     for user in admins:
#         try:
#             await bot.send_message(
#                 chat_id=user,
#                 text=msg,
#                 parse_mode=msg_f
#             )
#         except Exception as error:
#             logger.info(f"Message did not send to user: {user}. Error: {error}")

#     await call.message.answer(f"Assalomu alaykum !", reply_markup=reply.main)
#     await state.clear()




# @router.callback_query(MessageState.check, F.data=='cancel')
# async def pagination_handler(call: CallbackQuery, state: FSMContext):
#     await call.message.answer("Xabar yuborish bekor qilindi!!!", reply_markup=reply.main)
#     await state.clear()