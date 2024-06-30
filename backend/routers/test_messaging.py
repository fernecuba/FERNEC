import json
import pytest
from unittest import mock
from fastapi import HTTPException
from http.client import responses

from .messaging import send_email
from .models import Email


class MockRequest:
    class MockApp:
        class MockState:
            email_config = "mock_config"
        state = MockState()
    app = MockApp()


def get_email() -> Email:
    return Email(recipients=["test@example.com"], subject="Test Subject", body="Test Body")


@pytest.mark.asyncio
async def test_send_email_success():
    email = get_email()

    with mock.patch('backend.routers.messaging._send_email') as mock_send_email:
        mock_send_email.return_value = None

        response = await send_email(MockRequest(), email)

        mock_send_email.assert_called_once_with(
            email.recipients,
            email.subject,
            email.body,
            MockRequest().app.state.email_config
        )

        print(f"response is {response.__dict__}")
        assert response.status_code == 201
        response_body = json.loads(response.body)
        assert response_body["recipients"] == email.recipients
        assert response_body["subject"] == email.subject
        assert response_body["body"] == email.body


@pytest.mark.asyncio
async def test_send_email_fails():
    email = get_email()

    # Caso de excepción
    with mock.patch('backend.routers.messaging._send_email') as mock_send_email:
        mock_send_email.side_effect = Exception("Fake exception")

        with pytest.raises(HTTPException) as exception:
            await send_email(MockRequest(), email)

        assert exception.value.status_code == 500
        assert exception.value.detail == responses[500]
