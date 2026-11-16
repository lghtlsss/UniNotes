from sqlalchemy import ForeignKey, String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from app.base import Base


class Image(Base):
    __tablename__ = "images"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    note_id: Mapped[int] = mapped_column(
        ForeignKey("notes.id", ondelete="CASCADE"),
        nullable=False
    )

    object_key: Mapped[str] = mapped_column(
        String(512),
        nullable=False,
        unique=True
    )

    filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    content_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    size: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
