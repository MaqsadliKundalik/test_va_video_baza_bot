from aiogram import Router
from handlers.message import router as message_router
from handlers.callback import router as callback_router
from handlers.inline import router as inline_router

router = Router()   
router.include_router(message_router)
router.include_router(callback_router)  
router.include_router(inline_router)