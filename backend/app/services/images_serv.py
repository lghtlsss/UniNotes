from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Note, Image
from sqlalchemy import select
from sqlalchemy.orm.attributes import flag_modified
from app.services.storage_serv import storage
from uuid import uuid4


async def upload_image_serv(note_id: int, file, db: AsyncSession, user_id):
    statement = await db.execute(select(Note).where(Note.id == note_id, Note.user_id == user_id))
    note = statement.scalar_one_or_none()

    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")

    if not file.content_type:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unknown file type")

    if file.filename is None:
        file.filename = 'untitled'

    object_key = f"{user_id}/notes/{note_id}/{uuid4()}{file.filename}"
    await storage.upload_file(file, object_key, file.content_type)
    # TODO: Сделать проверку на то, что файл реально того типа что указан через pillow

    uploaded_image = Image(
        note_id=note.id,
        object_key=object_key,
        filename=file.filename,
        size=file.size,
    )

    db.add(uploaded_image)
    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise
    await db.refresh(uploaded_image)
    return uploaded_image


async def check_image_accessibility(image_id: int, note_id: int, db: AsyncSession, user_id: int):
    statement = await db.execute(
        select(Image).where(Image.id == image_id, Image.note_id == note_id, Note.user_id == user_id))
    image = statement.scalar_one_or_none()

    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")

    if not await storage.file_exists(image.object_key):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

    return image


async def get_image_link(image_id: int, note_id: int, db: AsyncSession, user_id: int):
    image = await check_image_accessibility(image_id, note_id, db, user_id)

    link = await storage.generate_load_presigned_url(image.object_key, 7200)

    return {"temp_link": link}


async def delete_image_serv(image_id: int, note_id: int, db: AsyncSession, user_id: int):
    image = await check_image_accessibility(image_id, note_id, db, user_id)

    image_id = image.id
    statement = await db.execute(select(Note).where(
        Note.id == note_id,
        Note.user_id == user_id)
    )
    note = statement.scalar_one_or_none()
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note nod found")

    try:
        await storage.delete_file(image.object_key)
        await db.delete(image)
        await db.commit()
    except Exception:
        await db.rollback()
        raise

    note.content["content"] = [
        item
        for item in note.content["content"]
        if not (item.get("type") == "image" and item.get("image_id") == image_id)
    ]

    flag_modified(note, "content")
    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise

    return {"message": "success"}
