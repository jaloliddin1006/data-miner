from aiogram import Router, types, F


router = Router()


@router.message(F.photo)
async def start_user(message: types.Message):
    # await message.answer(message.text)
    id_photo = message.photo[-1].file_id
    await message.answer_photo(id_photo)
    await message.answer(id_photo)



@router.message()
async def start_user(message: types.Message):
    pass
    # id_photo = message.photo[-1].file_id
    # #А потом просто вот так отправляете где айди это вытащенное фото из бд(к примеру)
    # await message.answer_photo(id_photo)
