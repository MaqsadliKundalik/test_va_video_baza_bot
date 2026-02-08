from aiogram import Router
from .start import router as start_router
from .subscription import router as subscription_router
from .tests import router as tests_router

router = Router()
router.include_router(start_router)
router.include_router(subscription_router)
router.include_router(tests_router)