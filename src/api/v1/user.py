# fastapi
from fastapi import Depends, APIRouter, HTTPException, BackgroundTasks, status
from fastapi.security import OAuth2PasswordBearer

# sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

# 3'rd party
from jose import jwt, JWTError

# local
from src.core.db import get_db
from src.models.user import User
from src.schemas.user import UserRead, UserCreate
from src.core.hash import hash_raw_password, sign_email, decode_signed_email
from src.core.utils import send_verification_email
from src.core.jwt import SECRET_KEY, ALGORITHM


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def _send_verification_email(email: str, background_tasks: BackgroundTasks):
    token = sign_email(email)
    background_tasks.add_task(send_verification_email, email, token)


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """Register a new user and send a verification email."""

    hashed_password = hash_raw_password(user.password)

    new_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        hashed_password=hashed_password,
        email_verified=False,
    )
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This email has already been taken by another account.",
        )

    _send_verification_email(new_user.email, background_tasks)

    return new_user


@router.post("/seek-email-verification")
async def seek_email_verification(email: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """Resend the verification email to a user if not yet verified."""

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No user account found within this email!",
        )
    
    if user.email_verified:
        return {"message": "Email is already verified."}

    _send_verification_email(user.email, background_tasks)

    return {"message": f"Verification email resent to {user.email}. Please check your inbox or spam."}


@router.patch("/verify-email")
async def verify_email(token: str, db: Session = Depends(get_db)):
    """Verify a user's email using the token sent to their email address."""

    email = decode_signed_email(token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid or expired token!"
        )

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="No user account found within this email!"
        )

    if user.email_verified:
        return {"message": "Email is already verified."}

    user.email_verified = True
    db.commit()

    return {"message": "Email verified successfully."}


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """Decode JWT and return the authenticated user."""
    
    unauthorized = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("email")
        if email is None:
            raise unauthorized
    except JWTError:
        raise unauthorized

    user = db.query(User).filter(User.email == email).first()
    if user is None or not user.is_active:
        raise unauthorized

    return user


@router.get("/me", response_model=UserRead, summary="My Profile")
async def user_profile(current_user: User = Depends(get_current_user)):
    return current_user
