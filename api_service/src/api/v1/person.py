from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from api.errors import NotFoundErrors
from api.v1.base import get_base_params, get_search_params
from models.base import QueryBase
from models.film import ShortFilm
from models.person import Person
from services.film import get_film_service
from services.person import PersonService, get_person_service

router = APIRouter()


@router.get('/', response_model=list[Person],
            summary='Список участников съемочных групп',
            description='Список участников съемочных групп '
                        'с пагинацией и сортировкой по имени',
            response_description='uuid, имя, профессия и список фильмов')
async def get_persons(
        params: QueryBase = Depends(get_base_params),
        person_service: PersonService = Depends(get_person_service)
) -> list[Person]:
    person_list = await person_service.get_by_query(params=params)
    return [Person(**person) for person in person_list or []]


@router.get('/search', response_model=list[Person],
            summary='Поиск по участникам',
            description='Поиск по участникам',
            response_description='uuid, имя, профессия и список фильмов')
async def search_persons(
        params: QueryBase = Depends(get_search_params),
        person_service: PersonService = Depends(get_person_service)
) -> list[Person]:
    person_list = await person_service.get_by_query(params=params)
    return [Person(**person) for person in person_list or []]


@router.get('/{person_id}', response_model=Person,
            summary='Информация о персоне',
            description='Вывод подробной информации о конкретном человеке',
            response_description='uuid, имя, профессия и список фильмов')
async def person_detail(
        person_id: str,
        person_service: PersonService = Depends(get_person_service)
) -> Person:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=NotFoundErrors.PERSON_HAS_NOT_FOUND
        )
    return Person(**person)


@router.get('/{person_id}/film', response_model=list[ShortFilm],
            summary='Фильмы персоны',
            description='Вывод информации о фильмах конкретного человека',
            response_description='uuid, название и рейтинг')
async def film_by_person(
        person_id: str,
        person_service: PersonService = Depends(get_person_service),
        film_service: PersonService = Depends(get_film_service)
) -> list[ShortFilm]:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=NotFoundErrors.PERSON_HAS_NOT_FOUND
        )
    result = [
        await film_service.get_by_id(film_id)
        for film_id in person['film_ids']
        if film_id is not None
    ]
    return [ShortFilm(**i) for i in result if i is not None]
