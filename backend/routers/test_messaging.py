import json
import pytest
from unittest import mock
from fastapi import HTTPException
from http.client import responses

from .messaging import send_email, _send_email
from .models import Email, EmailConfig


class MockRequest:
    class MockApp:
        class MockState:
            email_config = "mock_config"
        state = MockState()
    app = MockApp()


def get_email() -> Email:
    return Email(recipients=["john.doe@fernec.com"], subject="fake subject", body="fake body")


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


@pytest.fixture
def mock_email_config():
    return EmailConfig(
        EMAIL_SENDER="fernec.fiuba@gmail.com",
        EMAIL_PASSWORD="fake-password",
        SMTP_HOST="smtp.fake.com",
        SMTP_PORT=465
    )


@pytest.mark.asyncio
async def test_send_email_success(mock_email_config):
    recipients = ["john.doe@fernec.com"]
    subject = "fake subject"
    body = "fake body"

    with mock.patch('backend.routers.messaging.smtplib.SMTP_SSL') as mock_smtp:
        # Mock SMTP configuration
        mock_smtp_instance = mock_smtp.return_value.__enter__.return_value
        mock_smtp_instance.sendmail.return_value = {}

        _send_email(recipients, subject, body, mock_email_config)
        _send_email_args = mock_smtp_instance.sendmail.call_args[0]

        assert _send_email_args[0] == mock_email_config.EMAIL_SENDER
        assert _send_email_args[1] == recipients
        assert "Subject: fake subject" in _send_email_args[2]
        assert "From: fernec.fiuba@gmail.com" in _send_email_args[2]
        assert "To: john.doe@fernec.com" in _send_email_args[2]

    mock_smtp.assert_called_once_with(mock_email_config.SMTP_HOST, mock_email_config.SMTP_PORT)
    mock_smtp_instance.login.assert_called_once_with(mock_email_config.EMAIL_SENDER,
                                                     mock_email_config.EMAIL_PASSWORD)
