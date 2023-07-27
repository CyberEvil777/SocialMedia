from typing import Optional, Type, TypeVar

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import delete, exists, insert, update, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.base.exception import get_404_exception
from src.base.schemas import Response

CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
GetSchemaType = TypeVar("GetSchemaType", bound=BaseModel)
QuerySchemaType = TypeVar("QuerySchemaType", bound=BaseModel)


class BaseService:
    """Класс интерфейс для сервисов"""

    async def create(self):
        """Создание"""
        pass

    async def update(self):
        """Обновление"""
        pass

    async def delete(self):
        """Удаление"""
        pass

    async def all(self):
        """Выдача всех"""
        pass

    async def filter(self):
        """Фильтрация"""
        pass

    async def get(self):
        pass

    async def get_obj(self):
        pass


class Service(BaseService):
    model: Type[tuple]
    create_schema: CreateSchemaType
    update_schema: UpdateSchemaType
    query_schema: QuerySchemaType
    get_schema: GetSchemaType

    async def create(
        self, session: AsyncSession, schema, *args, **kwargs
    ) -> Optional[CreateSchemaType]:
        """Создание"""
        stmt = insert(self.model).values(**schema.dict(exclude_unset=True), **kwargs)
        obj = await session.execute(stmt)
        await session.commit()
        get_404_exception(obj.rowcount)
        return Response(message="Создано")

    async def update(
        self, session: AsyncSession, schema, *args, **kwargs
    ) -> Optional[UpdateSchemaType]:
        """Обновление"""
        stmt = (
            update(self.model).where(**kwargs).values(**schema.dict(exclude_unset=True))
        )
        await session.execute(stmt)
        await session.commit()
        return Response(message="Обновлено")

    async def delete(self, session: AsyncSession, pk: int, *args, **kwargs):
        """Удаление"""
        stmt = delete(self.model).where(self.model.c.id == pk, **kwargs)
        obj = await session.execute(stmt)
        await session.commit()
        get_404_exception(obj.rowcount)
        return Response(message="Удалено")

    async def get_obj(
        self,
        session: AsyncSession,
        pk: int,
    ) -> Optional[GetSchemaType]:
        stmt = select(self.model).where(self.model.c.id == pk)
        obj = await session.execute(stmt)
        get_404_exception(obj.rowcount)
        return obj.fetchall()

    async def all(self, session: AsyncSession,  skip: int = 0, limit: int = 100) -> Optional[GetSchemaType]:
        stmt = select(self.model).offset(skip).limit(limit)
        result = await session.execute(stmt)
        get_404_exception(result.rowcount)
        return result.fetchall()


