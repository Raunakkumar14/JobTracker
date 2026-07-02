import os
import random
from datetime import datetime, timedelta
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv
from app.models.user import User

load_dotenv()  # Load environment variables from .env file

SMTP_HOST = os.getenv("SMTP_HOST") or os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_FROM = os.getenv("SMTP_FROM") or SMTP_USERNAME
OTP_EXPIRY_MINUTES = 10


def send_otp_email(to_email: str, otp: str, purpose: str) -> bool:
    if not SMTP_HOST or not SMTP_USERNAME or not SMTP_PASSWORD:
        return False

    subject = f"Your {purpose} OTP"
    body = f"Your OTP is {otp}. It will expire in 10 minutes."

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = SMTP_FROM
    message["To"] = to_email
    message.set_content(body)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(message)

    return True

def _generate_otp() -> str:
    return f"{random.randint(100000, 999999)}"


def _set_otp(user: User, code_field: str, expiry_field: str, purpose: str) -> str:
    otp = _generate_otp()
    setattr(user, code_field, otp)
    setattr(user, expiry_field, datetime.utcnow() + timedelta(minutes=OTP_EXPIRY_MINUTES))
    send_otp_email(user.email, otp, purpose)
    return otp
