
from users.models import UsersTable
from datetime import datetime, timedelta
from config import JWT_SECRET_KEY as SECRET_KEY, JWT_ALGORITHM as ALGORITHM
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from jose import jwt
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(username: str, user_id: int, expires_delta: timedelta, role:str):
    encode = {
        "sub": username,
        "id": user_id,
        "exp": datetime.utcnow() + expires_delta
    }
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def authenticate_user(db: Session, username: str, password: str):
    db_user = db.query(UsersTable).filter(UsersTable.username == username).first()
    if not db_user or not bcrypt_context.verify(password, db_user.password):
        return False
    return db_user
