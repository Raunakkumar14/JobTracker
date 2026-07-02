from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.database.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_verified = Column(Boolean, default=False, nullable=False)
    verification_code = Column(String, nullable=True)
    reset_code = Column(String, nullable=True)
    verification_code_expires_at = Column(DateTime, nullable=True)
    reset_code_expires_at = Column(DateTime, nullable=True)

    jobs = relationship("Job", back_populates="user")