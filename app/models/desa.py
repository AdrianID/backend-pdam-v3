from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import BaseModel

class Desa(BaseModel):
    __tablename__ = "desa"

    kecamatan_id = Column(Integer, ForeignKey("kecamatan.id"), nullable=False)
    nama_desa = Column(String, nullable=False)

    # Relationships
    kecamatan = relationship("Kecamatan", back_populates="desa")
    area = relationship("Area", back_populates="desa")
    area_distrik = relationship("AreaDistrik", back_populates="desa")
    pelanggan = relationship("Pelanggan", back_populates="desa")
    spks = relationship("SPKS", back_populates="desa")
    gelombang_spks = relationship("GelombangSPKS", back_populates="desa") 