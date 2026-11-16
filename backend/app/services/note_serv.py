from fastapi import HTTPException, status
from app.schemas import SNoteCreate, SNoteContentUpdate, SNoteTitleUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Note
from sqlalchemy import select
from datetime import datetime, timezone


async def create_note_serv(data: SNoteCreate, db: AsyncSession, user_id: int) -> Note:
    new_note = Note(
        title=data.title,
        content=data.content,
        version=1,
        user_id=user_id,
    )

    db.add(new_note)
    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise
    await db.refresh(new_note)

    return new_note


async def all_notes_serv(db: AsyncSession, user_id: int):
    result = await db.execute(select(Note).where(Note.user_id == user_id))
    return result.scalars().all()


async def note_by_id_serv(db: AsyncSession, note_id: int, user_id: int):
    result = await db.execute(select(Note).where(Note.id == note_id, Note.user_id == user_id))
    note = result.scalar_one_or_none()

    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")

    return note


async def check_accessibility(note_id: int, db: AsyncSession, user_id: int):
    res = await db.execute(select(Note).where(Note.id == note_id, Note.user_id == user_id))
    db_note = res.scalar_one_or_none()

    if db_note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")

    return db_note


async def check_version(version: int, note_id: int, db: AsyncSession):
    res = await db.execute(select(Note).where(Note.id == note_id, Note.version == version))
    db_note = res.scalar_one_or_none()

    if db_note is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Note has been modified")

    return db_note


async def change_title_serv(data: SNoteTitleUpdate, note_id: int, db: AsyncSession, user_id: int):
    await check_accessibility(note_id, db, user_id)
    db_note = await check_version(data.version, note_id, db)

    db_note.title = data.title
    db_note.updated_at = datetime.now(timezone.utc)
    db_note.version += 1

    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise
    await db.refresh(db_note)
    return db_note


async def update_content_serv(data, note_id: int, db: AsyncSession, user_id: int):
    await check_accessibility(note_id, db, user_id)

    db_note = await check_version(data.version, note_id, db)
    db_note.content = data.content
    db_note.updated_at = datetime.now(timezone.utc)
    db_note.version += 1

    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise
    await db.refresh(db_note)
    return db_note
