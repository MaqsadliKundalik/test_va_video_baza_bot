from aiogram.filters import Filter
from aiogram import types
from database.models import User, Subscriptions
import re

class IsSubscribed(Filter):
    async def __call__(self, message: types.Message) -> bool:
        subscription = await Subscriptions.get_or_none(user_id=message.from_user.id)
        return bool(subscription)

class IsNewUser(Filter):
    async def __call__(self, message: types.Message) -> bool:
        user = await User.get_or_none(tg_id=message.from_user.id)
        return not bool(user)

class TestCodeFilter(Filter):
    async def __call__(self, message: types.Message) -> bool:
        if not message.text:
            return False
        return bool(re.match(r'^\d+-\d+$', message.text))