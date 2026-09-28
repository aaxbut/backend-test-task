from fastapi import APIRouter

from app.views.webhook.payment import router as payment_router

router = APIRouter(prefix='/webhook', tags=['Webhook'])

router.include_router(payment_router)
