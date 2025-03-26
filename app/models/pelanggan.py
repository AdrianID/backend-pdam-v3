from sqlalchemy import Column, String, Integer, ForeignKey, Numeric, JSON, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from app.db.base import BaseModel
from app.models.kecamatan import Kecamatan
from enum import Enum

class StatusPelanggan(str, Enum):
    pending = "pending"
    verified = "verified"
    billing = "billing"
    paid = "paid"
    installation = "installation"
    active = "active"
    inactive = "inactive"
    terminated = "terminated"

    def __str__(self):
        return self.value 

class Pelanggan(BaseModel):
    __tablename__ = "pelanggan"

    kecamatan_id = Column(Integer, ForeignKey("kecamatan.id"), nullable=False)
    desa_id = Column(Integer, ForeignKey("desa.id"), nullable=False)
    kategori_id = Column(Integer, ForeignKey("kategori.id"), nullable=False)
    area_distrik_id = Column(Integer, ForeignKey("area_distrik.id"), nullable=False)
    sub_area_distrik_id = Column(Integer, ForeignKey("sub_area_distrik.id"), nullable=False)
    
    jenis_pelanggan = Column(String, nullable=False)
    nomor_pelanggan = Column(String, unique=True, nullable=False)
    nomor_meteran = Column(String, unique=True, nullable=False)
    nomor_kk = Column(String, unique=True, nullable=False)
    nomor_sertifikat = Column(String, nullable=True)
    nomor_telp = Column(String, nullable=False)
    nama_pelanggan = Column(String, nullable=False)
    nik = Column(String, unique=True, nullable=False)
    alamat = Column(String, nullable=False)
    rt = Column(String, nullable=False)
    rw = Column(String, nullable=False)
    nomor_rumah = Column(String, nullable=False)
    gang = Column(String, nullable=True)
    blok = Column(String, nullable=True)
    luas_bangunan = Column(Numeric(10, 2), nullable=True)
    jenis_hunian = Column(String, nullable=False)
    kebutuhan_air_awal = Column(Integer, nullable=False)
    kran_diminta = Column(Integer, nullable=False)
    kwh_pln = Column(String, nullable=True)
    status_kepemilikan = Column(String, nullable=False)
    file_sertifikat = Column(String, nullable=True)
    file_ktp = Column(String, nullable=True)
    file_kk = Column(String, nullable=True)
    pekerjaan = Column(String, nullable=True)
    latitude = Column(Numeric(10, 8), nullable=True)
    longitude = Column(Numeric(11, 8), nullable=True)
    status = Column(SQLAlchemyEnum(StatusPelanggan), default='pending')
    data_geojson = Column(JSON, nullable=True)

    # Relationships with lazy loading
    kecamatan = relationship("Kecamatan", back_populates="pelanggan")
    desa = relationship("Desa", back_populates="pelanggan")
    kategori = relationship("Kategori", back_populates="pelanggan")
    area_distrik = relationship("AreaDistrik", back_populates="pelanggan")
    sub_area_distrik = relationship("SubAreaDistrik", back_populates="pelanggan")
    users = relationship("User", back_populates="pelanggan")
    penggunaan_air = relationship("PenggunaanAir", back_populates="pelanggan")
    spks = relationship("SPKS", back_populates="pelanggan") 