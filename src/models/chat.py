from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from src.constants import MAX_TITLE_LENGTH
from src.core.db import BaseModel


class Chat(BaseModel):
    title = Column(String(MAX_TITLE_LENGTH), nullable=False)
    messages = relationship(
        'Message', back_populates='chat', cascade='all, delete-orphan'
    )
