from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse, JSONResponse
from sqlalchemy.orm import Session
from src.db.session import get_db
from src.schemas.user import UserCreate, UserOut, UserLogin
from src.core.security import create_access_token, create_refresh_token
from src.models.user import User
from src.utils.dependencies import get_current_user
from src.crud.user import get_user_by_username, create_user, authenticate_user

router = APIRouter()

@router.post("/register")
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    try:
        db_user = get_user_by_username(db, username=user_data.username)
        if db_user:
            return JSONResponse(
                status_code=400,
                content={"detail": "Username already registered"}
            )

        new_user = create_user(db, user_in=user_data)

        return JSONResponse(
            status_code=200,
            content={"message": "User created successfully", "user_id": new_user.id}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"detail": f"Registration failed: {str(e)}"}
        )

@router.post("/login")
async def login(
    login_data: UserLogin,  # This should work with your current frontend
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, username=login_data.username, password=login_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access_token = create_access_token(data={"sub": user.username, "id": user.id})
    refresh_token = create_refresh_token(data={"sub": user.username, "id": user.id})

    response = RedirectResponse(url="/dashboard", status_code=303)
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)

    return response

@router.post("/logout")
async def logout():
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return response

@router.get("/me", response_model=UserOut)
async def read_me(user: User = Depends(get_current_user)):
    return user