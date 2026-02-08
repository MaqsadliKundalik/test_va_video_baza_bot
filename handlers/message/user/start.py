from aiogram import Router, types, F
from aiogram.filters import CommandStart
from keyboards.user import main_menu_subscribed_user, main_menu_unsubscribed_user
from filters.user import IsSubscribed, IsNewUser
from aiogram.fsm.context import FSMContext
from database.models import User

router = Router()

@router.message(IsNewUser())
async def new_user_handler(message: types.Message):
    await message.answer(f"Assalomu alaykum, {message.from_user.full_name}!\nBotga xush kelibsiz. ilk", reply_markup=main_menu_unsubscribed_user)
    await User.create(tg_id=message.from_user.id, username=message.from_user.username, full_name=message.from_user.full_name)

@router.message(IsSubscribed(), CommandStart())
async def subscribed_user_handler(message: types.Message):
    await message.answer(f"Assalomu alaykum, {message.from_user.full_name}!\nBotga xush kelibsiz. Obuna bo'lgan", reply_markup=main_menu_subscribed_user)

@router.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer(f"Assalomu alaykum, {message.from_user.full_name}!\nBotga xush kelibsiz. obuna bo'linmagan", reply_markup=main_menu_unsubscribed_user)

# back menu
@router.message(F.text == "🔙 Ortga", IsSubscribed())
async def back_menu_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(f"Assalomu alaykum, {message.from_user.full_name}!\nBotga xush kelibsiz.", reply_markup=main_menu_subscribed_user)

@router.message(F.text == "🔙 Ortga")
async def back_menu_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(f"Assalomu alaykum, {message.from_user.full_name}!\nBotga xush kelibsiz.", reply_markup=main_menu_unsubscribed_user)