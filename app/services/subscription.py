from uuid import UUID

from app.models import Subscription
from app.repos.subscription import SubscriptionRepo
from app.schemas.subscription import SubscriptionResponseSchema
from app.services.base import SoftDeletableService


class SubscriptionService(SoftDeletableService[UUID, Subscription, SubscriptionResponseSchema]):
    response_schema = SubscriptionResponseSchema
    repo: SubscriptionRepo
