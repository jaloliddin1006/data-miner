from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove
)

main = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🎙 Ovoz yozish"),
            KeyboardButton(text="🔊 Tekshirish"),
        ],
        [
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Biror birini tanlang",
    selective=True

)


text_btn = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="❌ To'xtatish"),
            KeyboardButton(text="🔜 Tashlab ketish"),
        ],
     
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)


rmk = ReplyKeyboardRemove()