import uuid

from models.base import ORJSONModel


class Genre(ORJSONModel):
    uuid: uuid.UUID
    name: str
