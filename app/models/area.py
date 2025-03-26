from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import BaseModel

class Area(BaseModel):
    __tablename__ = "area"

    kecamatan_id = Column(Integer, ForeignKey("kecamatan.id"), nullable=False)
    desa_id = Column(Integer, ForeignKey("desa.id"), nullable=False)
    klasifikasi_area = Column(String, nullable=False)
    nama = Column(String, nullable=False)

    # Relationships
    kecamatan = relationship("Kecamatan", back_populates="area")
    desa = relationship("Desa", back_populates="area") 