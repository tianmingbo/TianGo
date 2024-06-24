from datetime import datetime
import datetime
import typing
from pydantic import BaseModel, Field, validator, BaseConfig


def convert_datetime_to_realworld(dt: datetime.datetime) -> str:
    return dt.replace(tzinfo=datetime.timezone.utc).isoformat().replace("+00:00", "Z")


def convert_field_to_camel_case(string: str) -> str:
    return "".join(
        word if index == 0 else word.capitalize()
        for index, word in enumerate(string.split("_"))
    )


class CommonSchema(BaseModel):
    class Config(BaseConfig):
        allow_population_by_field_name = True
        json_encoders = {datetime.datetime: convert_datetime_to_realworld}


class DBSchema(CommonSchema):
    class Config(CommonSchema.Config):
        orm_mode = True


class DateTimeModelMixin(BaseModel):
    created_at: datetime.datetime = None  # type: ignore
    updated_at: datetime.datetime = None  # type: ignore

    @validator("created_at", "updated_at", pre=True)
    def default_datetime(
            cls,  # noqa: N805
            value: datetime.datetime,  # noqa: WPS110
    ) -> datetime.datetime:
        return value or datetime.datetime.now()


class IDModelMixin(BaseModel):
    id_: int = Field(0, alias="id")


class RestModel(BaseModel):
    data: typing.Any = None  # noqa:WPS110
    code: int = 200
    msg: str = ""
    error: str = ""


class RestListModel(RestModel):
    total: int = -1
    pages: int = -1


class PageModel(BaseModel):
    per_page: int = Field(20, ge=1)
    page: int = Field(1, ge=1)


class CreateSuccessSchema(RestModel):
    msg: str = "success"


class DeleteSuccessSchema(RestModel):
    msg: str = "success"
