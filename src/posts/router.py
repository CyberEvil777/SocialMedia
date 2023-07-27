from fastapi import APIRouter, Depends
from fastapi_pagination import Page, Params
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.base_config import current_user
from src.auth.models import User
from src.auth.schemas import UserIdDTO
from src.database import get_async_session
from src.posts.schemas import PostCreate, PostResponse
from src.posts.service import post_s

router = APIRouter(prefix="/post", tags=["Post"])


@router.post("/")
async def create_post(
    schema: PostCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Эндпойнт для создания поста."""
    return await post_s.create(session, schema, UserIdDTO(user_id=user.id))


@router.post("/{post_id}")
async def update_post(
    post_id: int,
    schema: PostCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Эндпойнт для обновления поста."""
    return await post_s.update(session, schema, post_id, user.id)


@router.delete("/{post_id}")
async def delete_post(
    post_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Эндпойнт для удаления поста."""
    return await post_s.delete(session, post_id, UserIdDTO(user_id=user.id))


@router.get("/{post_id}")
async def get_post(
    post_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Эндпойнт для выдачи одного поста."""
    return await post_s.get_obj(session, pk=post_id)


@router.get("/", response_model=Page[PostResponse])
async def get_posts(
    params: Params = Depends(),
    session: AsyncSession = Depends(get_async_session),
):
    """Эндпойнт для выдачи постов с пагинацией."""
    return await post_s.all(session, params)
