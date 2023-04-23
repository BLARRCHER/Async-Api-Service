import uuid
from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from api.errors import NotFoundErrors
from api.v1.base import get_base_params, get_search_params
from models.base import Filter, ORJSONModel, QueryBase
from models.film import Film
from services.film import FilmService, get_film_service

router = APIRouter()


class ShortFilm(ORJSONModel):
    uuid: uuid.UUID
    title: Optional[str]
    imdb_rating: Optional[float] = 0


def get_filter_params(
        base_params: QueryBase = Depends(get_base_params),
        filter_value: Optional[str] = Query(
            default=None,
            alias="filter[genre]",
            description="поиск по жанру среди фильмов"
        ),
):
    base_params.filter = (
        Filter(field='genre', value=filter_value) if filter_value else None
    )
    return base_params


@router.get('/', response_model=list[ShortFilm],
            summary='Список фильмов',
            description='Список фильмов с пагинацией, '
                        'фильтрацией по жанрам и сортировкой по рейтингу',
            response_description='uuid, название и рейтинг')
async def many_films(
    params: QueryBase = Depends(get_filter_params),
    film_service: FilmService = Depends(get_film_service),
) -> list[ShortFilm]:
    try:
        film_list = await film_service.get_by_query(params=params)
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))
    return [
        ShortFilm(**film) for film in film_list or []
    ]


@router.get('/search', response_model=list[ShortFilm],
            summary='Поиск по фильмам',
            description='Поиск по фильмам',
            response_description='uuid, название и рейтинг')
async def search_films(
        params: QueryBase = Depends(get_search_params),
        film_service: FilmService = Depends(get_film_service),
) -> list[ShortFilm]:
    film_list = await film_service.get_by_query(params=params)
    return [
        ShortFilm(**film) for film in film_list or []
    ]


@router.get('/{film_id}',
            response_model=Optional[Film],
            summary='Подробная информация о фильме',
            description='Вывод подробной информации по uuid фильма',
            response_description='uuid, название, рейтинг, описание, жанры, '
                                 'актеры, сценаристы, режисcеры')
async def film_details(
        film_id: str,
        film_service: FilmService = Depends(get_film_service)
) -> Film:
    film = await film_service.get_by_id(film_id)

    if not film:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=NotFoundErrors.FILM_HAS_NOT_FOUND
        )
    return Film(**film)
