from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SPKSBase(BaseModel):
    kecamatan_id: int
    desa_id: int
    kategori_id: int
    area_distrik_id: int
    sub_area_distrik_id: int
    pelanggan_id: int
    pegawai_id: int
    nama: str
    alamat: str
    nomor_telp: str
    nomor_spks: str
    petugas_sr: str
    kuota: int
    keterangan: Optional[str] = None

class SPKSCreate(SPKSBase):
    pass

class SPKSUpdate(BaseModel):
    nama: Optional[str] = None
    alamat: Optional[str] = None
    nomor_telp: Optional[str] = None
    petugas_sr: Optional[str] = None
    kuota: Optional[int] = None
    keterangan: Optional[str] = None

class SPKS(SPKSBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 