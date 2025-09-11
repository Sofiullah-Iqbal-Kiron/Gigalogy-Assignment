# fastapi
from fastapi import FastAPI

# 3'rd party
# from sqladmin import Admin, ModelView

# local
from src.core.db import Base, engine
from src.api.v1 import auth, user


Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Registration and Email Verification System")

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(user.router, prefix="/api/v1/users", tags=["users"])


# class UserAdmin(ModelView):
#     model = User
#     column_list = [
#         "id",
#         "email",
#         "first_name",
#         "last_name",
#         "is_active",
#         "is_superuser",
#         "joined_at",
#     ]
#     column_searchable_list = ["email", "first_name", "last_name"]
#     column_sortable_list = [
#         "id",
#         "email",
#         "first_name",
#         "last_name",
#         "is_active",
#         "is_superuser",
#         "joined_at",
#     ]
#     form_excluded_columns = ["hashed_password", "last_login"]


# admin = Admin(app, engine)
# admin.add_view(UserAdmin)
