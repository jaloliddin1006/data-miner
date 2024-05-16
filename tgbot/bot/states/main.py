from aiogram.filters.state import State, StatesGroup


class Test(StatesGroup):
    Q1 = State()
    Q2 = State()

class RecordState(StatesGroup):
    voice = State()
    check = State()