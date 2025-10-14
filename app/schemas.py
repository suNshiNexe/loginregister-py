from pydantic import BaseModel, EmailStr
## from typing import Optional

from pydantic import ConfigDict

class UserBase(BaseModel):
    username: str
    email: EmailStr #validação pydantic formato email

class UserCreate(UserBase):
    password: str

class User (UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)



class Token(BaseModel):
    access_token: str
    token_type: str

