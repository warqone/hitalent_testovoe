from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_async_session
from src.core.logger import logger
from src.models.chat import Chat
from src.models.message import Message
from src.schemas.chat import ChatCreate, ChatOut, ChatWithMessages
from src.schemas.message import MessageCreate, MessageOut

router = APIRouter()


@router.post(
        '/', response_model=ChatOut,
        status_code=HTTPStatus.CREATED,
        summary='Создать чат'
)
async def create_chat(
    payload: ChatCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Создание чата."""
    title = payload.title.strip()
    if not title:
        raise HTTPException(
            HTTPStatus.BAD_REQUEST, 'Название не может быть пустым'
        )

    chat = Chat(title=title)
    session.add(chat)
    await session.commit()
    await session.refresh(chat)
    logger.info(f'Создан чат {chat.id}')
    return chat


@router.post(
        '/{chat_id}/messages/',
        response_model=MessageOut,
        status_code=HTTPStatus.CREATED,
        summary='Создать сообщение'
)
async def create_message(
    chat_id: int,
    payload: MessageCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Создание сообщения в чате."""
    chat = await session.get(Chat, chat_id)
    if not chat:
        raise HTTPException(HTTPStatus.NOT_FOUND, 'Чат не найден.')

    text = payload.text.strip()
    if not text:
        raise HTTPException(
            HTTPStatus.BAD_REQUEST, 'Текст не может быть пустым.'
        )

    message = Message(chat_id=chat_id, text=text)
    session.add(message)
    await session.commit()
    await session.refresh(message)
    logger.info(f'Создано сообщение {message.id} в чате {chat_id}')
    return message


@router.get(
        '/{chat_id}',
        response_model=ChatWithMessages,
        status_code=HTTPStatus.OK,
        summary='Получить чат'
)
async def get_chat(
    chat_id: int,
    limit: int = Query(20, ge=1, le=100),
    session: AsyncSession = Depends(get_async_session),
):
    """Получение чата и его сообщений."""
    chat = await session.get(Chat, chat_id)
    if not chat:
        raise HTTPException(HTTPStatus.NOT_FOUND, 'Чат не найден.')

    stmt = (
        select(Message)
        .where(Message.chat_id == chat_id)
        .order_by(Message.created_at.desc())
        .limit(limit)
    )
    result = await session.execute(stmt)
    messages = list(reversed(result.scalars().all()))
    logger.info(f'Получены сообщения {len(messages)} в чате {chat_id}')
    return {
        'id': chat.id,
        'title': chat.title,
        'created_at': chat.created_at,
        'messages': messages,
    }


@router.delete(
        '/{chat_id}',
        status_code=HTTPStatus.NO_CONTENT,
        summary='Удалить чат'
)
async def delete_chat(
    chat_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Удаление чата."""
    chat = await session.get(Chat, chat_id)
    if not chat:
        raise HTTPException(HTTPStatus.NOT_FOUND, 'Чат не найден.')

    await session.delete(chat)
    await session.commit()
    return logger.info(f'Удален чат {chat_id}')
