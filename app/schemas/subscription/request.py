from datetime import datetime
from uuid import UUID

from app.resources.enums import SubscriptionStatus
from app.schemas.base import BaseRequestSchema


class SubscriptionRequestSchema(BaseRequestSchema):
    user_id: UUID
    status: SubscriptionStatus = SubscriptionStatus.ACTIVE
    expires_at: datetime
