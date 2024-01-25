from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import models
from src.main import get_db

# Create an instance of OAuth2PasswordBearer with the token URL set to "signin"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="signin")

# Define a dependency function to get the current user
def get_current_user(
    token: str = Depends(oauth2_scheme),  # The OAuth2 token is a dependency
    db: Session = Depends(get_db)  # The database session is also a dependency
):
    # Query the database for a user with the provided token
    user = db.query(models.User).filter(models.User.token == token).first()

    # If no user is found, raise an HTTPException with status 401 (Unauthorized)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # If a user is found, return the user
    return user