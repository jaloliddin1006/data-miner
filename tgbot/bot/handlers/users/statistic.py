from aiogram import F, Router, types
from aiogram.types import Voice
from asgiref.sync import sync_to_async
from django.db.models import Count
from tgbot.models import User, Voice, Text
from tgbot.bot.loader import bot
from tgbot.bot.keyboards import reply
from aiogram.enums.parse_mode import ParseMode


router = Router()

@router.message(F.text.in_(['📊 Statistika', '/stat']))
async def check_voice_func(message: types.Message):
    user_id = message.from_user.id
    user = await User.objects.aget(telegram_id=user_id)

    user_checked = await sync_to_async(
        lambda: user.checks.count(),
        thread_sensitive=True
    )()

    user_voices= await sync_to_async(
        lambda: user.voices.count(),
        thread_sensitive=True
    )()

    all_voices = await Voice.objects.acount()
    all_users = await User.objects.acount()

    bot_properties = await bot.me()

    # leadership 
    leaders = await sync_to_async(
        lambda: list(User.objects.annotate(check=Count('checks', distinct=True), voice=Count('voices', distinct=True), leader=Count('checks', distinct=True)*0.2+Count('voices', distinct=True)).order_by('-leader')),
        thread_sensitive=True
    )()

    leaders_text = f"**{bot_properties.full_name}** dagi eng faol top 10 nafar ishtirokchi \n\n"

    pos = 0
    strickers = ["🥇","🥈","🥉","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
    for user in leaders[:10]:
        leaders_text += f"{strickers[pos]}. [{user.full_name}](tg://user?id={user.telegram_id}) |  🎙️ : {user.voice} | ☑︎: {user.check}\n"
        pos += 1

    # text = f"@{bot_properties.username} statistikasi\n\n"
    leaders_text += "\n\n<b>Sizning natijangiz:</b>\n"
    leaders_text += f"🎙️ {user_voices} ta matn o'qidingiz.\n"
    leaders_text += f"☑︎ {user_checked} ta ovozni tekshirdingiz.\n\n"
    leaders_text += f"Jami ishtirokchilar soni: {all_users} ta\n"
    leaders_text += f"Jami yozilgan audiolar soni: {all_voices} ta\n\n"
    leaders_text += f"@{bot_properties.username} "


    # await message.answer(text)

    await message.answer(leaders_text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply.main)

    