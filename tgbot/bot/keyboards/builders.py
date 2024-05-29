from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder # type: ignore


GENDER_CHOISES = (
    ('erkak', '🤵‍♂️ Erkak'),
    ('ayol', '🤵‍♀️ Ayol')
)

# REGION_CHOISES = (
#     ('001', 'Toshkent shahri'),
#     ('014', 'Andijon'),
#     ('002', 'Buxoro'),
#     ('003', 'Farg`ona'),
#     ('004', 'Jizzax'),
#     ('005', 'Xorazm'),
#     ('006', 'Namangan'),
#     ('007', 'Navoiy'),
#     ('008', 'Qashqadaryo'),
#     ('009', 'Qoraqalpog`iston'),
#     ('010', 'Samarqand'),
#     ('011', 'Sirdaryo'),
#     ('012', 'Surxondaryo'),
#     ('013', 'Toshkent'),
# )

regions = [
    "Toshkent shahri", "Andijon", "Buxoro", "Farg`ona",
    "Jizzax", "Xorazm", "Namangan", "Navoiy",
    "Qoraqalpog`iston",'Samarqand', "Surxondaryo", "Qashqadaryo",
     "Sirdaryo", "Toshkent"
]

def calc_kb():
    items = [
        "1", "2", "3", "+",
        "4", "5", "6", "-",
        "7", "8", "9", "*",
        "0", ".", "=", "/"
    ]

    builder = ReplyKeyboardBuilder()
    [builder.button(text=item) for item in items]

    builder.button(text="Orqaga")
    builder.adjust(*[4] * 4, 1)  # 4, 4, 4, 4, 1

    return builder.as_markup(resize_keyboard=True)


def profile(text):
    builder = ReplyKeyboardBuilder()
    if isinstance(text, str):
        text = [text]
    [builder.button(text=item) for item in text]

    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def check_channel_sub(channels: list):
    builder = InlineKeyboardBuilder()
    [builder.button(text=name, url=link) for name, link in channels]
    return builder.as_markup()




async def check_text(text_id: str):
    builder = InlineKeyboardBuilder()
    builder.button(text="🔄 Qaytadan yozish", callback_data=f"rewrite_record:{text_id}")
    builder.button(text="✅ Saqlash", callback_data=f"correct:{text_id}")
    builder.button(text="❌ Bekor qilish", callback_data=f"wrong:{text_id}")
    builder.adjust(1, 2) 
    return builder.as_markup()


async def check_voice(text_id: str):
    builder = InlineKeyboardBuilder()
    builder.button(text="🔼 Menu", callback_data=f"menu")
    builder.button(text="👍🏻 To'g'ri", callback_data=f"positive:{text_id}")
    builder.button(text="👎 Noto'g'ri", callback_data=f"negative:{text_id}")
    builder.adjust(1, 2) 
    return builder.as_markup()

async def get_gender_btn(sex):
    builder = InlineKeyboardBuilder()
    [builder.button(text=f"{name} ✅" if sex == code else name, callback_data=f"set_gender_{code}") for code, name in GENDER_CHOISES]
    return builder.as_markup()


async def get_region_btn(region):
    builder = InlineKeyboardBuilder()
    [builder.button(text=f"{name} ✅" if region == name else name, callback_data=f"set_region_{name}") for name in regions]
    builder.adjust(1, *[2]*6) 
    return builder.as_markup()
