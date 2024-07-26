from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from app.dependencies import auth_required, get_page, get_size
from app.utils import pagination, pagination_dict
from app.schemas import ClientResponse
from app.database import get_session
from app.models import Client, User
from app.client import service
from app import constants

from app.client.dependencies import (
    validate_client_create,
    validate_user_client,
    validate_client,
)
from app.client.schemas import (
    ClientPaginationResponse,
    ClientFullResponse,
    ClientCreate,
    ClientUpdate,
)

router = APIRouter(prefix="/client", tags=["Client"])


@router.get(
    "/", summary="List user clients", response_model=ClientPaginationResponse
)
async def list_user_clients(
    page: int = Depends(get_page),
    size: int = Depends(get_size),
    session: AsyncSession = Depends(get_session),
    user: User = Depends(auth_required()),
):
    limit, offset = pagination(page, size)

    total = await service.count_user_clients(session, user, offset, limit)
    clients = await service.list_user_clients(session, user, offset, limit)

    return {
        "pagination": pagination_dict(total, page, limit),
        "list": clients.all(),
    }


@router.get(
    "/{client_reference}",
    summary="Get client by reference",
    response_model=ClientResponse,
)
async def get_client_by_reference(client: Client = Depends(validate_client)):
    return client


@router.get(
    "/{client_reference}/full",
    summary="Get user full client by reference",
    response_model=ClientFullResponse,
)
async def get_user_client(client: Client = Depends(validate_user_client)):
    return client


@router.post(
    "/", summary="Create new user client", response_model=ClientFullResponse
)
async def create_user_client(
    create: ClientCreate = Depends(validate_client_create),
    session: AsyncSession = Depends(get_session),
    user: User = Depends(
        auth_required(permissions=[constants.PERMISSION_CLIENT_CREATE])
    ),
):
    return await service.create_user_client(session, user, create)


@router.put(
    "/{client_reference}",
    summary="Update user client",
    response_model=ClientFullResponse,
    dependencies=[
        Depends(auth_required(permissions=[constants.PERMISSION_CLIENT_UPDATE]))
    ],
)
async def update_user_client(
    update: ClientUpdate,
    session: AsyncSession = Depends(get_session),
    client: Client = Depends(validate_user_client),
):
    return await service.update_client(session, client, update)


@router.delete(
    "/{client_reference}",
    summary="Delete user client",
    response_model=ClientFullResponse,
    dependencies=[
        Depends(auth_required(permissions=[constants.PERMISSION_CLIENT_DELETE]))
    ],
)
async def delete_user_client(
    session: AsyncSession = Depends(get_session),
    client: Client = Depends(validate_user_client),
):
    return await service.delete_client(session, client)
