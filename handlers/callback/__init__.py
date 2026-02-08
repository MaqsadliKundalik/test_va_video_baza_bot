from aiogram import Router
from handlers.callback.admin import router as admin_router
from handlers.callback.user import router as user_router

router = Router()   
router.include_router(admin_router)
router.include_router(user_router)