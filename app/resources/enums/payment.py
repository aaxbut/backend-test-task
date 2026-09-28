from enum import StrEnum


class PaymentStatus(StrEnum):
    """Lifecycle statuses of a payment as reported by the acquiring bank.

    Only ``CONFIRMED`` triggers subscription activation in the webhook
    handler. All other statuses are persisted to ``payments`` for audit
    and analytics, but have no side effects on ``subscriptions``.
    """

    # Funds have been captured successfully. This is the only status
    # that activates (or extends) the user's subscription.
    CONFIRMED = 'CONFIRMED'

    # Payment has been initiated but is awaiting confirmation
    # from the bank. Do not grant access yet.
    PENDING = 'PENDING'

    # Payment was declined by the bank, exceeded the limit, or had
    # insufficient funds. Record the attempt; do not touch the subscription.
    FAILED = 'FAILED'
    # Payment was voided before capture — by the user, the merchant,
    # or the anti-fraud system. Record only; subscription stays untouched.
    CANCELED = 'CANCELED'

    # Captured funds were returned to the user (full or partial).
    # On receipt, the subscription should be revoked or its
    # expires_at collapsed to now().
    REFUNDED = 'REFUNDED'
