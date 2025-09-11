# fastapi
from fastapi import FastAPI

# 3'rd party
from sqladmin import Admin, ModelView

# local
from src.core.db import Base, engine
from src.api.v1 import auth, user
from src.models.user import User as UserModel


Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Registration and Email Verification System")
admin = Admin(app, engine)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(user.router, prefix="/api/v1/users", tags=["users"])


class UserAdmin(ModelView, model=UserModel):
    column_list = [
        UserModel.id,
        UserModel.email,
        UserModel.is_active,
    ]
    form_columns = [
        UserModel.email,
        UserModel.hashed_password,
        UserModel.is_active,
    ]


admin.add_view(UserAdmin)
