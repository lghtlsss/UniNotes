from fastapi import APIRouter, Depends, HTTPException, status
from app.database import get_db
from app.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.schemas import SLoginAndRegister
from sqlalchemy import select
from app.passw_security import hash_password, verify_password
from app.dependencies import create_access_token


async def register_serv(data: SLoginAndRegister, db: AsyncSession = Depends(get_db)):
    test_user = await db.execute(select(User).where(User.email == data.email)).scalar_one_or_none()

    if test_user is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Пользователь с таким email уже существует")

    db_user = User(
        email=data.email,
        password=hash_password(data.password),
    )

    db.add(db_user)
    try:
        await db.commit()
    except IntegrityError as exc:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User with this email already exists") from exc
    await db.refresh(db_user)

    access_token = create_access_token(db_user.id)

    return {
        "user": db_user,
        "token": {
            "access_token": access_token,
            "token_type": "bearer"
        }
    }


async def login_serv(data: SLoginAndRegister, db: AsyncSession = Depends(get_db)):
    test_user = await db.execute(select(User).where(User.email == data.email)).scalar_one_or_none()

    if test_user is None:
        raise HTTPException(status_code=status.HTTP_404_CONFLICT, detail="Пользователь с таким email не найден")

    if not verify_password(data.password, test_user.hashed_password):
        raise HTTPException(401, "Invalid email or password")

    access_token = create_access_token(test_user.id)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

