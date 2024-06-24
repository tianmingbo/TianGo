import datetime
from typing import Any, Type

from pydantic import create_model
from sqlalchemy.orm import InstrumentedAttribute
from sqlalchemy.sql import sqltypes


from .base_schema import RestModel, RestListModel, DBSchema

from math import ceil


async def pagination(db, base_section, count, per_page: int, page: int) -> (list, int, int):
    """
    获取分页相关字段
    """
    query_list = (await db.execute(base_section.limit(per_page).offset(per_page * (page - 1)))).scalars().all()

    if page == 1 and len(query_list) < per_page:
        total = len(query_list)

    else:
        total = count

    pages = int(ceil(total / float(per_page)))

    return query_list, pages, total


def type_mapping(tp: sqltypes) -> Type:
    """类型映射"""
    match tp:
        case sqltypes.String:
            return str
        case sqltypes.Integer | sqltypes.INTEGER | sqltypes.BigInteger | sqltypes.BIGINT | sqltypes.INT:
            return int
        case sqltypes.FLOAT | sqltypes.Float:
            return float
        case sqltypes.BOOLEAN | sqltypes.Boolean:
            return bool
        case sqltypes.DATETIME | sqltypes.DateTime:
            return datetime.datetime
        case sqltypes.Date | sqltypes.Date:
            return datetime.date
        case sqltypes.JSON:
            return Any
        case _:
            pass


class _SqlalchemyModelToSchemaModel:
    """根据orm自动生成pydantic模型"""

    __REQUEST_CREATE_SCHEMA = None
    __REQUEST_UPDATE_SCHEMA = None
    __RESPONSE_ONE_SCHEMA = None
    __RESPONSE_LIST_SCHEMA = None
    __RESPONSE_ALL_SCHEMA = None

    class Config:
        orm_mode = True

    @classmethod
    def get_table_field(cls) -> dict:
        """获取所有表字段"""
        return {attr: cls.__dict__[attr] for attr in cls.__dict__ if
                isinstance(cls.__dict__[attr], InstrumentedAttribute)}

    @classmethod
    def request_create_schema(cls):
        if not cls.__REQUEST_CREATE_SCHEMA:
            cls.__REQUEST_CREATE_SCHEMA = create_model(f"{cls.__name__}CreateInSchema", **cls.__get_db_in_dict(nullable=False))
        return cls.__REQUEST_CREATE_SCHEMA

    @classmethod
    def request_update_schema(cls):
        if not cls.__REQUEST_UPDATE_SCHEMA:
            cls.__REQUEST_UPDATE_SCHEMA = create_model(f"{cls.__name__}UpdateInSchema", **cls.__get_db_in_dict(nullable=True))
        return cls.__REQUEST_UPDATE_SCHEMA

    @classmethod
    def response_one_schema(cls):
        """返回单个"""
        if not cls.__RESPONSE_ONE_SCHEMA:
            data_schema = create_model(
                f"{cls.__name__}ResponseOneDataSchema",
                __base__=DBSchema,
                **cls.__get_db_out_dict())
            cls.__RESPONSE_ONE_SCHEMA = create_model(
                f"{cls.__name__}ResponseOneSchema",
                __base__=RestModel,
                data=(data_schema, None)
            )
        return cls.__RESPONSE_ONE_SCHEMA

    @classmethod
    def response_list_schema(cls):
        """返回带分页的列表"""
        if not cls.__RESPONSE_LIST_SCHEMA:
            data_schema = create_model(
                f"{cls.__name__}ResponseListDataSchema",
                __base__=DBSchema,
                **cls.__get_db_out_dict())
            cls.__RESPONSE_LIST_SCHEMA = create_model(
                f"{cls.__name__}ResponseListSchema",
                __base__=RestListModel,
                data=(list[data_schema], list())
            )
        return cls.__RESPONSE_LIST_SCHEMA

    @classmethod
    def response_all_schema(cls):
        """返回列表"""
        if not cls.__RESPONSE_ALL_SCHEMA:
            data_schema = create_model(
                f"{cls.__name__}ResponseAllDataSchema",
                __base__=DBSchema,
                **cls.__get_db_out_dict())
            cls.__RESPONSE_ALL_SCHEMA = create_model(
                f"{cls.__name__}ResponseAllSchema",
                __base__=RestModel,
                data=(list[data_schema], None)
            )
        return cls.__RESPONSE_ALL_SCHEMA

    @classmethod
    def __get_db_in_dict(cls, nullable: bool = True) -> dict:
        model_construction = {}
        for name, attr in cls.get_table_field().items():
            if name.startswith("_"):
                continue

            if name.lower() == "id":
                continue

            if name.lower() in ["create_time", "update_time", "created_time", "updated_time"]:

                continue

            if not hasattr(attr, "type"):
                continue

            if not nullable and not attr.nullable:
                value = (type_mapping(type(attr.type)), ...)
            else:
                value = (type_mapping(type(attr.type)), None)
            model_construction[name] = value
        return model_construction

    @classmethod
    def __get_db_out_dict(cls):
        model_construction = {}
        for name, attr in cls.get_table_field().items():
            if name.startswith("_"):
                continue

            if name.lower() in ["password", "passwd"]:
                continue

            if not hasattr(attr, "type"):
                continue
            model_construction[name] = (type_mapping(type(attr.type)), None)
        return model_construction
