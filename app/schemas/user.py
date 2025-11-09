from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    name: str
    username: str

class UserCreate(UserBase):
    password: str
    is_admin: Optional[bool] = False

class User(UserBase):
    id: int
    is_admin: bool
    created_dt: datetime

    model_config = ConfigDict(from_attributes=True)
