from enum import Enum


class NotFoundErrors(str, Enum):
    FILM_HAS_NOT_FOUND = 'film has not found'
    GENRE_HAS_NOT_FOUND = 'genre has not found'
    PERSON_HAS_NOT_FOUND = 'person has not found'
