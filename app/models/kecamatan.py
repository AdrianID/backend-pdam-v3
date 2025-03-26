from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from app.db.base import BaseModel


class Kecamatan(BaseModel):
    __tablename__ = "kecamatan"

    nama_kecamatan = Column(String, nullable=False)
    
    # Relationships menggunakan string untuk menghindari circular import
    desa = relationship("Desa", back_populates="kecamatan", lazy="dynamic")
    area = relationship("Area", back_populates="kecamatan", lazy="dynamic")
    area_distrik = relationship("AreaDistrik", back_populates="kecamatan", lazy="dynamic")
    pelanggan = relationship("Pelanggan", back_populates="kecamatan", lazy="dynamic")
    spks = relationship("SPKS", back_populates="kecamatan", lazy="dynamic")
    gelombang_spks = relationship("GelombangSPKS", back_populates="kecamatan", lazy="dynamic") 