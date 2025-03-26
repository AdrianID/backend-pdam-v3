from sqlalchemy import Boolean, Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.base import BaseModel
from datetime import datetime

class User(BaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    pelanggan_id = Column(Integer, ForeignKey("pelanggan.id"), nullable=True)
    username = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)  # Ini akan menyimpan hashed password
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    # Relationships
    role = relationship("Role", back_populates="users")
    pelanggan = relationship("Pelanggan", back_populates="users", uselist=False)
    pegawai = relationship("Pegawai", back_populates="user", uselist=False) 