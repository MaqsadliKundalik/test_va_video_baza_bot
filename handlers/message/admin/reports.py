from aiogram import Router, F, types
from aiogram.types import BufferedInputFile
from database.models import Subscriptions, TestAnswers
from keyboards.admin import reports_menu, main_menu
from utils.excel import generate_subscribers_report, generate_members_report, generate_rating_report
from filters.admin import IsAdmin
from datetime import datetime

router = Router()

@router.message(F.text == "Hisobotlar", IsAdmin())
async def show_reports_menu(message: types.Message):
    await message.answer("Hisobotlar bo'limi:", reply_markup=reports_menu)

@router.message(F.text == "Obunachilar", IsAdmin())
async def send_subscribers_report(message: types.Message):
    msg = await message.answer("Hisobot tayyorlanmoqda...")
    file_buffer = await generate_subscribers_report()
    input_file = BufferedInputFile(file_buffer.getvalue(), filename=f"obunachilar_{datetime.now().strftime('%Y-%m-%d')}.xlsx")
    await msg.delete()
    await message.answer_document(input_file, caption="Obunachilar ro'yxati")

@router.message(F.text == "A'zolar", IsAdmin())
async def send_members_report(message: types.Message):
    msg = await message.answer("Hisobot tayyorlanmoqda...")
    file_buffer = await generate_members_report()
    input_file = BufferedInputFile(file_buffer.getvalue(), filename=f"azolar_{datetime.now().strftime('%Y-%m-%d')}.xlsx")
    await msg.delete()
    await message.answer_document(input_file, caption="A'zolar ro'yxati")

@router.message(F.text == "Reyting", IsAdmin())
async def send_rating_report(message: types.Message):
    msg = await message.answer("Hisobot tayyorlanmoqda...")
    file_buffer = await generate_rating_report()
    input_file = BufferedInputFile(file_buffer.getvalue(), filename=f"reyting_{datetime.now().strftime('%Y-%m-%d')}.xlsx")
    await msg.delete()
    await message.answer_document(input_file, caption="Reyting hisoboti")

@router.message(F.text == "Barcha obunalarni tozalash", IsAdmin())
async def clear_all_subscriptions(message: types.Message):
    count = await Subscriptions.all().count()
    await Subscriptions.all().delete()
    await message.answer(f"✅ Barcha obunalar tozalandi! O'chirilganlar soni: {count}")

@router.message(F.text == "Test yechimlarini tozalash", IsAdmin())
async def clear_all_test_solutions(message: types.Message):
    count = await TestAnswers.all().count()
    await TestAnswers.all().delete()
    await message.answer(f"✅ Barcha test yechimlari tozalandi! O'chirilganlar soni: {count}")

@router.message(F.text == "Ortga", IsAdmin())
async def back_to_main(message: types.Message):
    await message.answer("Bosh menyu:", reply_markup=main_menu)

@router.message(IsAdmin())
async def f(message: types.Message):
    pass