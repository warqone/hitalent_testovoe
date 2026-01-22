from pydantic import BaseModel, Field
from datetime import datetime

from src.constants import MIN_LENGTH, MAX_MESSAGE_LENGTH


class MessageCreate(BaseModel):
    text: str = Field(min_length=MIN_LENGTH, max_length=MAX_MESSAGE_LENGTH)


class MessageOut(BaseModel):
    id: int
    chat_id: int
    text: str
    created_at: datetime

    class Config:
        from_attributes = True
