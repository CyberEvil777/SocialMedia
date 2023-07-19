from fastapi import APIRouter, Depends

from src.auth.base_config import current_user
from src.auth.models import User
from src.auth.schemas import UserIdDTO
from src.database import get_async_session
from src.posts.schemas import PostCreate
from sqlalchemy.ext.asyncio import AsyncSession

from src.posts.service import post_s

router = APIRouter(
    prefix="/post",
    tags=["Post"]
)


@router.post('/')
async def create_post(
        schema: PostCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    """Создания поста."""
    return await post_s.create(session, schema, UserIdDTO(user_id=user.id))


@router.post('/{post_id}')
async def update_post(
        post_id: int,
        schema: PostCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    """Обновление поста."""
    return await post_s.update(session, schema, post_id, user.id)


@router.delete('/{post_id}')
async def delete_post(
        post_id: int,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    """Удаление поста."""
    return await post_s.delete(session, post_id, UserIdDTO(user_id=user.id))
