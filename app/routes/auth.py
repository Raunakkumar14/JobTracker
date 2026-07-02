import random
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth import create_access_token
from app.core.email import send_otp_email,_set_otp,_generate_otp
from app.core.security import hash_password, verify_password
from app.database.dependencies import get_db
from app.models.user import User
from app.schema.user import (
    EmailOtpRequest,
    ResetPasswordRequest,
    UserCreate,
    UserLogin,
    VerifyEmailRequest,
)

router = APIRouter(tags=["Authentication"], prefix="/auth")

OTP_EXPIRY_MINUTES = 10

@router.post("/register")
def register(user: UserCreate,db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    new_user = User(
        email=user.email,
        password=hash_password(user.password),
        is_verified=False
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    _set_otp(
    new_user,
    "verification_code",
    "verification_code_expires_at",
    "email verification"
)

    db.commit()
    return {
    "message": "User registered successfully. Please check your email for the verification OTP."
}

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not db_user.is_verified:
        raise HTTPException(status_code=400, detail="Email not verified")

    token = create_access_token({"sub": db_user.email})

    return {
        "access_token": token,
        "token_type": "bearer",
    }


# @router.post("/send-verification-otp")
# def send_verification_otp(request: EmailOtpRequest, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.email == request.email).first()

#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     if user.is_verified:
#         return {"message": "Email already verified"}

#     _set_otp(user, "verification_code", "verification_code_expires_at", "email verification")
#     db.commit()

#     return {"message": "Verification OTP sent successfully"}


@router.post("/verify-email")
def verify_email(request: VerifyEmailRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.is_verified:
        return {"message": "Email already verified"}

    if not user.verification_code or not user.verification_code_expires_at:
        raise HTTPException(status_code=400, detail="No verification OTP found")

    if datetime.utcnow() > user.verification_code_expires_at:
        raise HTTPException(status_code=400, detail="Verification OTP expired")

    if request.otp != user.verification_code:
        raise HTTPException(status_code=400, detail="Invalid verification OTP")

    user.is_verified = True
    user.verification_code = None
    user.verification_code_expires_at = None
    db.commit()

    return {"message": "Email verified successfully"}


@router.post("/forgot-password")
def forgot_password(request: EmailOtpRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    _set_otp(user, "reset_code", "reset_code_expires_at", "password reset")
    db.commit()

    return {"message": "Password reset OTP sent successfully"}


@router.post("/reset-password")
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user.reset_code or not user.reset_code_expires_at:
        raise HTTPException(status_code=400, detail="No reset OTP found")

    if datetime.utcnow() > user.reset_code_expires_at:
        raise HTTPException(status_code=400, detail="Reset OTP expired")

    if request.otp != user.reset_code:
        raise HTTPException(status_code=400, detail="Invalid reset OTP")

    user.password = hash_password(request.new_password)
    user.reset_code = None
    user.reset_code_expires_at = None
    db.commit()

    return {"message": "Password reset successfully"}