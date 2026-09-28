from app.models.payment import Payment
from app.schemas.payment.response import PaymentResponseSchema
from tests.factories.base import BaseModelFactory, SQLAlchemyBaseModelFactory


class PaymentFactory(SQLAlchemyBaseModelFactory[Payment]): ...


class PaymentResponseFactory(BaseModelFactory[PaymentResponseSchema]): ...
