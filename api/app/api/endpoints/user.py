from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.schemas.user_schema import UserSchema, UserBase, UserCreate
from db.database import get_db
from db.crud.user_crud import *

users_router = APIRouter(
    prefix="/users"
)


@users_router.get(path="/test_user", response_model=dict[str, str])
async def read_users():
    return {"message": "Read Users"}

@users_router.post("/", response_model=UserSchema)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, user=user)


@users_router.get("/", response_model=list[UserSchema])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users


@users_router.get("/{user_id}", response_model=UserSchema)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user