from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from filters.user import IsSubscribed, TestCodeFilter
from database.models import Test, TestAnswers, VideoLessons
from keyboards.user import ready_markup, back_menu, main_menu_subscribed_user
from states.user import TestStates

router = Router()

@router.message(F.text == "📂 Katalog")
async def catalog_handler(message: types.Message):
    await message.answer_document(types.FSInputFile("catalog.docx"))

@router.message(IsSubscribed(), TestCodeFilter())
async def tests_handler(message: types.Message):
    test_id = int(message.text.split("-")[1])
    test = await Test.get(id=test_id)
    await message.answer(f"""
{test.name} testini ishlashga tayyormisiz?
    """, reply_markup=ready_markup(test_id))

@router.callback_query(F.data.startswith("ready_"), IsSubscribed())
async def ready_test(call: types.CallbackQuery, state: FSMContext):
    test_id = int(call.data.split("_")[1])
    test = await Test.get(id=test_id)

    await call.message.edit_reply_markup(reply_markup=None)
    await call.answer()
    await call.message.answer_document(test.file_id, protect_content=True)
    await call.message.answer("""
    Testni ishlab bo'lib, javoblaringizni quyidagi formatlardan biri asosida yuboring.

1-A,2-B,3-C,...
1-a,2-b,3-c,...
1A2B3C...
1a2b3c...
1A,2B,3C,...
1a,2b,3c,...
    """, reply_markup=back_menu)
    await state.update_data(test=test)
    await state.set_state(TestStates.waiting_for_test_answers)

@router.message(TestStates.waiting_for_test_answers, IsSubscribed())
async def test_answers_handler(message: types.Message, state: FSMContext):
    import re
    data = await state.get_data()
    test: Test = data.get("test")
    
    user_matches = re.findall(r'(\d+)[-,\s]*([a-zA-Z])', message.text)
    
    if not user_matches:
        await message.answer("Javoblar formati noto'g'ri. Iltimos, qaytadan yuboring.")
        return

    user_answers = {int(num): ans.upper() for num, ans in user_matches}
    
    correct_raw = test.test_key.upper()
    if re.search(r'\d', correct_raw):
        correct_matches = re.findall(r'(\d+)[-,\s]*([a-zA-Z])', correct_raw)
        correct_map = {int(num): ans.upper() for num, ans in correct_matches}
    else:
        correct_map = {i + 1: char for i, char in enumerate(correct_raw)}

    correct_count = sum(1 for q_num, ans in user_answers.items() if correct_map.get(q_num) == ans)
    total_questions = len(correct_map)

    results = []
    sorted_keys = sorted(correct_map.keys())
    for key in sorted_keys:
        if user_answers.get(key) == correct_map[key]:
            results.append(f"{key}. ✅")
        else:
            results.append(f"{key}. ❌")

    rows = []
    for i in range(0, len(results), 3):
        rows.append("   ".join(results[i:i+3]))

    result_text = "\n".join(rows)

    await message.answer(
        f"🏁 Test yakunlandi!\n\n"
        f"📝 Test: {test.name}\n"
        f"✅ To'g'ri javoblar: {correct_count}\n"
        f"❌ Noto'g'ri javoblar: {total_questions - correct_count}\n"
        f"📊 Natija: {correct_count}/{total_questions}\n\n"
        f"{result_text}",
        reply_markup=main_menu_subscribed_user
    )

    await TestAnswers.create(
        test_id=test.id,
        user_id=message.from_user.id,
        answer=message.text,
        score=correct_count
    )
    await state.clear()
    video_lesson = await VideoLessons.filter(test_id=test.id).first()
    if video_lesson:
        await message.answer_video(
            video_lesson.file_id, 
            caption=f"""
{video_lesson.caption}
            """, 
            reply_markup=main_menu_subscribed_user,
            protect_content=True    
        )