import logging
from datetime import UTC, datetime, timedelta
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Payment, Subscription
from app.repos.payment import PaymentRepo
from app.resources.enums import PaymentStatus, SubscriptionStatus
from app.schemas.payment import PaymentRequestSchema, PaymentResponseSchema
from app.schemas.subscription import SubscriptionRequestSchema
from app.services.base import SoftDeletableService
from app.services.subscription import SubscriptionService

logger = logging.getLogger(__name__)


WRONG_PAYMENT_STATUS = 'Payment status is not CONFIRMED: {status}'


class PaymentService(SoftDeletableService[UUID, Payment, PaymentResponseSchema]):
    response_schema = PaymentResponseSchema
    repo: PaymentRepo

    def __init__(
        self,
        repo: PaymentRepo,
        subscription_service: SubscriptionService,
    ) -> None:
        super().__init__(repo)
        self.subscription_service = subscription_service

    async def payment_processing(
        self,
        db_session: AsyncSession,
        data: PaymentRequestSchema,
    ) -> PaymentResponseSchema:

        if not data.status == PaymentStatus.CONFIRMED:
            raise ValueError(WRONG_PAYMENT_STATUS.format(status=data.status))

        async with db_session.begin_nested():
            try:
                payment = self.repo.get_payment_by_payment_id(payment_id=data.payment_id)
                payment = await self.execute(db_session=db_session, query=payment)
                if payment:
                    logger.info('Payment %s already processed', data.payment_id)
                    return PaymentResponseSchema.model_validate(payment)

                payment = Payment(**data.model_dump())
                db_session.add(payment)
                await db_session.flush()
                subscription = self.subscription_service.repo.get_subscription_by_user_id(
                    user_id=data.user_id
                )

                subscription = await self.execute(db_session=db_session, query=subscription)
                expires_at = datetime.now(UTC).replace(tzinfo=None) + timedelta(days=30)
                if not subscription:
                    subscription = Subscription(
                        **SubscriptionRequestSchema(
                            user_id=data.user_id,
                            status=SubscriptionStatus.ACTIVE,
                            expires_at=expires_at,
                        ).model_dump()
                    )
                else:
                    subscription.expires_at = expires_at
                    subscription.status = SubscriptionStatus.ACTIVE

                db_session.add(subscription)
                await db_session.flush()
                logger.info('Successfully processed payment %s', data.payment_id)
            except IntegrityError as e:
                logger.warning(
                    'Payment %s already exists (race condition): %s', data.payment_id, e
                )

                payment_query = self.repo.get_payment_by_payment_id(data.payment_id)
                existing_payment = await self.execute(db_session=db_session, query=payment_query)

                if existing_payment:
                    logger.info('Found existing payment %s after race condition', data.payment_id)
                    return PaymentResponseSchema.model_validate(existing_payment)

                logger.exception('IntegrityError but payment %s not found', data.payment_id)
                raise ValueError(WRONG_PAYMENT_STATUS.format(status=data.status)) from e

        return PaymentResponseSchema.model_validate(payment)
