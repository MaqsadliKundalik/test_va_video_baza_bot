from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from typing import List
from database.models import Category, Test

main_menu = ReplyKeyboardBuilder()
main_menu.button(text="Testlar") 
main_menu.button(text="Hisobotlar")
main_menu.button(text="📂 Katalog")
main_menu.adjust(2)
main_menu = main_menu.as_markup(resize_keyboard=True)

reports_menu = ReplyKeyboardBuilder()
reports_menu.button(text="Obunachilar")
reports_menu.button(text="A'zolar")
reports_menu.button(text="Reyting")
reports_menu.button(text="Barcha obunalarni tozalash")
reports_menu.button(text="Test yechimlarini tozalash")
reports_menu.button(text="Ortga")
reports_menu.adjust(2, 1)
reports_menu = reports_menu.as_markup(resize_keyboard=True)

back_menu = ReplyKeyboardBuilder()
back_menu.button(text="Ortga")
back_menu = back_menu.as_markup(resize_keyboard=True)

def get_categories_markup(categories: List[Category]):  
    category_menu = ReplyKeyboardBuilder()
    for category in categories:
        category_menu.button(text=category.name)
    category_menu.button(text="➕ Kategoriya qo'shish")
    category_menu.button(text="Ortga")
    category_menu.adjust(2)
    return category_menu.as_markup(resize_keyboard=True)

def category_actions_markup(category_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(text="🔎 Testlarni ko'rish", switch_inline_query_current_chat=f"cat_{category_id}")
    builder.button(text="➕ Test qo'shish", callback_data=f"add_test_{category_id}")
    builder.button(text="❌ Kategoriyani o'chirish", callback_data=f"del_cat_{category_id}")
    builder.adjust(1)
    return builder.as_markup()

def test_actions_markup(test_id: int, has_video: bool = False):
    builder = InlineKeyboardBuilder()
    builder.button(text="❌ Testni o'chirish", callback_data=f"del_test_{test_id}")
    builder.button(text="🔑 Kalitni almashtirish", callback_data=f"edit_key_{test_id}")
    
    if has_video:
        builder.button(text="🎥 Videoni ko'rish", callback_data=f"view_vid_{test_id}")
        builder.button(text="🔄 Videoni almashtirish", callback_data=f"edit_vid_{test_id}")
    else:
        builder.button(text="➕ Video qo'shish", callback_data=f"add_vid_{test_id}")
        
    builder.adjust(1)
    return builder.as_markup()

def approve_subscription_markup(user_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Tasdiqlash", callback_data=f"approve_sub_{user_id}")
    builder.button(text="❌ Rad etish", callback_data=f"reject_sub_{user_id}")
    builder.adjust(1)
    return builder.as_markup()