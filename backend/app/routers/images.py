from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import User
from app.dependencies import get_current_user

router = APIRouter(prefix="Images", tags=["Images"])


@router.post("/{note_id}/upload")
def upload_image(note_id: int, file: UploadFile = File(...), db: AsyncSession = Depends(get_db),
                 user: User = Depends(get_current_user)):
    return
