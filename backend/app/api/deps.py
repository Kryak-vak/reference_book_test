from collections.abc import AsyncGenerator
from functools import partial
from typing import Annotated, Type

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.db import AsyncSessionLocal
from ..services import ServiceType


async def get_session() -> AsyncGenerator[AsyncSession, None, None]:
    async with AsyncSessionLocal() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_service(service_cls: Type[ServiceType], session: SessionDep) -> ServiceType:
    repository = service_cls.repository_class(session)
    return service_cls(session, repository)


def service_dep(service_cls: Type[ServiceType]):
    return Depends(partial(get_service, service_cls))