from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    email: str
    password: str
    token: Optional[str] = None
    
class UserIn(UserBase):
    email: str
    password: str
    
class Token(BaseModel):
    token: str