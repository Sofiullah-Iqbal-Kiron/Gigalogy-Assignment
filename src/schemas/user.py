# python
from datetime import datetime
from typing import Optional, Annotated

# 3'rd party
from pydantic import BaseModel, EmailStr, StringConstraints, computed_field


class UserRead(BaseModel):
    id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: EmailStr
    email_verified: bool
    last_login: Optional[datetime] = None
    joined_at: datetime

    class Config:
        from_attributes = True

    @computed_field
    @property
    def full_name(self) -> Optional[str]:
        if self.first_name or self.last_name:
            return " ".join(part for part in [self.first_name, self.last_name] if part)
        
        return None


class UserCreate(BaseModel):
    first_name: Optional[Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=128)]] = None
    last_name: Optional[Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=128)]] = None
    email: EmailStr
    password: Annotated[str, StringConstraints(strip_whitespace=True, min_length=8, max_length=128)]
