# fastapi
from fastapi import Depends, APIRouter, HTTPException, BackgroundTasks, status

# sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

# local
from src.core.db import get_db
from src.models.user import User
from src.schemas.user import UserRead, UserCreate
from src.core.utils import hash_raw_password, send_confirmation_email


router = APIRouter()


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
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

    background_tasks.add_task(send_confirmation_email, new_user.email)

    return new_user


# @router.get("/me", response_model=UserRead, status_code=status.HTTP_200_OK)
# async def user_profile(current_user: User = Depends(get_current_user)):
#     return current_user
