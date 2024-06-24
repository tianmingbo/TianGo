from typing import Any
from typing import Self

from sqlalchemy import select, insert, func, text, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from chain_exception.exceptions import ItemDuplicateException, DBException, ItemNotFoundException
from .common import pagination, _SqlalchemyModelToSchemaModel


class ChainBaseModel(_SqlalchemyModelToSchemaModel):

    @classmethod
    async def count(cls, session: AsyncSession, query_expression=tuple()) -> int:
        """
        根据条件查询记录数量
        """
        query_expression = tuple(query_expression)
        base_count_section = select(func.count(text("*"))).select_from(cls).where(*query_expression)
        return (await session.execute(base_count_section)).scalars().first()

    @classmethod
    async def insert(cls, session: AsyncSession, values: dict) -> None:
        """
        插入单条数据
        """
        try:
            _orm = insert(cls).values(**values)
            await session.execute(_orm)
            await session.commit()
        except IntegrityError as e:
            raise ItemDuplicateException(error=str(e))

        except Exception as e:
            raise DBException(error=str(e))

    @classmethod
    async def update_one(cls, session: AsyncSession, values: dict, query_expression=tuple()) -> Self:
        """
        更新第一条数据
        """
        query_expression = tuple(query_expression)
        query_result = await cls.query_one(session, query_expression)
        if not query_result:
            raise ItemNotFoundException(msg="记录不存在")
        try:
            for k, v in values.items():
                setattr(query_result, k, v)

            await session.commit()
            return query_result

        except Exception as e:
            raise DBException(error=str(e))

    @classmethod
    async def update_all(cls, session: AsyncSession, values: dict[str, Any], query_expression=tuple()) -> list[Self]:
        """
        更新所有符合条件的数据
        """
        try:
            query_expression = tuple(query_expression)
            query = await session.execute(select(cls).where(*query_expression))
            query_result = query.scalars().all()

            for item in query_result:
                for k, v in values.items():
                    setattr(item, k, v)
            await session.commit()

            return query_result

        except Exception as e:
            raise DBException(error=str(e))

    @classmethod
    async def query_one(cls, session: AsyncSession, query_expression=tuple()) -> Self:
        """
        查询符合条件的第一条数据
        """
        try:
            query_expression = tuple(query_expression)
            _orm = select(cls).where(*query_expression)
            query_row = await session.execute(_orm)
            return query_row.scalars().first()

        except Exception as e:
            raise DBException(error=str(e))

    @classmethod
    async def query_all(cls, session: AsyncSession, query_expression=tuple()) -> list[Self]:
        """
        查询符合条件的所有数据
        """
        try:
            query_expression = tuple(query_expression)
            _orm = select(cls).where(*query_expression)
            return (await session.execute(_orm)).scalars().all()
        except Exception as e:
            raise DBException(error=str(e))

    @classmethod
    async def query_list(
            cls,
            session: AsyncSession,
            query_expression=tuple(),
            /,
            order_by_expression=tuple(),
            per_page: int = 20,
            page: int = 1,
    ) -> tuple[list, int, int]:
        """
        分页检索符合条件的记录
        """
        try:
            query_expression = tuple(query_expression)
            order_by_expression = tuple(order_by_expression)
            count = await cls.count(session, query_expression=query_expression)
            base_section = select(cls).where(*query_expression).order_by(*order_by_expression)
            infolist, pages, total = await pagination(session, base_section, count, per_page, page)
            return infolist, pages, total
        except Exception as e:
            raise DBException(error=str(e))

    @classmethod
    async def delete(cls, session: AsyncSession, query_expression=tuple()) -> None:
        """
        删除符合条件的记录
        """
        query_expression = tuple(query_expression)

        if not await cls.query_one(session, query_expression=query_expression):
            raise ItemNotFoundException()
        try:
            _orm = delete(cls).where(*query_expression)
            await session.execute(_orm)
            await session.commit()
        except Exception as e:
            raise DBException(error=str(e))
