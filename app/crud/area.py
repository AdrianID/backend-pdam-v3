from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models.area import Area
from app.schemas.area import AreaCreate, AreaUpdate

def get_area(db: Session, area_id: int) -> Optional[Area]:
    return db.query(Area)\
        .filter(Area.id == area_id)\
        .filter(Area.deleted_at.is_(None))\
        .first()

def get_areas(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    filters: Dict[str, Any] = None
) -> List[Area]:
    query = db.query(Area).filter(Area.deleted_at.is_(None))
    
    if filters:
        if filters.get("kecamatan_id"):
            query = query.filter(Area.kecamatan_id == filters["kecamatan_id"])
        if filters.get("desa_id"):
            query = query.filter(Area.desa_id == filters["desa_id"])
        if filters.get("klasifikasi_area"):
            query = query.filter(Area.klasifikasi_area == filters["klasifikasi_area"])
        if filters.get("search"):
            search = f"%{filters['search']}%"
            query = query.filter(Area.nama.ilike(search))
    
    return query.offset(skip).limit(limit).all()

def create_area(db: Session, area: AreaCreate) -> Area:
    db_area = Area(**area.dict())
    db.add(db_area)
    db.commit()
    db.refresh(db_area)
    return db_area

def update_area(
    db: Session,
    db_area: Area,
    area: AreaUpdate
) -> Area:
    for field, value in area.dict(exclude_unset=True).items():
        setattr(db_area, field, value)
    
    db.add(db_area)
    db.commit()
    db.refresh(db_area)
    return db_area

def delete_area(db: Session, area_id: int) -> Optional[Area]:
    area = get_area(db, area_id)
    if area:
        from datetime import datetime
        area.deleted_at = datetime.utcnow()
        db.add(area)
        db.commit()
        db.refresh(area)
    return area 