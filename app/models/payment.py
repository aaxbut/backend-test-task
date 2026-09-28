from uuid import UUID

from sqlalchemy import CheckConstraint, Column, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column

from app.models import BaseModel
from app.resources.enums import PaymentStatus


class Payment(BaseModel):
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey('user.id', ondelete='RESTRICT'), nullable=False
    )
    payment_id: Mapped[str]
    status: Mapped[PaymentStatus]
    amount: Mapped[int]

    __table_args__ = (
        CheckConstraint('amount >= 0', name='ck_payments_amount_nonneg'),
        Index(
            'payment_id_uq_partial_idx',
            'payment_id',
            unique=True,
            postgresql_where=Column('deleted_at').is_(None),
        ),
    )
