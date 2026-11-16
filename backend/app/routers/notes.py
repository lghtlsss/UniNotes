from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.dependencies import get_current_user
from app.models import User
from app.schemas import SNoteCreate, SNoteResponse
from app.services import create_note_serv, note_by_id_serv, all_notes_serv, change_title_serv

router = APIRouter(prefix="/notes", tags=["Notes"])


@router.post("/create", response_model=SNoteResponse)
async def create_note(data: SNoteCreate, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    return await create_note_serv(data, db, user.id)


@router.get("/all", response_model=list[SNoteResponse])
async def get_all_notes(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    return await all_notes_serv(db, user.id)


@router.get("/byid/{note_id}")
async def get_single_note(note_id: int, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    return await note_by_id_serv(db, note_id, user.id)


@router.put("/change_title/{note_id}", response_model=SNoteResponse)
async def change_title(new_title: str, note_id: int, db: AsyncSession = Depends(get_db),
                       user: User = Depends(get_current_user)):
    return await change_title_serv(new_title, note_id, db, user.id)
