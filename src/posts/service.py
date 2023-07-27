from typing import Optional

from fastapi import HTTPException
from fastapi_pagination import paginate, Params
from fastapi_pagination.utils import verify_params
from sqlalchemy import update, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import user
from src.base.exception import get_404_exception
from src.base.schemas import Response
from src.base.service_base import Service
from src.posts.models import post
from src.posts.schemas import PostCreate, PostUpdate, PostResponse


class PostService(Service):
    model = post
    create_schema = PostCreate
    update_schema = PostUpdate
    get_schema = PostResponse

    async def update(
        self,
        session: AsyncSession,
        schema: PostUpdate,
        post_id: int,
        user_id: int,
        *args,
        **kwargs
    ) -> Optional[PostUpdate]:
        """Обновление"""
        stmt = (
            update(self.model)
            .where(post.c.id == post_id, user.c.id == user_id)
            .values(title=schema.title, text=schema.text)
        )
        response = Response(message="Обновлено")
        obj = await session.execute(stmt)
        await session.commit()
        get_404_exception(obj.rowcount)
        return response

    async def all(self, session: AsyncSession, params: Params) -> Optional[PostResponse]:
        """Выдаем все посты с пагинацией"""
        params, raw_params = verify_params(params, "limit-offset")
        limit, skip = getattr(raw_params, "limit", 50), getattr(raw_params, "offset", 0)
        query = select(
            post.c.id, post.c.title, post.c.text,
        ).offset(skip).limit(skip+limit).order_by(post.c.created_at.desc())
        result = await session.execute(query)
        objs = result.fetchall()

        posts = [PostResponse(
            id=obj.id,
            title=obj.title,
            text=obj.text,
        ) for obj in objs]

        return paginate(posts, params)

    async def get_obj(
        self,
        session: AsyncSession,
        pk: int,
    ) -> Optional[PostResponse]:
        stmt = select(self.model).where(self.model.c.id == pk)
        obj = await session.execute(stmt)
        get_404_exception(obj.rowcount)
        obj = obj.one_or_none()
        return PostResponse(
            id=obj.id,
            title=obj.title,
            text=obj.text,
        )


post_s = PostService()
