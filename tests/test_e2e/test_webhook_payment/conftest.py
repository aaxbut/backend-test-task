import pytest
from fastapi import FastAPI


@pytest.fixture(scope='module')
def webhook_payment_url(app: FastAPI) -> str:
    return app.url_path_for('webhook:payment')
