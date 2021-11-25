# -*- coding: utf-8 -*-
# @Time    : 2020/10/13 17:39
# @Author  : tmb
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root:tian@127.0.0.1:3306/douyin", max_overflow=5)
# 创建mysql操作对象
Session = sessionmaker(bind=engine)
session = Session()
