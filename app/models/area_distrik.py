from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import BaseModel

class AreaDistrik(BaseModel):
    __tablename__ = "area_distrik"

    kecamatan_id = Column(Integer, ForeignKey("kecamatan.id"), nullable=False)
    desa_id = Column(Integer, ForeignKey("desa.id"), nullable=False)
    nama = Column(String, nullable=False)

    # Relationships
    kecamatan = relationship("Kecamatan", back_populates="area_distrik")
    desa = relationship("Desa", back_populates="area_distrik")
    sub_area_distrik = relationship("SubAreaDistrik", back_populates="area_distrik")
    pelanggan = relationship("Pelanggan", back_populates="area_distrik")
    spks = relationship("SPKS", back_populates="area_distrik")
    gelombang_spks = relationship("GelombangSPKS", back_populates="area_distrik") 