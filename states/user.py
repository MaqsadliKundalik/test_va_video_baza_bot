from aiogram.fsm.state import State, StatesGroup

class UserStates(StatesGroup):
    waiting_for_subscription_payment = State()

class TestStates(StatesGroup):
    waiting_for_test_answers = State()
