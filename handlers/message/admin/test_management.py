from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.context import FSMContext
from database.models import Category, Test, VideoLessons
from aiogram.fsm.context import FSMContext
from database.models import Category, Test, VideoLessons
from utils.catalog_manager import update_catalog, CATALOG_PATH
from keyboards.admin import get_categories_markup, category_actions_markup, main_menu, back_menu, test_actions_markup
from states.admin import AdminStates
from filters.admin import IsAdmin

router = Router()


@router.message(AdminStates.waiting_for_test_file, IsAdmin())
async def receive_test_file(message: types.Message, state: FSMContext):
    if message.text == "Ortga":
        await state.clear()
        return await show_categories(message)
    
    if not message.document:
        await message.answer("Iltimos, fayl yuboring!")
        return

    file_id = message.document.file_id
    await state.update_data(file_id=file_id)
    await message.answer("Test nomini kiriting:")
    await state.set_state(AdminStates.waiting_for_test_name)

@router.message(AdminStates.waiting_for_test_name, IsAdmin())
async def receive_test_name(message: types.Message, state: FSMContext):
    if message.text == "Ortga":
        await state.clear()
        return await show_categories(message)

    await state.update_data(name=message.text)
    await message.answer("Test kalitlarini yuboring:\n(Masalan: 1a2b3c... yoki abcd...)")
    await state.set_state(AdminStates.waiting_for_test_keys)

@router.message(AdminStates.waiting_for_test_keys, IsAdmin())
async def receive_test_keys(message: types.Message, state: FSMContext):
    if message.text == "Ortga":
        await state.clear()
        return await show_categories(message)

    data = await state.get_data()
    
    await Test.create(
        name=data['name'],
        file_id=data['file_id'],
        test_key=message.text,
        category_id=data['category_id']
    )
    
    await message.answer("✅ Test muvaffaqiyatli saqlandi!")
    await update_catalog()
    await state.clear()
    await show_categories(message)


@router.message(F.text == "Testlar", IsAdmin())
async def show_categories(message: types.Message):
    categories = await Category.all()
    await message.answer(
        "Kategoriyani tanlang yoki yangisini qo'shing:",
        reply_markup=get_categories_markup(categories)
    )

@router.message(F.text == "➕ Kategoriya qo'shish", IsAdmin())
async def ask_category_name(message: types.Message, state: FSMContext):
    await message.answer("Yangi kategoriya nomini kiriting:", reply_markup=back_menu)
    await state.set_state(AdminStates.waiting_for_category_name)

@router.message(AdminStates.waiting_for_category_name, IsAdmin())
async def add_category(message: types.Message, state: FSMContext):
    if message.text == "Ortga":
        await state.clear()
        return await show_categories(message)
    
    name = message.text
    if await Category.filter(name=name).exists():
        await message.answer("Bunday kategoriya mavjud! Boshqa nom kiriting.")
        return

    await Category.create(name=name)
    await message.answer(f"✅ '{name}' kategoriyasi qo'shildi!")
    await state.clear()
    await show_categories(message)

# Handle Category Selection (Text Match)

@router.callback_query(F.data.startswith("del_cat_"), IsAdmin())
async def delete_category(call: types.CallbackQuery):
    cat_id = int(call.data.split("_")[2])
    category = await Category.get_or_none(id=cat_id)
    
    if category:
        await category.delete()
        await call.message.delete()
        await call.answer("Kategoriya o'chirildi!", show_alert=True)
        categories = await Category.all()
        await call.message.answer(
            "Kategoriyalar:",
            reply_markup=get_categories_markup(categories)
        )
    else:
        await call.answer("Kategoriya topilmadi", show_alert=True)

# --- Add Test Flow ---
@router.callback_query(F.data.startswith("add_test_"), IsAdmin())
async def start_add_test(call: types.CallbackQuery, state: FSMContext):
    cat_id = int(call.data.split("_")[2])
    await state.update_data(category_id=cat_id)
    await call.message.delete()
    await call.message.answer("Test faylini yuboring (Excel/Word):", reply_markup=back_menu)
    await state.set_state(AdminStates.waiting_for_test_file)

@router.message(F.text == "Ortga", IsAdmin())
async def go_back(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Bosh menyu:", reply_markup=main_menu)

# --- Test Action Handlers --- 

@router.callback_query(F.data.startswith("del_test_"), IsAdmin())
async def delete_test(call: types.CallbackQuery):
    test_id = int(call.data.split("_")[2])
    test = await Test.get_or_none(id=test_id)
    
    if test:
        await test.delete()
        # Also delete associated video if any
        video = await VideoLessons.get_or_none(test_id=test_id)
        if video:
            await video.delete()
            
        await call.answer("Test va uning videolari o'chirildi!", show_alert=True)
        # Edit message to show it's deleted
        try:
            await call.message.edit_caption(caption="❌ Bu test o'chirilgan.")
        except:
            await call.message.delete()
        
        await update_catalog()
    else:
        await call.answer("Test topilmadi", show_alert=True)

@router.callback_query(F.data.startswith("edit_key_"), IsAdmin())
async def start_edit_key(call: types.CallbackQuery, state: FSMContext):
    test_id = int(call.data.split("_")[2])
    test = await Test.get_or_none(id=test_id)
    
    if not test:
        return await call.answer("Test topilmadi", show_alert=True)

    await state.update_data(editing_test_id=test_id)
    await state.set_state(AdminStates.waiting_for_new_key)
    await call.message.answer(f"Test: {test.name}\nYangi kalitni yuboring:", reply_markup=back_menu)
    await call.answer()

@router.message(AdminStates.waiting_for_new_key, IsAdmin())
async def save_new_key(message: types.Message, state: FSMContext):
    if message.text == "Ortga":
        await state.clear()
        return await show_categories(message)
        
    data = await state.get_data()
    test_id = data.get('editing_test_id')
    
    test = await Test.get_or_none(id=test_id)
    if test:
        test.test_key = message.text
        await test.save()
        await message.answer("✅ Test kaliti yangilandi!")
        # Optional: return to category view
    else:
        await message.answer("Xatolik: Test topilmadi.")
        
    await state.clear()

# --- Video Actions ---
@router.callback_query(F.data.startswith("view_vid_"), IsAdmin())
async def view_video(call: types.CallbackQuery):
    test_id = int(call.data.split("_")[2])
    video = await VideoLessons.get_or_none(test_id=test_id)
    
    if video:
        await call.message.answer_video(video.file_id, caption=f"Video dars: {video.caption}")
        await call.answer()
    else:
        await call.answer("Video topilmadi", show_alert=True)

@router.callback_query(F.data.startswith("add_vid_"), IsAdmin())
async def start_add_video(call: types.CallbackQuery, state: FSMContext):
    test_id = int(call.data.split("_")[2])
    await state.update_data(video_test_id=test_id)
    await state.set_state(AdminStates.waiting_for_video)
    await call.message.delete()
    await call.message.answer("Video faylni yuboring:", reply_markup=back_menu)
    await call.answer()

@router.callback_query(F.data.startswith("edit_vid_"), IsAdmin())
async def start_edit_video(call: types.CallbackQuery, state: FSMContext):
    test_id = int(call.data.split("_")[2])
    await state.update_data(video_test_id=test_id)
    await state.set_state(AdminStates.waiting_for_video)
    await call.message.delete()
    await call.message.answer("Yangi video faylni yuboring:", reply_markup=back_menu)
    await call.answer()

@router.message(AdminStates.waiting_for_video, IsAdmin())
async def receive_video_file(message: types.Message, state: FSMContext):
    if message.text == "Ortga":
        await state.clear()
        return await show_categories(message)
    
    if not message.video:
        await message.answer("Iltimos, video yuboring!")
        return
        
    await state.update_data(video_file_id=message.video.file_id)
    await message.answer("Video uchun izoh (caption) yozing:")
    await state.set_state(AdminStates.waiting_for_video_caption)

@router.message(AdminStates.waiting_for_video_caption, IsAdmin())
async def receive_video_caption(message: types.Message, state: FSMContext):
    if message.text == "Ortga":
        await state.clear()
        return await show_categories(message)

    data = await state.get_data()
    test_id = data.get('video_test_id')
    file_id = data.get('video_file_id')
    caption = message.text
    
    video = await VideoLessons.get_or_none(test_id=test_id)
    if video:
        video.file_id = file_id
        video.caption = caption
        await video.save()
        await message.answer("✅ Video yangilandi!")
    else:
        await VideoLessons.create(
            test_id=test_id,
            file_id=file_id,
            caption=caption
        )
        await message.answer("✅ Video qo'shildi!")
        
    await state.clear()

@router.message(F.text.startswith("/manage_test_"), IsAdmin())
async def manage_test_command(message: types.Message):
    try:
        test_id = int(message.text.split("_")[2])
    except (ValueError, IndexError):
        await message.answer("Test topilmadi.")
        return

    test = await Test.get_or_none(id=test_id)
    if not test:
        await message.answer("Test topilmadi.")
        return

    video = await VideoLessons.get_or_none(test_id=test.id)
    has_video = video is not None

    await message.answer_document(
        document=test.file_id,
        caption=f"📄 **Test**: {test.name}\n🔑 **Kalit**: `{test.test_key}`",
        parse_mode="Markdown",
        reply_markup=test_actions_markup(test.id, has_video)
    )
    # Delete the command message to keep chat clean
    try:
        await message.delete()
    except:
        pass

@router.message(F.text == "📂 Katalog", IsAdmin())
async def catalog_command(message: types.Message):
    await message.answer_document(types.FSInputFile(CATALOG_PATH))

@router.message(lambda message: message.text not in ["Testlar", "➕ Kategoriya qo'shish", "Ortga"] and message.text and not message.text.startswith("/"), IsAdmin())
async def category_selected(message: types.Message):
    category = await Category.get_or_none(name=message.text)
    if not category:
        return 
        
    await message.answer(
        f"Kategoriya: {category.name}\nAmalni tanlang:",
        reply_markup=category_actions_markup(category.id)
    )
