from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from src.models.user import User
from src.schemas.user import UserOut, UserUpdate, UserCreate
from src.crud.user import get_user_by_username, create_user
from src.db.session import get_db
from src.utils.dependencies import admin_required
from src.core.security import get_password_hash

router = APIRouter()

class PaginatedUsers(BaseModel):
    items: List[UserOut]
    total: int
    page: int
    size: int

@router.get("/users", response_model=PaginatedUsers)
def list_users(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    _: User = Depends(admin_required),
):
    offset = (page - 1) * size
    users = db.query(User).offset(offset).limit(size).all()
    total = db.query(User).count()
    return {"items": users, "total": total, "page": page, "size": size}

@router.post("/users", response_model=UserOut, status_code=201)
def create_admin_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
    _: User = Depends(admin_required),
):
    if get_user_by_username(db, user_in.username):
        raise HTTPException(400, "Username already exists")
    return create_user(db, user_in)

@router.put("/users/{user_id}", response_model=UserOut)
def update_user(
    user_id: int,
    update: UserUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(admin_required),
):
    db_user = db.get(User, user_id)
    if not db_user:
        raise HTTPException(404, "User not found")
    if update.username:
        db_user.username = update.username
    if update.password:
        db_user.hashed_password = get_password_hash(update.password)
    if update.role:
        db_user.role = update.role
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/users/{user_id}", status_code=204)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(admin_required),
):
    db_user = db.get(User, user_id)
    if not db_user:
        raise HTTPException(404, "User not found")
    db.delete(db_user)
    db.commit()