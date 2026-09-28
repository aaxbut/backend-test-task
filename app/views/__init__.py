from fastapi import APIRouter

from app.views.auth import router as auth_router
from app.views.system import router as system_router
from app.views.webhook import router as webhook_router

router = APIRouter()

router.include_router(system_router)
router.include_router(auth_router)
router.include_router(webhook_router)
