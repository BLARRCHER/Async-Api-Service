import random

from fastapi import status
import pytest

from src.api.errors import NotFoundErrors


pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    'params, expected_answer',
    [

        (
            {'page[number]': 1, 'page[size]': 10},
            {'status': status.HTTP_200_OK, 'length': 10}
        ),
        (
            {'page[number]': 2, 'page[size]': 5},
            {'status': status.HTTP_200_OK, 'length': 5}
        ),
        (
            {'page[number]': 3, 'page[size]': 10},
            {'status': status.HTTP_200_OK, 'length': 0}
        ),
        # поля с ошибками
        (
            {'page[number]': -1, 'page[size]': -10},
            {'status': status.HTTP_422_UNPROCESSABLE_ENTITY, 'length': 1}
        ),
        (
            {'page[random_field]': 1, 'page[size]': -10},
            {'status': status.HTTP_422_UNPROCESSABLE_ENTITY, 'length': 1}
        ),
    ]
)
async def test_films_pagination(
    load_films_to_es,
    gen_film_data,
    make_get_request,
    clear_redis_cache,
    api_films_v1_base_url,
    params,
    expected_answer
):
    await load_films_to_es(gen_film_data())

    response = await make_get_request(api_films_v1_base_url, params=params)

    assert len(response.body) == expected_answer['length']
    assert response.status == expected_answer['status']


@pytest.mark.parametrize(
    'params, is_reverse',
    [
        (
            {'sort': '-imdb_rating'},
            True

        ),
        (
            {'sort': 'imdb_rating'},
            False
        )
    ]
)
async def test_films_sorting(
    load_films_to_es,
    gen_film_data,
    make_get_request,
    clear_redis_cache,
    api_films_v1_base_url,
    params,
    is_reverse
):
    generated_films = gen_film_data()

    ratings = []

    for i, film in enumerate(generated_films):
        rating = float(random.randint(1, 9))
        film['imdb_rating'] = rating
        ratings.append(rating)

    await load_films_to_es(generated_films)

    sorted_by_rating = sorted(ratings, reverse=is_reverse)

    response = await make_get_request(api_films_v1_base_url, params=params)

    assert response.status == status.HTTP_200_OK
    assert sorted_by_rating == [i['imdb_rating'] for i in response.body]


async def test_films_sorting_on_non_existed_field(
    prepare_films_from_testdata,
    make_get_request,
    clear_redis_cache,
    api_films_v1_base_url,
):
    params = {'sort': 'non_existed_field'}

    response = await make_get_request(api_films_v1_base_url, params=params)

    assert response.status == status.HTTP_400_BAD_REQUEST


@pytest.mark.parametrize(
    'params, expected_answer',
    [
        (
            {'filter[genre]': 'Documentary'},
            {'status': status.HTTP_200_OK, 'length': 2}
        ),
        (
            {'filter[genre]': 'Reality-TV'},
            {'status': status.HTTP_200_OK, 'length': 1}
        ),
    ]
)
async def test_films_by_filter(
    prepare_films_from_testdata,
    make_get_request,
    clear_redis_cache,
    api_films_v1_base_url,
    params,
    expected_answer
):
    response = await make_get_request(api_films_v1_base_url, params=params)

    assert response.status == expected_answer['status']
    assert len(response.body) == expected_answer['length']


async def test_film_by_id(
    prepare_films_from_testdata,
    make_get_request,
    clear_redis_cache,
    api_film_by_id_v1_url,
    film_id
):
    response = await make_get_request(
        api_film_by_id_v1_url.format(film_id=film_id))

    assert response.status == status.HTTP_200_OK
    assert response.body['uuid'] == str(film_id)


async def test_film_has_not_found(
    prepare_films_from_testdata,
    make_get_request,
    clear_redis_cache,
    api_film_by_id_v1_url,
):
    response = await make_get_request(
        api_film_by_id_v1_url.format(film_id='fake_uid'))

    assert response.body['detail'] == NotFoundErrors.FILM_HAS_NOT_FOUND
    assert response.status == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize(
    'params, expected_answer',
    [
        (
            {'query': 'star'},
            {'status': status.HTTP_200_OK, 'length': 2}
        ),
        (
            {'query': 'exploring'},
            {'status': status.HTTP_200_OK, 'length': 1}
        ),
        (
            {'query': 'potato'},
            {'status': status.HTTP_200_OK, 'length': 0}
        ),
    ]
)
async def test_search(
    prepare_films_from_testdata,
    make_get_request,
    clear_redis_cache,
    api_film_by_query_v1_url,
    params,
    expected_answer
):
    response = await make_get_request(api_film_by_query_v1_url, params=params)

    assert len(response.body) == expected_answer['length']
    assert response.status == expected_answer['status']
