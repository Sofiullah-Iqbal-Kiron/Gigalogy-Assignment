# fastapi
from fastapi import Depends, APIRouter, HTTPException, status

# sqlalchemy
from sqlalchemy.orm import Session

# 3'rd party
from jose import jwt, JWTError

# local
from src.core.db import get_db
from src.models.user import User
from src.schemas.auth import LoginRequest, TokenPair, TokenRefresh
from src.core.jwt import (
    create_access_token,
    create_refresh_token,
    SECRET_KEY,
    ALGORITHM,
)
from core.utils import verify_password


router = APIRouter()


@router.post("/login", response_model=TokenPair)
async def login_user(login_data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No user account found within this email!",
        )

    if not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password!",
        )

    token_data = {"id": str(user.id), "email": user.email}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    return TokenPair(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=TokenPair)
async def refresh_token(request: TokenRefresh):
    try:
        payload = jwt.decode(request.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])

        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type.",
            )

        user_id = payload.get("id")
        email = payload.get("email")
        if not user_id or not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload.",
            )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token.",
        )

    token_data = {"id": user_id, "email": email}
    access_token = create_access_token(token_data)

    return TokenPair(access_token=access_token, refresh_token=request.refresh_token)
