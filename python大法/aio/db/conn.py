# conn

import asyncio
from typing import AsyncGenerator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base


class DBConnectionManager:
    def __init__(self,
                 url: str = None,
                 *,
                 dialect: str = "mysql",
                 driver: str = "aiomysql",
                 username: str = "root",
                 password: str = "root",
                 host: str = "localhost",
                 port: int = 3306,
                 dbname: str = "test",
                 pool_recycle: int = 3_600,
                 echo: bool = False,
                 expire_on_commit: bool = False,
                 autocommit: bool = False,
                 autoflush: bool = False,
                 is_async: bool = True,
                 ):
        self.url: str

        if url:
            self.url = url

        else:
            self.url = f"{dialect}+{driver}://{username}:{password}@{host}:{port}/{dbname}?charset=utf8mb4&binary_prefix=true"
        self.is_async = is_async
        self.pool_recycle = pool_recycle
        self.echo = echo
        self.expire_on_commit = expire_on_commit
        self.autocommit = autocommit
        self.autoflush = autoflush
        self.Base = declarative_base()

        sessionmaker_args = {
            "expire_on_commit": self.expire_on_commit,
            "autocommit": self.autocommit,
            "autoflush": self.autoflush
        }
        if is_async:
            self.engine = self.__create_async_engine()
            self.sessionmaker = sessionmaker(
                self.engine,
                class_=AsyncSession,
                **sessionmaker_args
            )
        else:
            self.engine = self.__create_sync_engine()
            self.sessionmaker = sessionmaker(
                self.engine,
                **sessionmaker_args
            )

    def __create_sync_engine(self):
        return create_engine(self.url, echo=self.echo, pool_recycle=self.pool_recycle)

    def __create_async_engine(self):
        return create_async_engine(self.url, echo=self.echo, pool_recycle=self.pool_recycle)

    async def async_session(self) -> AsyncGenerator[AsyncSession, None]:
        """session生成器 作为fastapi的Depends选项"""
        async with self.sessionmaker() as session:
            yield session

    def session(self):
        session = self.sessionmaker()
        try:
            yield session
            session.commit()
        except Exception as exc:
            session.rollback()
            raise exc
        finally:
            session.close()

    async def create_all(self):
        if self.is_async:
            await self.__async_create_all()
        else:
            await asyncio.to_thread(self.__sync_create_all)

    async def __async_create_all(self):
        """创建表"""
        async with self.engine.begin() as conn:
            await conn.run_sync(self.Base.metadata.create_all)

    def __sync_create_all(self):
        self.Base.metadata.create_all(self.engine)

    async def drop_all(self):
        """删除表"""
        if self.is_async:
            await self.__async_drop_all()
        else:
            await asyncio.to_thread(self.__sync_drop_all)

    async def __async_drop_all(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(self.Base.metadata.drop_all)

    def __sync_drop_all(self):
        self.Base.metadata.drop_all(self.engine)
