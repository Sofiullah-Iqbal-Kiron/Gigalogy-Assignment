# sqlalchemy
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func

# local
from src.core.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    email = Column(String(254), nullable=False, unique=True, index=True)
    hashed_password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)

    email_verified = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)

    last_login = Column(DateTime(timezone=True), onupdate=func.now())
    joined_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    def __repr__(self):
        return f"<User id={self.id} email={self.email!r}>"
