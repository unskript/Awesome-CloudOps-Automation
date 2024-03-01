from sqlalchemy.orm import Session

from db.models.user import User
from db.schemas.user_schema import UserCreate


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session):
    return db.query(User).all()


def create_user(db: Session, user: UserCreate):
    password = user.password
    db_user = User(email=user.email, hashed_password=password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user