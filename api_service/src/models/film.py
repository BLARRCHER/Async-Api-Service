import uuid
from typing import Optional

from pydantic import Field

from models.base import ORJSONModel
from models.genre import Genre
from models.person import ShortPerson


class ShortFilm(ORJSONModel):
    uuid: uuid.UUID
    title: Optional[str]
    imdb_rating: Optional[float] = 0


class Film(ShortFilm):
    description: Optional[str]
    genre: Optional[list[Genre]] = Field(default_factory=list)
    actors: Optional[list[ShortPerson]] = Field(default_factory=list)
    writers: Optional[list[ShortPerson]] = Field(default_factory=list)
    directors: Optional[list[ShortPerson]] = Field(default_factory=list)
