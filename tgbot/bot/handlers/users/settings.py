from aiogram import F, Router, types
from aiogram.types import CallbackQuery, Voice
from aiogram.fsm.context import FSMContext
from asgiref.sync import sync_to_async

from tgbot.models import Feedback, User
from tgbot.bot.loader import bot
from tgbot.bot.keyboards import reply, builders
from tgbot.bot.states.main import FeedBackState
from tgbot.bot.utils import check_channel_member

router = Router()

@router.message(F.text.in_(['/settings']))
async def settings_func_start(message: types.Message, state: FSMContext):
    # user = await User.objects.aget(telegram_id=message.chat.id)
    text = "Sizning ma'lumotlaringizni o'zgartirish bo'limi."
    await message.answer(text)
    await message.answer("O'zgartirmoqchi bo'lgan bo'limingizni tanlang", reply_markup=reply.settings_btn)


@router.message(F.text == 'Hududni tanlash')
async def settings_func_location(message: types.Message):
    user = await User.objects.aget(telegram_id=message.from_user.id)
    await message.answer("O'z hududingizni tanlang:", reply_markup=await builders.get_region_btn(user.location))

@router.message(F.text == 'Jinsni tanlash')
async def settings_func_sex(message: types.Message):
    user = await User.objects.aget(telegram_id=message.from_user.id)
    await message.answer("O'z jinsingizni tanlang:", reply_markup=await builders.get_gender_btn(user.sex))


@router.callback_query(F.data.startswith('set_region_'))
async def back_to_menu(call: CallbackQuery, state: FSMContext):
    user = await User.objects.aget(telegram_id=call.from_user.id)
    data = call.data
    user.location = data.split('_')[-1]
    await user.asave()

    await call.message.delete()
    await call.message.answer("Hudud o'zgartirildi", reply_markup=reply.settings_btn)


@router.callback_query(F.data.startswith('set_gender_'))
async def back_to_menu(call: CallbackQuery, state: FSMContext):
    user = await User.objects.aget(telegram_id=call.from_user.id)
    data = call.data

    user.sex = data.split('_')[-1]
    await user.asave()

    await call.message.delete()
    await call.message.answer("Ma'lumot o'zgartirildi", reply_markup=reply.settings_btn)


@router.message(F.text == '❌ Bekor qilish')
async def settings_func(message: types.Message):
    await message.answer("Asosiy sahifa", reply_markup=reply.main)
