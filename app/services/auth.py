from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, hash_password, verify_password
from app.models.enums import UserRole
from app.models.user import User
from app.schemas.auth import RegisterRequest


async def register_user(user_data: RegisterRequest, db: AsyncSession):
    existing_user = await db.scalar(
        select(User).where(User.email == str(user_data.email))
    )

    if existing_user:
        raise HTTPException(status_code=409, detail="Email is already registered")

    new_user = User(
        full_name=user_data.full_name,
        email=str(user_data.email),
        password_hash=hash_password(user_data.password),
        phone_number=user_data.phone_number,
        role=UserRole.REPORTER,  # Default role for new users
    )

    db.add(new_user)

    try:
        await db.commit()
        await db.refresh(new_user)

    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Email is already registered")

    return new_user


async def login_user(form_data: OAuth2PasswordRequestForm, db: AsyncSession):

    user = await db.scalar(select(User).where(User.email == form_data.username))

    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account has been deactivated",
        )

    access_token = create_access_token({"sub": str(user.user_id)})

    return {"access_token": access_token, "token_type": "bearer", "user": user}
