from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Any

from app.database.database import get_db
from app.models import User
from app.schemas.user import UserSignup, UserLogin, UserResponse, Token
from app.auth.utils import (
    get_password_hash,
    verify_password,
    create_access_token
)

router = APIRouter()

@router.post(
    "/signup",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Регистрация нового пользователя",
    description="""
    Создание нового пользователя в системе.

    1. Проверка уникальности email
    2. Хеширование пароля для безопасности
    3. Сохранение пользователя в базу данных
    4. Возвращение данных пользователя (без пароля)
    """
)
async def signup(user_data: UserSignup, db: Session=Depends(get_db)) -> Any:
    existing_user = db.query(User).filter(User.email == user_data.email).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email уже зарегистрирован"
        )
    
    new_hashed_password = get_password_hash(user_data.password)

    new_user = User(
        email=user_data.email,
        hashed_password=new_hashed_password, 
        full_name=user_data.full_name
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post(
    "/login",
    response_model=Token,
    summary="Вход в систему",
    description="""
    Аутентификация пользователя и выдача JWT токена.
    
    1. Проверка email и пароль
    2. Если данные верные - создание JWT токен
    3. Возвращение токена для доступа к API
    """
)
async def login(user_data: UserLogin, db: Session=Depends(get_db)) -> Any:
    user = db.query(User).filter(User.email == user_data.email).first()

    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь деактивирован"
        )
    
    new_access_token = create_access_token(data={"sub": user.email})
    return Token(access_token=new_access_token)