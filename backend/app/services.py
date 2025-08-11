from abc import ABC
from typing import Generic, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from .dto import BuildingDTO, CategoryDTO, OrganizationDTO
from .mappers import BuildingMapper, CategoryMapper, MapperType, OrganizationMapper
from .repositories import (
    BuildingRepository,
    CategoryRepository,
    OrganizationsRepository,
    RepositoryType,
)
from .types_ import DTOType

ServiceType = TypeVar('ServiceType', bound='BaseService')


class BaseService(ABC, Generic[RepositoryType, DTOType]):
    repository_class: type[RepositoryType]
    mapper: type[MapperType]

    def __init__(self, session: AsyncSession, repository: RepositoryType) -> None:
        self.session = session
        self.repository = repository
    
    async def create(self, dto: DTOType) -> DTOType:
        obj = self.repository.create(dto)
        await self.session.commit()
        await self.session.refresh(obj)
        return self.repository.mapper.to_dto(obj)
    
    async def get(self, obj_id: int) -> DTOType:
        dto = await self.repository.get(obj_id)
        return dto

    async def read(self) -> list[DTOType]:
        return await self.repository.read()

    async def delete(self, obj_id: int) -> None:
        await self.repository.delete(obj_id)
        await self.session.commit()


class OrganizationService(BaseService[OrganizationsRepository, OrganizationDTO]):
    repository_class = OrganizationsRepository
    mapper = OrganizationMapper

    async def get_by_name(self, name: str) -> DTOType | None:
        return await self.repository.get_by_name(name)

    async def get_organizations_by_building(self, building_id: int) -> list[OrganizationDTO]:
        return await self.repository.get_by_building(building_id)

    async def get_organizations_by_category(self, category_id: int) -> list[OrganizationDTO]:
        return await self.repository.get_by_category(category_id)

    async def get_organizations_by_category_tree(self, category_id: int) -> list[OrganizationDTO]:
        return await self.repository.get_by_category_with_decendants(category_id)
    
    async def get_organizations_by_coordinates(self, coordiantes: str) -> list[OrganizationDTO]:
        pass


class BuildingService(BaseService[BuildingRepository, BuildingDTO]):
    repository_class = BuildingRepository
    mapper = BuildingMapper


class CategoryService(BaseService[CategoryRepository, CategoryDTO]):
    repository_class = CategoryRepository
    mapper = CategoryMapper
