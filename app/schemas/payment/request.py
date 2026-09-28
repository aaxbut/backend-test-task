from uuid import UUID

from app.resources.enums import PaymentStatus
from app.schemas.base import BaseRequestSchema


class PaymentRequestSchema(BaseRequestSchema):
    user_id: UUID
    payment_id: str
    amount: int
    status: PaymentStatus = PaymentStatus.PENDING
