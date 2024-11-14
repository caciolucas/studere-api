from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.session import get_db
from schemas.user_schemas import UserCreate, UserLogin
from services.user_service import UserService

router = APIRouter()


@router.post("/register/")
def register_user(body: UserCreate, db: Session = Depends(get_db)):
    user_service = UserService(db)

    return user_service.register_user(body.email, body.password, body.full_name)


@router.post("/login/")
def login_user(body: UserLogin, db: Session = Depends(get_db)):
    user_service = UserService(db)

    return user_service.login(body.email, body.password)
