from aiogram import Router, types, F
from aiogram.filters import Command
from filters.user import IsSubscribed, IsNewUser
from database.models import User, Subscriptions
from keyboards.user import back_menu
from states.user import UserStates
from aiogram.fsm.context import FSMContext
from keyboards.admin import approve_subscription_markup
from config import CARD_NUMBER, CARD_OWNER, SUBSCRIPTION_PRICE, ADMINS

router = Router()

@router.message(F.text == "💳 Obuna bo'lish")
async def subscription_handler(message: types.Message, state: FSMContext):
    await message.answer(
        f"""
*Obuna bo'lish uchun to'lovni amalga oshiring!*

💳 *Karta raqami:* `{CARD_NUMBER}`
👤 *Karta egasi:* {CARD_OWNER}
💰 *To'lov miqdori:* `{SUBSCRIPTION_PRICE:,}` so'm

To'lovni amalga oshirgandan so'ng, chekni rasmini shu yerga yuboring va tasdiqlanishini kuting.
        """,
         reply_markup=back_menu,
         parse_mode="Markdown"
         )
    await state.set_state(UserStates.waiting_for_subscription_payment)

@router.message(UserStates.waiting_for_subscription_payment, F.photo)
async def subscription_payment_handler(message: types.Message, state: FSMContext):
    await message.answer(
        """
*✅ Chek qabul qilindi! Tasdiqlanishini kuting.*
        """,
         reply_markup=back_menu,
         parse_mode="Markdown"
         )
    for admin in ADMINS:    
        try:
            await message.bot.send_photo(
                admin,
                message.photo[-1].file_id,
                caption=f"""
✅ Yangi obuna so'rovi:

*Ism*: {message.from_user.full_name}
*ID*: `{message.from_user.id}`
                """,
                parse_mode="Markdown",
                reply_markup=approve_subscription_markup(message.from_user.id)
                )
        except Exception as e:
            pass
    await state.clear()

