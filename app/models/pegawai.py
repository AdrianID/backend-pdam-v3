from sqlalchemy import Column, String, Integer, ForeignKey, Date, Text
from sqlalchemy.orm import relationship
from app.db.base import BaseModel

class Pegawai(BaseModel):
    __tablename__ = "pegawai"

    jabatan_id = Column(Integer, ForeignKey("jabatan.id"), nullable=False)
    tempat_id = Column(Integer, ForeignKey("tempat.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    nik = Column(String, unique=True, nullable=False)
    nip = Column(String, unique=True, nullable=False)
    jabatan = Column(String, nullable=False)
    periode_masuk = Column(Date, nullable=False)
    tanggal_lahir = Column(Date, nullable=False)
    alamat = Column(Text, nullable=False)
    nomor_tlp = Column(String, nullable=False)
    nomor_bpjs = Column(String, nullable=True)
    nomor_npwp = Column(String, nullable=True)

    # Relationships
    jabatan_rel = relationship("Jabatan", back_populates="pegawai")
    tempat = relationship("Tempat", back_populates="pegawai")
    user = relationship("User", back_populates="pegawai")
    tanggungan = relationship("Tanggungan", back_populates="pegawai")
    spks = relationship("SPKS", back_populates="pegawai") 