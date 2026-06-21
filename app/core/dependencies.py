from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import os
from dotenv import load_dotenv
from app.database.dependencies import get_db
from sqlalchemy.orm import Session
from app.models.user import User

# Load environment variables
load_dotenv()

# Security scheme (this gives Swagger 🔒 button)
security = HTTPBearer()

# Environment variables
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")


# Dependency to get current user from JWT
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials  # removes "Bearer "

    try:
        # Decode token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Extract user info
        user_email = payload.get("sub")

        if not user_email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        user=db.query(User).filter(User.email==user_email).first()

        return user

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )