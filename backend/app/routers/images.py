from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import User
from app.dependencies import get_current_user
from app.schemas import SImageLoadResponse
from app.services.images_serv import upload_image_serv, get_image_link, delete_image_serv

router = APIRouter(prefix="images", tags=["Images"])


@router.post("/{note_id}/upload", response_model=SImageLoadResponse)
async def upload_image(note_id: int, file: UploadFile = File(...), db: AsyncSession = Depends(get_db),
                       user: User = Depends(get_current_user)):
    return await upload_image_serv(note_id, file, db, user.id)


@router.get("/get/{image_id}", response_model={"link": str})
async def get_link_for_image(image_id: int, note_id: int,
                             db: AsyncSession = Depends(get_db),
                             user: User = Depends(get_current_user)):
    return await get_image_link(image_id, note_id, db, user.id)


@router.delete("/delete/{image_id}")
async def delete_image(image_id: int, note_id: int,
                       db: AsyncSession = Depends(get_db),
                       user: User = Depends(get_current_user)
                       ):
    return await delete_image_serv(image_id, note_id, db, user.id)
