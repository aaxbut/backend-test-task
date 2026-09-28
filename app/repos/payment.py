from uuid import UUID

from sqlalchemy import Select, select

from app.models import Payment
from app.repos.base import SoftDeletableRepo


class PaymentRepo(SoftDeletableRepo[UUID, Payment]):
    def get_payment_by_payment_id(self, payment_id: str) -> Select:
        return select(self.model).where(self.model.payment_id == payment_id).with_for_update()
