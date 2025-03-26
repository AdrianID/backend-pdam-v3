from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.base import BaseModel

class GelombangSPKS(BaseModel):
    __tablename__ = "gelombang_spks"

    kecamatan_id = Column(Integer, ForeignKey("kecamatan.id"), nullable=False)
    desa_id = Column(Integer, ForeignKey("desa.id"), nullable=False)
    area_distrik_id = Column(Integer, ForeignKey("area_distrik.id"), nullable=False)
    sub_area_distrik_id = Column(Integer, ForeignKey("sub_area_distrik.id"), nullable=False)
    spks_id = Column(Integer, ForeignKey("spks.id"), nullable=False)
    
    nomor_spks_global = Column(String, nullable=False)
    nomor_spks_terakhir = Column(String, nullable=False)
    nomor_spks_terbaru = Column(String, nullable=False)
    alamat = Column(Text, nullable=False)
    unit = Column(String, nullable=False)
    kuota_gelombang = Column(Integer, nullable=False)
    keterangan = Column(Text, nullable=True)

    # Relationships
    kecamatan = relationship("Kecamatan", back_populates="gelombang_spks")
    desa = relationship("Desa", back_populates="gelombang_spks")
    area_distrik = relationship("AreaDistrik", back_populates="gelombang_spks")
    sub_area_distrik = relationship("SubAreaDistrik", back_populates="gelombang_spks")
    spks = relationship("SPKS", back_populates="gelombang_spks") 