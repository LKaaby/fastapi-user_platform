from sqlalchemy.orm import Session
from src.models.user import User
from src.core.security import get_password_hash, verify_password
from src.schemas.user import UserCreate

def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user_in: UserCreate) -> User:
    hashed = get_password_hash(user_in.password)
    db_user = User(username=user_in.username, hashed_password=hashed, role=user_in.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str) -> User | None:
    user = get_user_by_username(db, username=username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user