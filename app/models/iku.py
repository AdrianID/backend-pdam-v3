from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.base import BaseModel

class IKU(BaseModel):
    __tablename__ = "iku"

    jabatan_id = Column(Integer, ForeignKey("jabatan.id"), nullable=False)
    nama_iku = Column(String, nullable=False)
    keterangan = Column(Text, nullable=True)

    # Relationships
    jabatan = relationship("Jabatan", back_populates="iku") 