from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship
from app.db.base import BaseModel

class Tempat(BaseModel):
    __tablename__ = "tempat"

    nama_tempat = Column(String, nullable=False)
    alamat = Column(Text, nullable=False)
    status = Column(String, nullable=False)

    # Relationships
    pegawai = relationship("Pegawai", back_populates="tempat") 