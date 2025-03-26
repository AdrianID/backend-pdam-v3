from typing import Any, List
from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.crud import user as user_crud
from app.models.user import User
from app.schemas.user import User as UserSchema, UserCreate, UserUpdate
from app.db.session import get_db
from app.utils.dependencies import get_current_active_user, get_current_active_superuser
from app.utils.response_handler import create_pagination_response, create_response

router = APIRouter()

@router.get("/users/", response_model=List[UserSchema])
def read_users(
    db: Session = Depends(get_db),
    page: int = 1,
    per_page: int = 10,
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    """
    Retrieve users with pagination
    """
    skip = (page - 1) * per_page
    users = user_crud.get_users(db, skip=skip, limit=per_page)
    total = user_crud.get_users_count(db)
    
    return create_pagination_response(
        data=[{
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "name": user.name,
            "role": user.role.name,
            "status": user.status
        } for user in users],
        total=total,
        page=page,
        per_page=per_page,
        message="Users retrieved successfully"
    )

@router.post("/register")
def register_user(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate,
) -> Any:
    """
    Register new user with default role_id=4 (public endpoint)
    """
    # Force role_id to 4 for public registration
    user_in.role_id = 4
    
    # Check if email exists
    user = user_crud.get_user_by_email(db, email=user_in.email)
    if user:
        return create_response(
            status=False,
            message="Email already registered",
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    # Check if username exists
    user = user_crud.get_user_by_username(db, username=user_in.username)
    if user:
        return create_response(
            status=False,
            message="Username already taken",
            status_code=status.HTTP_400_BAD_REQUEST
        )

    try:
        user = user_crud.create_user(db, user_in)
        return create_response(
            status=True,
            message="Registration successful",
            data={
                "id": user.id,
                "username": user.username,
                "name": user.name,
                "email": user.email,
                "role": {
                    "id": user.role.id,
                    "name": user.role.name,
                    "display_name": user.role.display_name
                },
                "status": user.status,
                "created_at": user.created_at,
                "updated_at": user.updated_at
            },
            status_code=status.HTTP_201_CREATED
        )
    except Exception as e:
        return create_response(
            status=False,
            message=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@router.post("/users/")
def create_user(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate,
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    """
    Create new user by admin (protected endpoint)
    """
    # Prevent using role_id=4 in admin creation
    if user_in.role_id == 4:
        return create_response(
            status=False,
            message="Please use /register endpoint for regular user registration",
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    # Check if email exists
    user = user_crud.get_user_by_email(db, email=user_in.email)
    if user:
        return create_response(
            status=False,
            message="Email already registered",
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    # Check if username exists
    user = user_crud.get_user_by_username(db, username=user_in.username)
    if user:
        return create_response(
            status=False,
            message="Username already taken",
            status_code=status.HTTP_400_BAD_REQUEST
        )

    try:
        user = user_crud.create_user(db, user_in)
        return create_response(
            status=True,
            message="User created successfully",
            data={
                "id": user.id,
                "username": user.username,
                "name": user.name,
                "email": user.email,
                "role": {
                    "id": user.role.id,
                    "name": user.role.name,
                    "display_name": user.role.display_name
                },
                "status": user.status,
                "created_at": user.created_at,
                "updated_at": user.updated_at
            },
            status_code=status.HTTP_201_CREATED
        )
    except Exception as e:
        return create_response(
            status=False,
            message=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@router.put("/users/me", response_model=UserSchema)
def update_user_me(
    *,
    db: Session = Depends(get_db),
    user_in: UserUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update own user.
    """
    user = user_crud.update_user(db, db_user=current_user, user_in=user_in)
    return user

@router.get("/users/me", response_model=UserSchema)
def read_user_me(
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user

@router.get("/users/{user_id}", response_model=UserSchema)
def read_user_by_id(
    user_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    user = user_crud.get_user_by_id(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    if user == current_user:
        return user
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user doesn't have enough privileges",
        )
    return user

@router.put("/users/{user_id}", response_model=UserSchema)
def update_user(
    *,
    db: Session = Depends(get_db),
    user_id: int,
    user_in: UserUpdate,
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    """
    Update a user. Only superuser can access this endpoint.
    """
    user = user_crud.get_user_by_id(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    user = user_crud.update_user(db, db_user=user, user_in=user_in)
    return user

@router.delete("/users/{user_id}", response_model=UserSchema)
def delete_user(
    *,
    db: Session = Depends(get_db),
    user_id: int,
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    """
    Delete a user. Only superuser can access this endpoint.
    """
    user = user_crud.delete_user(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user 