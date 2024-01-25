from src.main import Base
from sqlalchemy import Column, String, Integer
from src.auth.models import User

class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    content = Column(String(255))
    payload = Column(String(255))