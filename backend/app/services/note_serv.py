from fastapi import HTTPException, status
from app.schemas import SNoteCreate
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Note
from sqlalchemy import select


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


async def change_title_serv(new_title: str, note_id: int, db: AsyncSession, user_id: int):
    db_note = await check_accessibility(note_id, db, user_id)

    db_note.title = new_title
    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise
    await db.refresh(db_note)
    return db_note


async def update_content_serv(content, note_id: int, db: AsyncSession, user_id: int):
    db_note = await check_accessibility(note_id, db, user_id)

    db_note.content = content.content

    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise
    await db.refresh(db_note)
    return db_note
