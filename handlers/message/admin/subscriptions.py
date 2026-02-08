from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from database.models import User, Subscriptions
from keyboards.admin import approve_subscription_markup, main_menu
from keyboards.user import main_menu_subscribed_user
from config import ADMINS
from filters.admin import IsAdmin

router = Router()


@router.callback_query(F.data.startswith("approve_sub_"), IsAdmin())
async def approve_subscription(call: types.CallbackQuery):
    user_id = int(call.data.split("_")[2])
    await Subscriptions.create(
        user_id=user_id,
    )
    await call.answer("Obuna tasdiqlandi", show_alert=True)
    await call.message.delete()
    await call.message.answer("Obuna tasdiqlandi", reply_markup=main_menu)
    await call.bot.send_message(user_id, "Tabriklaymiz! Sizning obunangiz tasdiqlandi.", reply_markup=main_menu_subscribed_user)

@router.callback_query(F.data.startswith("reject_sub_"), IsAdmin())
async def reject_subscription(call: types.CallbackQuery):
    user_id = int(call.data.split("_")[2])

    await call.answer("Obuna rad etildi", show_alert=True)
    await call.message.delete()
    await call.message.answer("Obuna rad etildi", reply_markup=main_menu)
    await call.bot.send_message(user_id, "Afsuski, obuna so'rovingiz rad etildi.")

@router.message(F.text == "Barcha obunalarni bekor qilish", IsAdmin())
async def cancel_subscription(message: types.Message):
    subscriptions = await Subscriptions.all().prefetch_related("user")
    if not subscriptions:
        await message.answer("Obunalar yo'q", reply_markup=main_menu)
        return
    txt = ""
    for i, subscription in enumerate(subscriptions):
        txt += f"{i+1}. {subscription.user.full_name}\n"
        if len(txt) > 3000:
            await message.answer(txt)
            txt = ""
    if txt:
        await message.answer(txt)
