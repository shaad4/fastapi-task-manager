from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import timedelta

from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.dependencies.database import get_db
from app.db.models.user import User
from app.core.security import hash_password, verify_password, create_access_token
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.get("/me", response_model=UserResponse)
async def get_me(
    current_user: User = Depends(get_current_user)
):
    return current_user

@router.post("/register", response_model=UserResponse)
async def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    statement = select(User).where(User.username == user.username)

    result = db.execute(statement)

    existing_user = result.scalar_one_or_none()

    if existing_user is not None:
        raise HTTPException(
            status_code=409,
            detail="username alerady exist"
        )

    hashed_password = hash_password(user.password)

    new_user = User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/login")
async def login(
        user: UserLogin,
        db: Session = Depends(get_db)
):
    statement = select(User).where(User.username == user.username)
    result = db.execute(statement)

    existing_user = result.scalar_one_or_none()

    if existing_user is None:
        raise HTTPException(
            status_code=401,
            detail="invalid username or password"
        )

    password_valid = verify_password(
        user.password,
        existing_user.password_hash
    )

    if not password_valid:
        raise HTTPException(
            status_code=401,
            detail="invalid username or password"
        )

    access_token = create_access_token(
        data={"sub": str(existing_user.id)},
        expires_delta=timedelta(
            minutes=30
        )
    )

    return{
        "access_token": access_token,
        "token_type":"bearer"
    }

    

    