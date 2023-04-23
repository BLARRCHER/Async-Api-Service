from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from api.errors import NotFoundErrors
from api.v1.base import get_base_params
from models.base import QueryBase
from models.genre import Genre
from services.genre import GenreService, get_genre_service

router = APIRouter()


@router.get('/', response_model=list[Genre], summary='Список жанров',
            description='Список жанров',
            response_description='uuid, название')
async def get_genres(
        params: QueryBase = Depends(get_base_params),
        genre_service: GenreService = Depends(get_genre_service)
) -> list[Genre]:
    genre_list = await genre_service.get_by_query(params)
    return [Genre(**genre) for genre in genre_list or []]


@router.get('/{genre_id}',
            response_model=Genre, summary='Подробная информация о жанре',
            description='Вывод подробной информации о жанре',
            response_description='uuid, название, описание')
async def genre_detail(
        genre_id: str, genre_service: GenreService = Depends(get_genre_service)
) -> Genre:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=NotFoundErrors.GENRE_HAS_NOT_FOUND
        )
    return Genre(**genre)
