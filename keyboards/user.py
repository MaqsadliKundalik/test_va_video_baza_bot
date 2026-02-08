from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

main_menu_subscribed_user = ReplyKeyboardBuilder()
main_menu_subscribed_user.button(text="📂 Katalog")
main_menu_subscribed_user = main_menu_subscribed_user.as_markup(resize_keyboard=True)

main_menu_unsubscribed_user = ReplyKeyboardBuilder()
main_menu_unsubscribed_user.button(text="📂 Katalog")
main_menu_unsubscribed_user.button(text="💳 Obuna bo'lish")
main_menu_unsubscribed_user = main_menu_unsubscribed_user.as_markup(resize_keyboard=True)   

back_menu = ReplyKeyboardBuilder()
back_menu.button(text="⬅️ Ortga")
back_menu = back_menu.as_markup(resize_keyboard=True)

def ready_markup(test_id: int):
    ready_markup = InlineKeyboardBuilder()
    ready_markup.button(text="Tayyorman!", callback_data=f"ready_{test_id}")
    return ready_markup.as_markup()