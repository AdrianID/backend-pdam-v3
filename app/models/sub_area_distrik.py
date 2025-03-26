from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import BaseModel

class SubAreaDistrik(BaseModel):
    __tablename__ = "sub_area_distrik"

    area_distrik_id = Column(Integer, ForeignKey("area_distrik.id"), nullable=False)
    nama = Column(String, nullable=False)

    # Relationships
    area_distrik = relationship("AreaDistrik", back_populates="sub_area_distrik")
    pelanggan = relationship("Pelanggan", back_populates="sub_area_distrik")
    spks = relationship("SPKS", back_populates="sub_area_distrik")
    gelombang_spks = relationship("GelombangSPKS", back_populates="sub_area_distrik") 