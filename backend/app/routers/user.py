from fastapi import APIRouter, Depends
from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import SLoginAndRegister

from app.services import register_serv, login_serv

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/register")
async def register(data: SLoginAndRegister, db: AsyncSession = Depends(get_db)):
    return register_serv(data, db)


@router.post("/login")
async def login(data: SLoginAndRegister, db: AsyncSession = Depends(get_db)):
    return login_serv(data, db)
