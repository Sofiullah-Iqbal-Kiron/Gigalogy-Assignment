# fastapi
from fastapi import FastAPI


# local
from src.core.db import Base, engine
from src.api.v1 import auth, user


Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Registration and Email Verification System")

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(user.router, prefix="/api/v1/users", tags=["users"])
