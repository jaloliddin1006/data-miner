from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove
)

main = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📊 Statistika"),
        ],
        [
            KeyboardButton(text="🎙 Ovoz yozish"),
            KeyboardButton(text="🔊 Tekshirish"),
        ],
        [
            KeyboardButton(text="💬 Fikr qoldirish"),
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


back_btn = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="❌ Bekor qilish"),
        ],
     
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

rmk = ReplyKeyboardRemove()

settings_btn = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Hududni tanlash"),
            KeyboardButton(text="Jinsni tanlash"),
        ],
           [
            KeyboardButton(text="⬅️ Ortga qaytish"),
        ],
     
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

rmk = ReplyKeyboardRemove()