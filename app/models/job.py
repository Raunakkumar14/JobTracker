from datetime import date, datetime

from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.db import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    description = Column(String, nullable=True)
    location = Column(String, nullable=True)
    deadline = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="jobs")