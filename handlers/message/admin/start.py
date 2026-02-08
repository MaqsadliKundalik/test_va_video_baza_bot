from aiogram import types, Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from keyboards.admin import main_menu
from filters.admin import IsAdmin

router = Router()

@router.message(CommandStart(), IsAdmin())
async def start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Salom, admin!", reply_markup=main_menu)