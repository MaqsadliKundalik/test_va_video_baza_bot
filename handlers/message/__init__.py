from aiogram import Router
from handlers.message.admin import router as admin_router
from handlers.message.user import router as user_router

router = Router()   
router.include_router(admin_router)
router.include_router(user_router)