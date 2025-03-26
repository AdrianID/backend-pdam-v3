from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status, Form, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.config import settings
from app.utils.authentication import (
    create_access_token,
    create_refresh_token,
    verify_password
)
from app.schemas.user import Token
from app.crud.user import get_user_by_email, get_user_by_username, get_user_by_id, update_user
from app.db.session import get_db
from app.utils.response_handler import create_response
from app.schemas.otp import OTPVerify

router = APIRouter()

@router.post("/login")
async def login(
    *,
    db: Session = Depends(get_db),
    email: str = Body(...),
    password: str = Body(...)
) -> Any:
    """
    Login using email and password
    """
    try:
        user = get_user_by_email(db, email=email)
        
        if not user:
            return create_response(
                status=False,
                message="Incorrect email or password",
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        
        if not verify_password(password, user.password):
            return create_response(
                status=False,
                message="Incorrect email or password",
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        
        if user.status != "active":
            return create_response(
                status=False,
                message="Inactive user",
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        access_token = create_access_token(
            data={
                "sub": str(user.id),
                "email": user.email,
                "role": user.role.name
            }
        )
        
        refresh_token = create_refresh_token(
            data={"sub": str(user.id)}
        )

        return create_response(
            message="Login successful",
            data={
                "email": user.email,
                "username": user.username,
                "role": user.role.name,
                "role_id": user.role.id,
                "token": access_token,
                "refresh_token": refresh_token
            }
        )
    except Exception as e:
        return create_response(
            status=False,
            message=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@router.post("/refresh-token", response_model=Token)
def refresh_token(
    db: Session = Depends(get_db),
    refresh_token: str = None
) -> Any:
    """
    Refresh token endpoint to get a new access token
    """
    try:
        payload = jwt.decode(
            refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate refresh token",
        )
    
    user = get_user_by_id(db, id=token_data.sub)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        ),
        "refresh_token": create_refresh_token(
            data={"sub": str(user.id)}
        ),
        "token_type": "bearer",
    }

@router.post("/verify-email")
async def verify_otp(
    *,
    db: Session = Depends(get_db),
    otp_data: OTPVerify
) -> Any:
    """
    Verify OTP code
    """
    try:
        # Get user
        user = get_user_by_id(db, id=otp_data.user_id)
        if not user:
            return create_response(
                status=False,
                message="User not found",
                status_code=status.HTTP_404_NOT_FOUND
            )

        # Hardcoded OTP check
        if otp_data.code != "12345":
            return create_response(
                status=False,
                message="Invalid OTP code",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        # Update user status to active
        user_update = {"status": "active"}
        updated_user = update_user(db, db_user=user, user_in=user_update)

        # Generate tokens
        access_token = create_access_token(
            data={
                "sub": str(updated_user.id),
                "email": updated_user.email,
                "role": updated_user.role.name
            }
        )
        
        refresh_token = create_refresh_token(
            data={"sub": str(updated_user.id)}
        )

        return create_response(
            status=True,
            message="OTP verification successful",
            data={
                "user": {
                    "id": updated_user.id,
                    "email": updated_user.email,
                    "username": updated_user.username,
                    "name": updated_user.name,
                    "role": {
                        "id": updated_user.role.id,
                        "name": updated_user.role.name,
                        "display_name": updated_user.role.display_name
                    },
                    "status": updated_user.status
                },
                "token": access_token,
                "refresh_token": refresh_token
            },
            status_code=status.HTTP_200_OK
        )

    except Exception as e:
        return create_response(
            status=False,
            message=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        ) 