import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from http.client import responses
from fastapi import APIRouter, Request, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from loguru import logger

from .models import Email, EmailConfig

router = APIRouter(prefix="/messaging")


@router.post('/email')
async def send_email(request: Request, email: Email) -> JSONResponse:
    try:
        _send_email(email.recipients, email.subject, email.body, request.app.state.email_config)
        return JSONResponse(status_code=201, content=jsonable_encoder(email))
    except Exception as e:
        logger.error(f"Exception sending email. Error detail: {e}")
        raise HTTPException(status_code=500, detail=responses[500])


def _send_email(recipients: list[str], subject: str, body: str, email_config: EmailConfig) -> None:
    sender = email_config.EMAIL_SENDER
    password = email_config.EMAIL_PASSWORD
    smtp_host = email_config.SMTP_HOST
    smtp_port = email_config.SMTP_PORT

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    html_body = MIMEText(body, 'html')
    msg.attach(html_body)

    with open("./resources/FERNEC.png", "rb") as img_file:
        img = MIMEImage(img_file.read())
        img.add_header("Content-ID", "<logo>")
        msg.attach(img)

    with smtplib.SMTP_SSL(smtp_host, smtp_port) as smtp_server:
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, msg.as_string())
    logger.success("Message sent!")
