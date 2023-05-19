from app.models import Anime, AnimeGenre, Company
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import AnimeSearchArgs
from sqlalchemy import select, func
from . import utils


async def company_count(session: AsyncSession, slugs: list[str]):
    companies = await session.scalars(
        select(Company.id).where(Company.slug.in_(slugs))
    )

    return companies.all()


async def anime_genre_count(session: AsyncSession, slugs: list[str]):
    genres = await session.scalars(
        select(AnimeGenre.id).where(AnimeGenre.slug.in_(slugs))
    )

    return genres.all()


def anime_search_where(
    search: AnimeSearchArgs, query, producers: list, studios: list, genres: list
):
    if search.years[0]:
        query = query.where(Anime.year >= search.years[0])

    if search.years[1]:
        query = query.where(Anime.year <= search.years[1])

    if len(search.season) > 0:
        query = query.where(
            Anime.season.in_(utils.enum_list_values(search.season))
        )

    if len(search.rating) > 0:
        query = query.where(
            Anime.rating.in_(utils.enum_list_values(search.rating))
        )

    if len(search.status) > 0:
        query = query.where(
            Anime.status.in_(utils.enum_list_values(search.status))
        )

    if len(search.source) > 0:
        query = query.where(
            Anime.source.in_(utils.enum_list_values(search.source))
        )

    if len(search.media_type) > 0:
        query = query.where(
            Anime.media_type.in_(utils.enum_list_values(search.media_type))
        )

    if len(search.producers) > 0:
        query = query.join(Anime.producers).filter(
            Company.slug.in_(search.producers)
        )

    if len(search.studios) > 0:
        query = query.join(Anime.studios).filter(
            Company.slug.in_(search.studios)
        )

    if len(search.genres) > 0:
        query = query.join(Anime.genres).filter(
            AnimeGenre.slug.in_(search.genres)
        )

    return query


async def anime_search(
    session: AsyncSession,
    limit: int,
    offset: int,
    search: AnimeSearchArgs,
    producers: list,
    studios: list,
    genres: list,
):
    query = select(Anime)
    query = anime_search_where(search, query, producers, studios, genres)

    if len(search.sort) > 0:
        query = query.order_by(*utils.build_order_by(search.sort))

    query = query.limit(limit).offset(offset)

    return await session.scalars(query)


async def anime_search_total(
    session: AsyncSession,
    search: AnimeSearchArgs,
    producers: list,
    studios: list,
    genres: list,
):
    query = select(func.count(Anime.id))
    query = anime_search_where(search, query, producers, studios, genres)

    return await session.scalar(query)
