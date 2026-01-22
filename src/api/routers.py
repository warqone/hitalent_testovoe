from fastapi import APIRouter

from src.api.endpoints.chats import router as chat_router

main_router = APIRouter()

main_router.include_router(
    chat_router,
    prefix='/chats',
    tags=['Чаты'],
)
