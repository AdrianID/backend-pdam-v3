from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models.sub_area_distrik import SubAreaDistrik
from app.schemas.sub_area_distrik import SubAreaDistrikCreate, SubAreaDistrikUpdate

def get_sub_area_distrik(db: Session, sub_area_id: int) -> Optional[SubAreaDistrik]:
    return db.query(SubAreaDistrik)\
        .filter(SubAreaDistrik.id == sub_area_id)\
        .filter(SubAreaDistrik.deleted_at.is_(None))\
        .first()

def get_sub_areas_by_area_distrik(
    db: Session,
    area_distrik_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[SubAreaDistrik]:
    return db.query(SubAreaDistrik)\
        .filter(
            SubAreaDistrik.area_distrik_id == area_distrik_id,
            SubAreaDistrik.deleted_at.is_(None)
        )\
        .offset(skip)\
        .limit(limit)\
        .all()

def get_sub_areas(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    filters: Dict[str, Any] = None
) -> List[SubAreaDistrik]:
    query = db.query(SubAreaDistrik).filter(SubAreaDistrik.deleted_at.is_(None))
    
    if filters:
        if filters.get("area_distrik_id"):
            query = query.filter(SubAreaDistrik.area_distrik_id == filters["area_distrik_id"])
        if filters.get("search"):
            search = f"%{filters['search']}%"
            query = query.filter(SubAreaDistrik.nama.ilike(search))
    
    return query.offset(skip).limit(limit).all()

def create_sub_area_distrik(db: Session, sub_area: SubAreaDistrikCreate) -> SubAreaDistrik:
    db_sub_area = SubAreaDistrik(**sub_area.dict())
    db.add(db_sub_area)
    db.commit()
    db.refresh(db_sub_area)
    return db_sub_area

def update_sub_area_distrik(
    db: Session,
    db_sub_area: SubAreaDistrik,
    sub_area: SubAreaDistrikUpdate
) -> SubAreaDistrik:
    for field, value in sub_area.dict(exclude_unset=True).items():
        setattr(db_sub_area, field, value)
    
    db.add(db_sub_area)
    db.commit()
    db.refresh(db_sub_area)
    return db_sub_area

def delete_sub_area_distrik(db: Session, sub_area_id: int) -> Optional[SubAreaDistrik]:
    sub_area = get_sub_area_distrik(db, sub_area_id)
    if sub_area:
        from datetime import datetime
        sub_area.deleted_at = datetime.utcnow()
        db.add(sub_area)
        db.commit()
        db.refresh(sub_area)
    return sub_area 