from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import SessionLocal
from app.models.user import User
from app.schema.user import UserCreate, UserLogin
from app.core.security import hash_password, verify_password
from app.core.auth import create_access_token
from app.database.dependencies import get_db

router = APIRouter(tags=["Authentication"],prefix="/auth")


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")
     
    new_user = User(
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"sub": db_user.email})

    return {
        "access_token": token,
        "token_type": "bearer"
    }