from datetime import datetime
from pydantic import BaseModel, Field

from src.constants import MIN_LENGTH, MAX_TITLE_LENGTH
from src.schemas.message import MessageOut


class ChatCreate(BaseModel):
    title: str = Field(min_length=MIN_LENGTH, max_length=MAX_TITLE_LENGTH)


class ChatOut(BaseModel):
    id: int
    title: str
    created_at: datetime


class ChatWithMessages(ChatOut):
    messages: list[MessageOut]
