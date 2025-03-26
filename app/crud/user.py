from typing import Any, Dict, Optional, Union, List
from sqlalchemy.orm import Session, joinedload
from app.models.user import User
from app.models.role import Role
from app.schemas.user import UserCreate, UserUpdate
from app.utils.authentication import get_password_hash

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User)\
        .options(joinedload(User.role))\
        .filter(
            User.email == email,
            User.deleted_at.is_(None)
        ).first()

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User)\
        .options(joinedload(User.role))\
        .filter(
            User.username == username,
            User.deleted_at.is_(None)
        ).first()

def get_user_by_id(db: Session, id: int) -> Optional[User]:
    return db.query(User)\
        .options(joinedload(User.role))\
        .filter(
            User.id == id,
            User.deleted_at.is_(None)
        ).first()

def get_users(
    db: Session, 
    skip: int = 0, 
    limit: int = 100
) -> List[User]:
    return db.query(User)\
        .options(joinedload(User.role))\
        .filter(User.deleted_at.is_(None))\
        .offset(skip)\
        .limit(limit)\
        .all()

def get_users_count(db: Session) -> int:
    return db.query(User)\
        .filter(User.deleted_at.is_(None))\
        .count()

def create_user(db: Session, user_in: UserCreate) -> User:
    try:
        db_user = User(
            username=user_in.username,
            name=user_in.name,
            email=user_in.email,
            password=get_password_hash(user_in.password),
            role_id=user_in.role_id,
            status=user_in.status
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        # Reload user with role relationship
        return get_user_by_id(db, db_user.id)
    except Exception as e:
        db.rollback()
        raise Exception(f"Error creating user: {str(e)}")

def update_user(
    db: Session, 
    db_user: User,
    user_in: Union[UserUpdate, Dict[str, Any]]
) -> User:
    if isinstance(user_in, dict):
        update_data = user_in
    else:
        update_data = user_in.dict(exclude_unset=True)
    
    if "password" in update_data:
        hashed_password = get_password_hash(update_data["password"])
        del update_data["password"]
        update_data["password"] = hashed_password
    
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Reload user with role relationship
    return get_user_by_id(db, db_user.id)

def delete_user(db: Session, user_id: int) -> Optional[User]:
    user = get_user_by_id(db, user_id)
    if user:
        # Soft delete
        from datetime import datetime
        user.deleted_at = datetime.utcnow()
        db.add(user)
        db.commit()
        db.refresh(user)
    return user

# Additional function to search users with filters
def search_users(
    db: Session,
    search: Optional[str] = None,
    role_id: Optional[int] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
) -> List[User]:
    query = db.query(User)\
        .options(joinedload(User.role))\
        .filter(User.deleted_at.is_(None))
    
    if search:
        query = query.filter(
            (User.username.ilike(f"%{search}%")) |
            (User.email.ilike(f"%{search}%")) |
            (User.name.ilike(f"%{search}%"))
        )
    
    if role_id:
        query = query.filter(User.role_id == role_id)
    
    if status:
        query = query.filter(User.status == status)
    
    return query.offset(skip).limit(limit).all()

def get_search_users_count(
    db: Session,
    search: Optional[str] = None,
    role_id: Optional[int] = None,
    status: Optional[str] = None
) -> int:
    query = db.query(User)\
        .filter(User.deleted_at.is_(None))
    
    if search:
        query = query.filter(
            (User.username.ilike(f"%{search}%")) |
            (User.email.ilike(f"%{search}%")) |
            (User.name.ilike(f"%{search}%"))
        )
    
    if role_id:
        query = query.filter(User.role_id == role_id)
    
    if status:
        query = query.filter(User.status == status)
    
    return query.count() 