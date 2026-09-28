from uuid import UUID

from app.schemas.base import AdminMeta, BaseResponseSchema


class SubscriptionResponseSchema(BaseResponseSchema, AdminMeta):
    id: UUID
    user_id: UUID
    status: str
