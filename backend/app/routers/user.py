from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import SLoginAndRegister

from app.services import register_serv, login_serv

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register")
async def register(data: SLoginAndRegister, db: AsyncSession = Depends(get_db)):
    return await register_serv(data, db)


@router.post("/login")
async def login(data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    return await login_serv(data, db)
