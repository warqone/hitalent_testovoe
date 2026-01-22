from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from src.constants import MAX_MESSAGE_LENGTH
from src.core.db import BaseModel


class Message(BaseModel):
    chat_id = Column(Integer, ForeignKey('chat.id'))
    text = Column(String(MAX_MESSAGE_LENGTH), nullable=False)
    chat = relationship('Chat', back_populates='messages')
