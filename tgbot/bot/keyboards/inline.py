from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from tgbot.models import Channel
# ssilki_kb = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [
#             InlineKeyboardButton(text="Telegram", url="https://t.me/Mamatmusayev_uz"),
#             InlineKeyboardButton(text="Youtube", url="https://youtube.com/mamatmusayev.uz/")
#         ],

#     ]
# )


message_format = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="HTML", callback_data='HTML'),
            InlineKeyboardButton(text="Markdown", callback_data='Markdown')
        ],

    ]
)

message_check = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Send Message", callback_data='send'),
            InlineKeyboardButton(text="❌ Cancel", callback_data='cancel')
        ],

    ]
)
