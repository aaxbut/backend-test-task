from uuid import UUID

from sqlalchemy import select

from app.models import Subscription
from app.repos.base import SoftDeletableRepo


class SubscriptionRepo(SoftDeletableRepo[UUID, Subscription]):
    def get_subscription_by_user_id(self, user_id: UUID):
        return select(self.model).where(self.model.user_id == user_id).with_for_update()
