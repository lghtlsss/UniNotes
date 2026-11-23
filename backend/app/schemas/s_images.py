from pydantic import BaseModel, ConfigDict
from datetime import datetime


class SImageLoadResponse(BaseModel):
    id: int
    note_id: int
    object_key: str
    filename: str
    size: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
