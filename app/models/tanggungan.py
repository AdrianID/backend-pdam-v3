from sqlalchemy import Column, String, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.db.base import BaseModel

class Tanggungan(BaseModel):
    __tablename__ = "tanggungan"

    pegawai_id = Column(Integer, ForeignKey("pegawai.id"), nullable=False)
    tipe = Column(String, nullable=False)
    nama = Column(String, nullable=False)
    tanggal_lahir = Column(Date, nullable=False)
    pendidikan = Column(String, nullable=True)

    # Relationships
    pegawai = relationship("Pegawai", back_populates="tanggungan") 