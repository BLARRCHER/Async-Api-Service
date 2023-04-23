import uuid
from enum import Enum

from pydantic import Field

from models.base import ORJSONModel

FilmIdType = uuid.UUID


class RoleTypeEnum(Enum):
    ACTOR = 'actor'
    WRITER = 'writer'
    DIRECTOR = 'director'


class ShortPerson(ORJSONModel):
    uuid: uuid.UUID
    full_name: str


class Person(ShortPerson):
    roles: list[RoleTypeEnum] = Field(default_factory=list)
    film_ids: list[FilmIdType]
