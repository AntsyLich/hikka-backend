from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session
from .schemas import AnimeSearchArgs
from app.errors import Abort
from fastapi import Depends
from typing import Tuple
from . import service


async def validate_search_anime(
    search: AnimeSearchArgs,
    session: AsyncSession = Depends(get_session),
) -> Tuple[AnimeSearchArgs, list, list, list]:
    producers = []
    studios = []
    genres = []

    # Check if provided producers exist
    if len(search.producers) > 0:
        producers = await service.company_count(session, search.producers)
        if len(producers) != len(search.producers):
            raise Abort("search", "unknown-producer")

    # Check if provided studios exist
    if len(search.studios) > 0:
        studios = await service.company_count(session, search.studios)
        if len(studios) != len(search.studios):
            raise Abort("search", "unknown-studio")

    # Check if provided genres exist
    if len(search.genres) > 0:
        genres = await service.anime_genre_count(session, search.genres)
        if len(genres) != len(search.genres):
            raise Abort("search", "unknown-genre")

    return search, producers, studios, genres
