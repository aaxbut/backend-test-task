from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.containers import AppContainer
from app.core.db import managed_db_session
from app.dependencies.db_session import get_db_session
from app.dependencies.sign import is_authorize_bank_payment
from app.schemas.payment import PaymentRequestSchema, PaymentResponseSchema
from app.services.payment import PaymentService

router = APIRouter(prefix='/payment', tags=['Payment'])


@router.post('/', name='webhook:payment')
@managed_db_session
async def payment(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    service: Annotated[PaymentService, Depends(AppContainer.payment_service)],
    _: Annotated[bool, Depends(is_authorize_bank_payment)],
    data: PaymentRequestSchema,
) -> PaymentResponseSchema:
    payment_response = await service.payment_processing(
        db_session,
        data=data,
    )
    return payment_response
