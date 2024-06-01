from aiogram import F, Router, types
from aiogram.types import CallbackQuery, Voice
from aiogram.fsm.context import FSMContext
from asgiref.sync import sync_to_async
from aiogram.types import InputFile
from tgbot.models import User, Voice, VoiceCheck
from tgbot.bot.keyboards import reply, builders


router = Router()

@router.message(F.text.in_(['🔊 Tekshirish', '/checking']))
async def check_voice_func(message: types.Message, state: FSMContext, user_id: int = None):
    
    if not user_id:
        await message.answer("Ovozni yaxshilab eshitib ko'ring, matn bilan mos keladimi yoki yo'q?", reply_markup=reply.rmk)
        user = await User.objects.aget(telegram_id=message.from_user.id)
    else:
        user = await User.objects.aget(telegram_id=user_id)
        
    user_checked = await sync_to_async(
        lambda: list(user.checks.values_list("voice__id", flat=True)),
        thread_sensitive=True)()
    
    voice = await sync_to_async(
        lambda: Voice.objects.exclude(id__in=user_checked).exclude(user__telegram_id=user.telegram_id).order_by('?').first(),
        thread_sensitive=True)()
    
    if not voice:
        await message.answer("Siz barcha ovozlarni tekshirib chiqdingiz", reply_markup=reply.main)
        await state.clear()
        return
    
    voice_text = await sync_to_async(
        lambda: voice.text.text,
        thread_sensitive=True)()
    
    voice_id = voice.voice_id
    
    try:
        if isinstance(voice_id, (str, InputFile)):
            await message.answer_voice(voice=voice_id, caption=voice_text, reply_markup=await builders.check_voice(voice.id))
        else:
            raise ValueError("Invalid type for voice_id. Must be a string or an instance of InputFile.")
    except Exception as e:
        print(e)
        await message.answer("Xatolik yuz berdi. Iltimos qaytadan urinib ko'ring", reply_markup=reply.main)
        await state.clear()

@router.callback_query(F.data.startswith("positive") | F.data.startswith("negative"))
async def check_voice(call: CallbackQuery, state: FSMContext):
    voice_id = call.data.split(":")[-1]
    user_id = call.from_user.id
    
    voice = await Voice.objects.aget(id=voice_id)
    user = await User.objects.aget(telegram_id=user_id)
    
    if call.data.startswith("positive"):
        is_correct = True
    else:
        is_correct = False
        
    await VoiceCheck.objects.acreate(user=user, voice=voice, is_correct=is_correct)
    await call.answer("Rahmat!")
    await call.message.delete()
    await check_voice_func(call.message, state, user_id=user_id)


@router.callback_query(F.data=='menu')
async def back_to_menu(call: CallbackQuery, state: FSMContext):
    await call.answer("O'z hissangizni qo'shganingizdan xursandmiz!\nKeyinroq yana davom eting :)", show_alert=True)
    await call.message.delete()
    await call.message.answer("Bosh menu", reply_markup=reply.main)
    await state.clear()