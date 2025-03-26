from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SubAreaDistrikBase(BaseModel):
    area_distrik_id: int
    nama: str

class SubAreaDistrikCreate(SubAreaDistrikBase):
    pass

class SubAreaDistrikUpdate(BaseModel):
    nama: Optional[str] = None

class SubAreaDistrik(SubAreaDistrikBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 