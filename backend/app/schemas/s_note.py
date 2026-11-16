from datetime import datetime
from pydantic import BaseModel, ConfigDict, field_validator
from zoneinfo import ZoneInfo
from typing import Any


class SNoteCreate(BaseModel):
    title: str
    content: dict[str, Any]


class SNoteResponse(BaseModel):
    id: int
    title: str
    content: dict[str, Any]
    version: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @field_validator("created_at", "updated_at")
    @classmethod
    def convert_timezone(cls, value: datetime) -> datetime:
        return value.astimezone(ZoneInfo("Europe/Moscow"))


class SNoteContentUpdate(BaseModel):
    content: dict[str, Any]
    version: int


class SNoteTitleUpdate(BaseModel):
    title: str
    version: int
