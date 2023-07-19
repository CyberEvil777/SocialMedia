from typing import Optional

from fastapi import HTTPException
from sqlalchemy import insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import user
from src.base.schemas import Response
from src.base.service_base import Service
from src.posts.models import post
from src.posts.schemas import PostCreate, PostUpdate


class PostService(Service):
    model = post
    create_schema = PostCreate
    update_schema = PostUpdate

    async def update(self, session: AsyncSession, schema: PostUpdate, post_id: int, user_id: int, *args, **kwargs) -> Optional[PostUpdate]:
        """Обновление"""
        stmt = update(self.model).where(post.c.id == post_id, user.c.id == user_id).values(title=schema.title, text=schema.text)
        response = Response(message="Обновлено")
        obj = await session.execute(stmt)
        await session.commit()
        if not obj:
            raise HTTPException(status_code=404, detail="Объект не найден")
            response = Response(message="Объект не найден")
        return response


post_s = PostService()
