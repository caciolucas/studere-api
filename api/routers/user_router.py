from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.session import get_db
from schemas.user_schemas import UserCreate, UserLogin, UserResponse, UserLoginResponse
from services.user_service import UserService

router = APIRouter()


@router.post("/register/", response_model=UserResponse, status_code=201)
def register_user(body: UserCreate, db: Session = Depends(get_db)):
    try:
        user_service = UserService(db)
        return user_service.register_user(body.email, body.password, body.full_name)
    except Exception as e:
        raise HTTPException(
            status_code=e.status_code if hasattr(e, 'status_code') else 500,
            detail=str(e)
        ) from e


@router.post("/login/", response_model=UserLoginResponse, status_code=201)
def login_user(body: UserLogin, db: Session = Depends(get_db)):
    try:
        user_service = UserService(db)
        return user_service.login(body.email, body.password)
    except Exception as e:
        raise HTTPException(
            status_code=e.status_code if hasattr(e, 'status_code') else 500,
            detail=str(e)
        ) from e
