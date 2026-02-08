from aiogram import Router
from .start import router as start_router
from .test_management import router as test_router
from .subscriptions import router as subscriptions_router
from .reports import router as reports_router

router = Router()
router.include_router(start_router)
router.include_router(reports_router)
router.include_router(test_router)
router.include_router(subscriptions_router)
