from uuid import UUID

from app.schemas.base import AdminMeta, BaseResponseSchema


class PaymentResponseSchema(BaseResponseSchema, AdminMeta):
    id: UUID
    user_id: UUID
    payment_id: str
    amount: int
    status: str
