# -*- coding: utf-8 -*-
# @Time    : 2020/10/13 16:52
# @Author  : tmb
# -*- coding: utf-8 -*-
# @Time    : 2020/10/13 16:27
# @Author  : tmb
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root:tian@127.0.0.1:3306/douyin", max_overflow=5)

Base = declarative_base()


#
# class UserInfo(Base):
#     __tablename__ = 'UserInfo'
#     id = Column(Integer, primary_key=True)
#     avatar_image = Column(String(128))
#     nickname = Column(String(128))
#     signature = Column(String(128))
#     following_count = Column(Integer)  # 关注
#     fans = Column(Integer)  # 粉丝
#     zan = Column(Integer)  # 赞
#     works_count = Column(Integer)  # 作品
#     favoriting_count = Column(Integer)  # 喜欢
#     douyin_id = Column(String(32), nullable=False)


class CaiHongPI(Base):
    __tablename__ = 'caihongpi'
    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(String(256))


# 定义初始化数据库函数
def init_db():
    Base.metadata.create_all(engine)


# 顶固删除数据库函数
def drop_db():
    Base.metadata.drop_all(engine)


# drop_db()
init_db()
