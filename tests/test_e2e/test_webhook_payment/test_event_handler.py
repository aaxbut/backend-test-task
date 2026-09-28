from uuid import UUID

import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy import select

from app.models import Payment, Subscription


async def test_webhook_payment_success(
    client: AsyncClient,
    webhook_payment_url: str,
    test_user_id: UUID,
) -> None:
    headers = {
        'Content-Type': 'application/json',
        'bank-signature': 'test',
    }

    payment = {
        'payment_id': 'abc-123',
        'user_id': f'{test_user_id}',
        'amount': 4900,
        'status': 'CONFIRMED',
    }
    resp = await client.post(webhook_payment_url, headers=headers, json=payment)

    assert resp.status_code == status.HTTP_200_OK


async def test_webhook_payment_idempotency(
    client: AsyncClient,
    webhook_payment_url: str,
    db_session,
    test_user_id: UUID,
) -> None:
    headers = {
        'Content-Type': 'application/json',
        'bank-signature': 'test',
    }

    payment = {
        'payment_id': 'abc-123',
        'user_id': f'{test_user_id}',
        'amount': 4900,
        'status': 'CONFIRMED',
    }

    first_resp = await client.post(webhook_payment_url, headers=headers, json=payment)
    second_resp = await client.post(webhook_payment_url, headers=headers, json=payment)

    assert first_resp.status_code == status.HTTP_200_OK
    assert second_resp.status_code == status.HTTP_200_OK

    query = select(Payment).where(Payment.payment_id == 'abc-123')
    result = await db_session.execute(query)
    payments = result.scalars().all()
    assert len(payments) == 1


async def test_webhook_payment_with_non_confirmed_status(
    client: AsyncClient,
    webhook_payment_url: str,
    db_session,
    test_user_id: UUID,
) -> None:
    headers = {
        'Content-Type': 'application/json',
        'bank-signature': 'test',
    }

    payment = {
        'payment_id': 'ghi-789',
        'user_id': f'{test_user_id}',
        'amount': 4900,
        'status': 'FAILED',
    }

    with pytest.raises(ValueError, match='Payment status is not CONFIRMED: FAILED'):
        await client.post(webhook_payment_url, headers=headers, json=payment)

    query = select(Payment).where(Payment.payment_id == 'ghi-789')
    result = await db_session.execute(query)
    payments = result.scalars().all()
    assert len(payments) == 0

    query = select(Subscription).where(Subscription.user_id == test_user_id)
    result = await db_session.execute(query)
    subscription = result.scalar_one_or_none()
    assert subscription is None
