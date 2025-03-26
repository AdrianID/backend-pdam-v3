from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.base import BaseModel

class SPKS(BaseModel):
    __tablename__ = "spks"

    kecamatan_id = Column(Integer, ForeignKey("kecamatan.id"), nullable=False)
    desa_id = Column(Integer, ForeignKey("desa.id"), nullable=False)
    kategori_id = Column(Integer, ForeignKey("kategori.id"), nullable=False)
    area_distrik_id = Column(Integer, ForeignKey("area_distrik.id"), nullable=False)
    sub_area_distrik_id = Column(Integer, ForeignKey("sub_area_distrik.id"), nullable=False)
    pelanggan_id = Column(Integer, ForeignKey("pelanggan.id"), nullable=False)
    pegawai_id = Column(Integer, ForeignKey("pegawai.id"), nullable=False)
    
    nama = Column(String, nullable=False)
    alamat = Column(Text, nullable=False)
    nomor_telp = Column(String, nullable=False)
    nomor_spks = Column(String, nullable=False)
    petugas_sr = Column(String, nullable=False)
    kuota = Column(Integer, nullable=False)
    keterangan = Column(Text, nullable=True)

    # Relationships
    kecamatan = relationship("Kecamatan", back_populates="spks")
    desa = relationship("Desa", back_populates="spks")
    kategori = relationship("Kategori", back_populates="spks")
    area_distrik = relationship("AreaDistrik", back_populates="spks")
    sub_area_distrik = relationship("SubAreaDistrik", back_populates="spks")
    pelanggan = relationship("Pelanggan", back_populates="spks")
    pegawai = relationship("Pegawai", back_populates="spks")
    gelombang_spks = relationship("GelombangSPKS", back_populates="spks") 