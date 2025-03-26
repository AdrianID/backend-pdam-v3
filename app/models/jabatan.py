from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.db.base import BaseModel

class Jabatan(BaseModel):
    __tablename__ = "jabatan"

    kelas_jabatan = Column(String, nullable=False)
    nama_jabatan = Column(String, nullable=False)

    # Relationships
    pegawai = relationship("Pegawai", back_populates="jabatan_rel")
    iku = relationship("IKU", back_populates="jabatan") 