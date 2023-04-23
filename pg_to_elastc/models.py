from typing import Optional, List
from pydantic import BaseModel, validator
from pydantic.fields import Field


class UUIDModel(BaseModel):
    uuid: str = Field(alias='id')

class Genre(UUIDModel):
    name: str


class FullPerson(UUIDModel):
    full_name: str
    roles: list = []
    film_ids: list = []


class ShortPerson(UUIDModel):
    full_name: str


class Movies(UUIDModel):
    imdb_rating: Optional[float] = 0
    genre: Optional[List[Genre]] = Field(default_factory=list)
    title: str
    description: Optional[str] = None
    actors_names: Optional[List[str]] = Field(default_factory=list)
    writers_names: Optional[List[str]] = Field(default_factory=list)
    actors: Optional[List[ShortPerson]] = Field(default_factory=list)
    writers: Optional[List[ShortPerson]] = Field(default_factory=list)
    directors: Optional[List[ShortPerson]] = Field(default_factory=list)

    class Config:
        validate_assignment = True
