from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.role import Role
from app.schemas.role import RoleCreate, RoleUpdate

def get_role(db: Session, role_id: int) -> Optional[Role]:
    return db.query(Role).filter(Role.id == role_id, Role.deleted_at.is_(None)).first()

def get_role_by_name(db: Session, name: str) -> Optional[Role]:
    return db.query(Role).filter(Role.name == name, Role.deleted_at.is_(None)).first()

def get_roles(
    db: Session, 
    skip: int = 0, 
    limit: int = 100
) -> List[Role]:
    return db.query(Role)\
        .filter(Role.deleted_at.is_(None))\
        .offset(skip)\
        .limit(limit)\
        .all()

def create_role(db: Session, role: RoleCreate) -> Role:
    db_role = Role(**role.dict())
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

def update_role(db: Session, role_id: int, role: RoleUpdate) -> Optional[Role]:
    db_role = get_role(db, role_id)
    if db_role:
        for key, value in role.dict(exclude_unset=True).items():
            setattr(db_role, key, value)
        db.commit()
        db.refresh(db_role)
    return db_role 