from datetime import datetime
from pydantic import BaseModel, ConfigDict
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


class SNoteContentUpdate(BaseModel):
    content: dict[str, Any]
