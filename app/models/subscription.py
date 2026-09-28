from datetime import datetime
from uuid import UUID

from sqlalchemy import Column, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column

from app.models import BaseModel
from app.resources.enums import SubscriptionStatus


class Subscription(BaseModel):
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey('user.id', ondelete='RESTRICT'), nullable=False
    )
    status: Mapped[SubscriptionStatus]

    expires_at: Mapped[datetime]

    __table_args__ = (
        Index(
            'subscription_user_id_uq_partial_idx',
            'user_id',
            unique=True,
            postgresql_where=Column('deleted_at').is_(None),
        ),
    )
