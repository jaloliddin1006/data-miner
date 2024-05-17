from aiogram import F, Router, types
from aiogram.types import CallbackQuery, Voice
from aiogram.fsm.context import FSMContext
import io, os
from pathlib import Path
from pydub import AudioSegment
from asgiref.sync import sync_to_async

from tgbot.models import User, Voice, Text, TextPassed, VoiceCheck
from tgbot.bot.loader import bot
from tgbot.bot.keyboards import reply, builders
from tgbot.bot.states.main import RecordState

router = Router()

@router.message(F.text.in_(['🔊 Tekshirish', '/checking']))
async def check_voice_func(message: types.Message, state: FSMContext, user_id: int = None):
    await message.answer("Ovozni yaxshilab eshitib ko'ring, matn bilan mos keladimi yoki yo'q?")
    if not user_id:
        user = await User.objects.aget(telegram_id=message.from_user.id)
    else:
        user = await User.objects.aget(telegram_id=user_id)
    user_checked = await sync_to_async(
        lambda: list(user.checks.values_list("voice__id", flat=True)),
        thread_sensitive=True
    )()
    voice = await sync_to_async(
        lambda: Voice.objects.filter().exclude(id__in=user_checked).order_by('?').first(),
        thread_sensitive=True
    )()
    if not voice:
        await message.answer("Siz barcha ovozlarni tekshirib chiqdingiz", reply_markup=reply.main)
        await state.clear()
        return
    voice_id = await sync_to_async(lambda: Voice.objects.get(id=voice.id).voice_id)()
    voice_text = await sync_to_async(lambda: Voice.objects.get(id=voice.id).text.text)()

    await state.update_data(voice_id=voice.id)
    # await state.update_data(text=voice.text.text)
    try:
        await message.answer_voice(voice=voice_id, caption=voice_text, reply_markup=await builders.check_voice(voice.id))
    except Exception as e:  
        await message.answer("Xatolik yuz berdi. Iltimos qaytadan urinib ko'ring", reply_markup=reply.main)
        await state.clear()

@router.callback_query(F.data.startswith("positive") | F.data.startswith("negative"))
async def check_voice(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    voice_id = call.data.split(":")[-1]
    user = await User.objects.aget(telegram_id=call.from_user.id)
    voice = await Voice.objects.aget(id=voice_id)
    if call.data.startswith("positive"):
        is_correct = True
    else:
        is_correct = False
    await VoiceCheck.objects.acreate(user=user, voice=voice, is_correct=is_correct)
    await call.message.delete_reply_markup()
    await call.message.answer("Rahmat!")
    await check_voice_func(call.message, state, user_id=user.telegram_id)
    # await call.message.answer("Rahmat!", reply_markup=reply.main)
    # await state.clear()


@router.callback_query(F.data=='menu')
async def back_to_menu(call: CallbackQuery, state: FSMContext):
    await call.message.delete_reply_markup()
    await call.message.answer("Bosh menuga qaytingiz", reply_markup=reply.main)
    await state.clear()