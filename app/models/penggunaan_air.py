from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.base import BaseModel

class PenggunaanAir(BaseModel):
    __tablename__ = "penggunaan_air"

    pelanggan_id = Column(Integer, ForeignKey("pelanggan.id"), nullable=False)
    periode = Column(String, nullable=False)
    meter_awal = Column(Integer, nullable=False)
    meter_akhir = Column(Integer, nullable=False)
    total_penggunaan = Column(Integer, nullable=False)
    status = Column(String, nullable=False)
    keterangan = Column(Text, nullable=True)

    # Relationships
    pelanggan = relationship("Pelanggan", back_populates="penggunaan_air") 