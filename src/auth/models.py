from src.main import Base
from sqlalchemy import Column, String
from passlib.context import CryptContext
import secrets

# The password context used to hash and verify passwords.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "user"
    email = Column(String(255), primary_key=True, index=True)
    password = Column(String(255))
    token = Column(String(255))
    
    def set_password(self, password):
        """
        Sets the password for the user.

        Args:
            password (str): The password to set.
        """
        self.password = pwd_context.hash(password)

    def verify_password(self, password):
        """
        Verifies if the provided password matches the user's password.

        Args:
            password (str): The password to verify.

        Returns:
            bool: True if the password is correct, False otherwise.
        """
        return pwd_context.verify(password, self.password)
    
    def create_token(self):
        """
        Generates a new token for the user.
        """
        self.token = secrets.token_hex(16)