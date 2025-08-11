from abc import ABC
from typing import Generic, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased, selectinload
from sqlalchemy.sql import literal_column, select

from .dto import BuildingDTO, CategoryDTO, OrganizationDTO
from .mappers import BuildingMapper, CategoryMapper, MapperType, OrganizationMapper
from .models import Building, Category, Organization
from .types_ import DTOType, ModelType

RepositoryType = TypeVar('RepositoryType', bound='BaseRepository')


class BaseRepository(ABC, Generic[ModelType, DTOType, MapperType]):
    model: type[ModelType]
    mapper: type[MapperType]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
    
    def _to_dto(self, obj: ModelType) -> DTOType:
        return self.mapper.to_dto(obj)
    
    def _from_dto(self, dto: DTOType) -> ModelType:
        return self.mapper.from_dto(dto)
    
    def create(self, dto: DTOType) -> ModelType:
        obj = self.model(**dto.model_dump())
        self.session.add(obj)

        return obj
    
    async def get(self, obj_id: int) -> DTOType | None:  # TODO Kwargs
        obj = await self.session.get(self.model, obj_id)
        return self._to_dto(obj) if obj is not None else None

    async def read(self) -> list[DTOType]:
        result = await self.session.scalars(
            select(self.model)
        )
        
        objects = result.all()

        return [self._to_dto(obj) for obj in objects]

    async def delete(self, obj_id: int) -> None:
        obj = await self.session.get(self.model, obj_id)
        await self.session.delete(obj)


class OrganizationsRepository(
        BaseRepository[Organization, OrganizationDTO, OrganizationMapper]
    ):
    model = Organization
    mapper = OrganizationMapper

    async def get_by_name(self, name: str) -> OrganizationDTO | None:
        org = await self.session.scalar(
            select(self.model).where(self.model.name == name)
        )
        return self._to_dto(org) if org else None

    async def get_by_building(self, building_id: int) -> list[OrganizationDTO]:
        result = await self.session.scalars(
            select(self.model).where(self.model.building_id==building_id)
        )

        organizations = result.all()

        return [self._to_dto(org) for org in organizations]

    async def get_by_category(self, category_id: int) -> list[OrganizationDTO]:
        stmt = (
            select(self.model)
            .join(self.model.categories)
            .where(Category.id == category_id)
        )
        result = await self.session.scalars(stmt)
        organizations = result.all()
        return [self._to_dto(org) for org in organizations]
    
    async def get_by_category_with_decendants(
            self,
            root_category_id: int,
            max_depth: int = 3
        ) -> list[OrganizationDTO]:
        category_alias = aliased(Category)

        base_cte = (
            select(
                Category.id.label('id'),
                literal_column('1').label('depth')
            )
            .where(Category.id == root_category_id)
            .cte(name='category_cte', recursive=True)
        )

        recursive_cte = base_cte.union_all(
            select(
                category_alias.id,
                (base_cte.c.depth + 1).label("depth")
            ).where(
                (category_alias.parent_id == base_cte.c.id) &
                (base_cte.c.depth < max_depth)
            )
        )

        stmt = (
            select(self.model)
            .join(self.model.categories)
            .where(Category.id.in_(select(recursive_cte.c.id)))
        )

        result = await self.session.scalars(stmt)
        organizations = result.all()
        return [self._to_dto(org) for org in organizations]


class BuildingRepository(
        BaseRepository[Building, BuildingDTO, BuildingMapper]
    ):
    model = Building
    mapper = BuildingMapper


class CategoryRepository(
        BaseRepository[Category, CategoryDTO, CategoryMapper]
    ):
    model = Category
    mapper = CategoryMapper
    
    async def get(self, obj_id: int) -> DTOType:
        result = await self.session.scalars(
            select(self.model)
            .options(selectinload(self.model.children))
            .where(self.model.id == obj_id)
        )
        obj = result.first()
        print(f'{obj = }')
        print(f'{obj.children = }')
        return self._to_dto(obj) if obj else None

    async def read(self) -> list[DTOType]:
        result = await self.session.scalars(
            select(self.model)
            .options(selectinload(Category.children))
        )
        
        objects = result.all()
        print(f'{objects = }')
        print(f'{objects[0].children = }')

        return [self._to_dto(obj) for obj in objects]
