import asyncio
from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from .utils import get_db
from .models import User
from .utils import send_confirmation_email

app = FastAPI()

@app.post("/register")
async def register_user(email: str, db: Session = Depends(get_db)):
    new_user = User(email=email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Asynchronously send the confirmation email
    asyncio.create_task(send_confirmation_email(email))

    return JSONResponse(content={"message": "Registration Success."})
