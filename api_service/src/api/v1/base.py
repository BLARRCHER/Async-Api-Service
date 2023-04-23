from typing import Optional

from fastapi import Depends, Query, Request

from models.base import Page, QueryBase


def get_base_params(
        request: Request,
        sort: Optional[str] = Query(
            default=None,
            description="сортировка по конкретному полю asc/desc"
        ),
        page_size: Optional[int] = Query(
            default=50, alias="page[size]", ge=1,
            description="кол-во элементов пагинации"
        ),
        page_num: Optional[int] = Query(
            default=1, alias="page[number]", ge=1,
            description="страница пагинации"
        )
):
    return QueryBase(
        sort=sort,
        page=Page(size=page_size, number=page_num),
        url=str(request.url.path)
    )


def get_search_params(
        query: Optional[str] = Query(
            default=None,
            description="поиск по ключевому слову"
        ),
        base_params: QueryBase = Depends(get_base_params),
):
    base_params.query = query
    return base_params
