from aiogram.filters.state import State, StatesGroup


class Test(StatesGroup):
    Q1 = State()
    Q2 = State()

class RecordState(StatesGroup):
    voice = State()
    check = State()

class FeedBackState(StatesGroup):
    feed = State()

class MessageState(StatesGroup):
    message = State()
    check = State()


class Start(StatesGroup):
    location = State()
    sex = State()