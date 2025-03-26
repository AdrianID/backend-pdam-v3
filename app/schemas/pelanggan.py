from pydantic import BaseModel, EmailStr, constr
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from app.models.pelanggan import StatusPelanggan

class PelangganBase(BaseModel):
    kecamatan_id: int
    desa_id: int
    kategori_id: int
    area_distrik_id: int
    sub_area_distrik_id: int
    jenis_pelanggan: str
    nomor_pelanggan: str
    nomor_meteran: str
    nomor_kk: str
    nomor_sertifikat: Optional[str] = None
    nomor_telp: str
    nama_pelanggan: str
    nik: str
    alamat: str
    rt: str
    rw: str
    nomor_rumah: str
    gang: Optional[str] = None
    blok: Optional[str] = None
    luas_bangunan: Optional[Decimal] = None
    jenis_hunian: str
    kebutuhan_air_awal: int
    kran_diminta: int
    kwh_pln: Optional[str] = None
    status_kepemilikan: str
    pekerjaan: Optional[str] = None
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None
    status: StatusPelanggan

class PelangganCreate(PelangganBase):
    pass

class PelangganUpdate(BaseModel):
    kecamatan_id: Optional[int] = None
    desa_id: Optional[int] = None
    kategori_id: Optional[int] = None
    area_distrik_id: Optional[int] = None
    sub_area_distrik_id: Optional[int] = None
    jenis_pelanggan: Optional[str] = None
    nomor_telp: Optional[str] = None
    alamat: Optional[str] = None
    status: Optional[StatusPelanggan] = None

class Pelanggan(PelangganBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 