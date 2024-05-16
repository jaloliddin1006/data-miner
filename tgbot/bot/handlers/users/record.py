from aiogram import F, Router, types
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.session.middlewares.request_logging import logger
from aiogram.types import CallbackQuery, Voice
from aiogram.fsm.context import FSMContext
import io
from pydub import AudioSegment
from asgiref.sync import sync_to_async

from tgbot.models import User, Voice, Text, TextPassed
from tgbot.bot.loader import bot, Bot
from django.conf import settings
from tgbot.bot.utils.extra_datas import make_title
from tgbot.bot.keyboards import reply, builders
from tgbot.bot.states.main import RecordState

router = Router()


@router.message(F.text.in_(['🎙 Ovoz yozish', '/record']))
async def record_func(message: types.Message, state: FSMContext, user_id: int = None, text_id: str = None):
    await state.set_state(RecordState.voice)
    if not text_id:
        if user_id:
            user = await User.objects.aget(telegram_id=user_id)
        else:
            user = await User.objects.aget(telegram_id=message.from_user.id)
            await message.answer("Ovoz yozishni boshlang. Matnni o'qib, voice yuboring.")
        # Wrap the synchronous ORM queries with sync_to_async and evaluate them completely within sync_to_async
        user_records = await sync_to_async(
            lambda: list(user.voices.all().values_list("text__text_id", flat=True)),
            thread_sensitive=True
        )()
        # print(user_records)

        user_passed = await sync_to_async(
            lambda: list(user.passed.values_list("text__text_id", flat=True)),
            thread_sensitive=True
        )()
        # print(user_passed)


        # Wrap the filtering and exclusion query in sync_to_async and evaluate it completely
        text = await sync_to_async(
            lambda: Text.objects.filter().exclude(text_id__in=user_records+user_passed).order_by('?').first(),
            thread_sensitive=True
        )()
    else:
        text = await Text.objects.aget(text_id=text_id)
    # print(text)    
    # print(text.text_id)    


    if not text:
        await message.answer("Siz barcha matnlarni o'qib chiqdingiz")
        await state.clear()
        return

 
    await state.update_data(text_id=text.text_id)
    await state.update_data(text=text.text)
    await message.answer(text.text, reply_markup=reply.text_btn)



@router.message(RecordState.voice, F.text=="❌ To'xtatish")
async def pagination_handler(message: types.Message, state: FSMContext):
    await message.answer("Ovoz yozish to'xtatildi!", reply_markup=reply.main)
    await state.clear()


@router.message(RecordState.voice, F.text=="🔜 Tashlab ketish")
async def pagination_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    text_id = data.get("text_id")
    text = await Text.objects.aget(text_id=text_id)
    user = await User.objects.aget(telegram_id=message.from_user.id)
    await sync_to_async(
        TextPassed.objects.create,
        thread_sensitive=True
    )(user=user, text=text)

    await message.answer("👇 Yangi matn.  Matnni o'qib, voice yuboring. 👇")
    await state.clear()
    await record_func(message, state, user_id=message.from_user.id)


@router.message(RecordState.voice, F.content_type == "voice")
async def profile(message: types.Message, state: FSMContext):
    data = await state.get_data()
    text_id = data.get("text_id")
    text = data.get("text")
    voice_id = message.voice.file_id
    await state.update_data(voice_id=voice_id)
    await message.answer("Yozilgan ovozingizni tekshiring.", reply_markup=reply.rmk)
    await message.answer_voice(voice=voice_id, caption=text, reply_markup=await builders.check_text(text_id))
    await state.set_state(RecordState.check)


@router.message(RecordState.voice, F.content_type != "voice")
async def profile(message: types.Message, state: FSMContext):
    await message.answer("Faqat ovoz yuboring")
    await state.set_state(RecordState.voice)




@router.callback_query(RecordState.check, F.data.startswith("correct"))
async def pagination_handler(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    text_id = data.get("text_id")
    voice_id = data.get("voice_id")
    user = await User.objects.aget(telegram_id=call.from_user.id)

    voice = await bot.get_file(voice_id)
    voice_ogg = io.BytesIO()
    await bot.download_file(voice.file_path, voice_ogg)
    
    voice_mp3_path = f"voices/{text_id}.mp3"
    AudioSegment.from_file(voice_ogg, format="ogg").export(
        f"media/{voice_mp3_path}", format="mp3"
    )
    text = await Text.objects.aget(text_id=text_id)

    await sync_to_async(
        Voice.objects.create,
        thread_sensitive=True
    )(user=user, text=text, voice=voice_mp3_path)

    await call.answer()
    await call.message.edit_reply_markup()
    await call.message.answer("Ovoz yozildi! ✅")
    await call.message.answer("👇 Matnni o'qib, voice yuboring. 👇")

    await state.clear()
    await record_func(call.message, state, user_id=call.from_user.id)



@router.callback_query(RecordState.check, F.data.startswith("rewrite_record"))
async def pagination_handler(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("👇 Matnni qaytadan o'qib, voice yuboring. 👇")
    await state.clear()
    await record_func(call.message, state, user_id=call.from_user.id, text_id=call.data.split(":")[1])

@router.callback_query(RecordState.check, F.data.startswith("wrong"))
async def pagination_handler(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("👇 Yangi matnni o'qib, voice yuboring. 👇")
    await state.clear()
    await record_func(call.message, state, user_id=call.from_user.id)

# @router.message(Form.photo, ~F.photo)
# async def profile(message: Message, state: FSMContext):
#     await message.answer("Faqat rasm yuboring")