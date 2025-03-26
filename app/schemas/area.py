from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AreaBase(BaseModel):
    kecamatan_id: int
    desa_id: int
    klasifikasi_area: str
    nama: str

class AreaCreate(AreaBase):
    pass

class AreaUpdate(BaseModel):
    klasifikasi_area: Optional[str] = None
    nama: Optional[str] = None

class Area(AreaBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 