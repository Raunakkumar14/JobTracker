from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import SessionLocal
from app.models.user import User
from app.schema.user import UserCreate, UserLogin,UserOut
from app.core.security import hash_password, verify_password
from app.core.auth import create_access_token
from app.database.dependencies import get_db
from app.core.dependencies import get_current_user

router = APIRouter(tags=["user"],prefix="/user")
@router.get("/{user_id}",response_model=UserOut)

def get_user(user_id: int, 
             db: Session = Depends(get_db),
             current_user=Depends(get_current_user)):
    
    user=db.query(User).filter(User.id==user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
