from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .models import User
from .schemas import UserIn, Token
from src.main import get_db

router = APIRouter()



# Define a route for user signup with a POST method. The response model will be Token.
@router.post("/signup", response_model=Token)
def sign_up(user: UserIn, db: Session = Depends(get_db)):  # The function takes a UserIn object and a database session as parameters.
    # Query the database for a user with the same email as the one provided.
    db_user = db.query(User).filter(User.email == user.email).first()
    # If a user with the same email is found, raise an HTTPException with status 400 and a detail message "Email already registered".
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    # If no user with the same email is found, create a new User object with the provided email.
    db_user = User(email=user.email)
    # Set the password for the new user using the set_password method.
    db_user.set_password(user.password)
    # Create a token for the new user using the create_token method.
    db_user.create_token()
    # Add the new user to the database session.
    db.add(db_user)
    # Commit the changes to the database.
    db.commit()
    # Refresh the session to get the current state of the new user.
    db.refresh(db_user)
    # Return the token of the new user.
    return {"token": db_user.token}

# Define a route for user login with a POST method. The response model will be Token.
@router.post("/login", response_model=Token)
def login(user: UserIn, db: Session = Depends(get_db)):  # The function takes a UserIn object and a database session as parameters.
    # Query the database for a user with the same email as the one provided.
    db_user = db.query(User).filter(User.email == user.email).first()
    # If no user is found or the provided password is incorrect, raise an HTTPException with status 401 and a detail message "Incorrect email or password".
    if not db_user or not db_user.verify_password(user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # If a user is found and the password is correct, create a token for the user using the create_token method.
    db_user.create_token()
    db.commit()
    # Return the token of the user.
    return {"token": db_user.token}