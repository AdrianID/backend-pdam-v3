from sqlalchemy import Column, String, Numeric
from sqlalchemy.orm import relationship
from app.db.base import BaseModel

class Kategori(BaseModel):
    __tablename__ = "kategori"

    nama_kategori = Column(String, nullable=False)
    tarif_penggunaan = Column(Numeric(10, 2), nullable=False)
    biaya_pasang = Column(Numeric(10, 2), nullable=False)
    denda = Column(Numeric(10, 2), nullable=False)

    # Relationships
    pelanggan = relationship("Pelanggan", back_populates="kategori")
    spks = relationship("SPKS", back_populates="kategori") 