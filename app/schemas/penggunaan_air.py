from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PenggunaanAirBase(BaseModel):
    pelanggan_id: int
    periode: str
    meter_awal: int
    meter_akhir: int
    total_penggunaan: int
    status: str
    keterangan: Optional[str] = None

class PenggunaanAirCreate(PenggunaanAirBase):
    pass

class PenggunaanAirUpdate(BaseModel):
    meter_akhir: Optional[int] = None
    total_penggunaan: Optional[int] = None
    status: Optional[str] = None
    keterangan: Optional[str] = None

class PenggunaanAir(PenggunaanAirBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 