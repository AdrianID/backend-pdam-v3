from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models.pelanggan import Pelanggan
from app.schemas.pelanggan import PelangganCreate, PelangganUpdate

def get_pelanggan(db: Session, pelanggan_id: int) -> Optional[Pelanggan]:
    return db.query(Pelanggan)\
        .filter(Pelanggan.id == pelanggan_id)\
        .filter(Pelanggan.deleted_at.is_(None))\
        .first()

def get_pelanggan_by_nomor(db: Session, nomor_pelanggan: str) -> Optional[Pelanggan]:
    return db.query(Pelanggan)\
        .filter(Pelanggan.nomor_pelanggan == nomor_pelanggan)\
        .filter(Pelanggan.deleted_at.is_(None))\
        .first()

def get_pelanggan_list(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    filters: Dict[str, Any] = None
) -> List[Pelanggan]:
    query = db.query(Pelanggan).filter(Pelanggan.deleted_at.is_(None))
    
    if filters:
        if filters.get("kecamatan_id"):
            query = query.filter(Pelanggan.kecamatan_id == filters["kecamatan_id"])
        if filters.get("desa_id"):
            query = query.filter(Pelanggan.desa_id == filters["desa_id"])
        if filters.get("status"):
            query = query.filter(Pelanggan.status == filters["status"])
        if filters.get("search"):
            search = f"%{filters['search']}%"
            query = query.filter(
                (Pelanggan.nama_pelanggan.ilike(search)) |
                (Pelanggan.nomor_pelanggan.ilike(search)) |
                (Pelanggan.nik.ilike(search))
            )
    
    return query.offset(skip).limit(limit).all()

def create_pelanggan(db: Session, pelanggan: PelangganCreate) -> Pelanggan:
    db_pelanggan = Pelanggan(**pelanggan.dict())
    db.add(db_pelanggan)
    db.commit()
    db.refresh(db_pelanggan)
    return db_pelanggan

def update_pelanggan(
    db: Session,
    db_pelanggan: Pelanggan,
    pelanggan: PelangganUpdate
) -> Pelanggan:
    for field, value in pelanggan.dict(exclude_unset=True).items():
        setattr(db_pelanggan, field, value)
    
    db.add(db_pelanggan)
    db.commit()
    db.refresh(db_pelanggan)
    return db_pelanggan

def delete_pelanggan(db: Session, pelanggan_id: int) -> Optional[Pelanggan]:
    pelanggan = get_pelanggan(db, pelanggan_id)
    if pelanggan:
        from datetime import datetime
        pelanggan.deleted_at = datetime.utcnow()
        db.add(pelanggan)
        db.commit()
        db.refresh(pelanggan)
    return pelanggan 