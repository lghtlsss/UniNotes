from pydantic import BaseModel, Field


class SLoginAndRegister(BaseModel):
    email: str
    password: str = Field(min_length=8)
