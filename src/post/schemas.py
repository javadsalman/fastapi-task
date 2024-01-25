from pydantic import BaseModel
from typing import Optional

class PostBase(BaseModel):
    id: int
    title: str
    content: str
    payload: Optional[str] = None


class PostAddOut(BaseModel):
    id: int
