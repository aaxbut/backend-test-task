from enum import StrEnum


class SubscriptionStatus(StrEnum):
    """Lifecycle statuses of a subscription."""

    ACTIVE = 'ACTIVE'
    EXPIRED = 'EXPIRED'
    CANCELED = 'CANCELED'
    PAUSED = 'PAUSED'
    REFUNDED = 'REFUNDED'
