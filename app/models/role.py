from sqlalchemy import Column, String, Integer, DateTime, Text
from sqlalchemy.orm import relationship
from app.db.base import BaseModel
from datetime import datetime

class Role(BaseModel):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    display_name = Column(String, nullable=False)
    access_permission = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    # Relationship with User
    users = relationship("User", back_populates="role") 