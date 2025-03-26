from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RoleBase(BaseModel):
    name: str
    display_name: str
    access_permission: str
    description: Optional[str] = None

class RoleCreate(RoleBase):
    pass

class RoleUpdate(BaseModel):
    name: Optional[str] = None
    display_name: Optional[str] = None
    access_permission: Optional[str] = None
    description: Optional[str] = None

class Role(RoleBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 