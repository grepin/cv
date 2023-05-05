from http import HTTPStatus
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Security
from pydantic import parse_obj_as
import orjson

from core.view_decorators import url_cache
from services.films import get_service
from services.mixins import GetByIDService, ListService, SearchService
from api.v1.response_models import Film, FilmSummary
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import core.messages as messages
from services.cache import BaseCacheStorage, get_redis_cache_service, get_cache_key
from services.auth import AuthService, get_auth_service
from pydantic import parse_raw_as

router = APIRouter()
security = HTTPBearer(auto_error=False)


def token(bearer):
    return None if bearer is None else bearer.credentials


@router.get(
    "/",
    response_model=List[FilmSummary],
    summary="Получение списка кинопроизведений",
    description="Постраничный список известных сервису кинопроизведений в краткой форме",
    response_description="Название, идентификатор и IMDB-рейтинг фильма",
    tags=['Список кинопроизведений'],
)
@url_cache(expire=60)
async def films(
        sort: Optional[str] = Query(None),
        filter_genre: Optional[str] = Query(None, alias="filter[genre]"),
        page: Optional[int] = Query(1, alias="page[number]"),
        size: Optional[int] = Query(50, alias="page[size]"),
        film_service: ListService = Depends(get_service),
) -> List[FilmSummary]:
    films = await film_service.list(
        page_number=size,
        page_size=page,
        sort=sort,
        filter_genre=filter_genre,
    )
    if not films:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=messages.FILMS_NOT_FOUND
        )
    return parse_obj_as(List[FilmSummary], films)


@router.get(
    "/{film_id}",
    response_model=Film,
    summary="Получение сведений о конкретном кинопроизведении",
    description="Полный набор сведений о конкретном кинопроизвдении,"
                "включая сведения о жанрах, актерах и режиссерах",
    response_description="Название, описание, IMDB-рейтинг, актеры, режиссеры, жанры",
    tags=['Полная информация о кинопроизведении']
)
async def film_details(
        film_id: str,
        bearer: HTTPAuthorizationCredentials = Security(security),
        auth_check_service: AuthService = Depends(get_auth_service),
        cache_service: BaseCacheStorage = Depends(get_redis_cache_service),
        film_service: GetByIDService = Depends(get_service)
) -> Film:
    subscription = await auth_check_service.subscription(token(bearer))
    cache_key = get_cache_key('film_details', {'film_id': film_id}, subscription)
    film = await cache_service.get_data_from_cache(cache_key)
    if film is None:
        film = await film_service.get(film_id)
        if not film:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=messages.FILM_NOT_FOUND
            )
        await cache_service.set_data_to_cache(
            cache_key,
            orjson.dumps(film.dict()),
            expire=60
        )
    else:
        film = parse_raw_as(Film, film)
    if film.subscription > subscription:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail=messages.SUBSCRIPTION_NEEDED
        )
    return Film(**film.dict())


@router.get(
    "/search/",
    response_model=List[FilmSummary],
    summary="Поиск кинопроизведений",
    description="Поиск кинопроизведений по указанной строке " +
                "запроса с постраничным выводом результатов в краткой форме",
    response_description="Идентификатор фильма, название, и IMDB-рейтинг",
    tags=['Поиск кинопроизведения']
)
@url_cache(expire=60)
async def search_films(
        query: Optional[str] = Query(None),
        page: Optional[int] = Query(1, alias="page[number]"),
        size: Optional[int] = Query(50, alias="page[size]"),
        film_service: SearchService = Depends(get_service),
) -> List[FilmSummary]:
    films = await film_service.search(
        string=query,
        page_number=size,
        page_size=page
    )
    if not films:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=messages.FILMS_NOT_FOUND
        )
    return parse_obj_as(List[FilmSummary], films)
