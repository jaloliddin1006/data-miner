from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    KeyboardButtonPollType,
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

# async def passed_text(text_id: str):
#     builder = InlineKeyboardBuilder()
#     builder.button(text="❌ To'xtatish", callback_data=f"close_record")
#     builder.button(text="🔜 Tashlab ketish", callback_data=f"passed:{text_id}")
#     builder.adjust(1, 1)  
#     return builder.as_markup()


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

maxsus_btn = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="location", request_location=True),
            KeyboardButton(text="contact", request_contact=True),
        ],
        [
            KeyboardButton(text=" poll", request_poll=KeyboardButtonPollType()),
        ],
        [
            KeyboardButton(text="Orqaga")

        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

rmk = ReplyKeyboardRemove()