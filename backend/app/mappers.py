from abc import ABC
from typing import Generic, TypeVar

from pydantic import BaseModel

from .dto import BuildingDTO, CategoryDTO, OrganizationDTO
from .models import Building, Category, Organization
from .schemas import BuildingSchema, CategorySchema, OrganizationSchema
from .types_ import DTOType, ModelType, SchemaType

MapperType = TypeVar('MapperType', bound='BaseMapper')


class BaseMapper(ABC, Generic[ModelType, DTOType, SchemaType]):
    model: type[ModelType]
    dto_class: type[DTOType]
    default_schema_class: type[SchemaType]
    
    @classmethod
    def to_dto(cls, obj: ModelType) -> DTOType:
        return cls.dto_class.model_validate(obj)
    
    @classmethod
    def from_dto(cls, dto: DTOType) -> ModelType:
        return cls.model(**dto.model_dump())
    
    @classmethod
    def to_from_schema(
            cls,
            data_model_in: BaseModel,
            data_model_out: type[BaseModel] | None = None
        ) -> BaseModel:
        if data_model_out is None:
            data_model_out = cls.default_schema_class
        
        return data_model_out.model_validate(data_model_in.model_dump())


class OrganizationMapper(BaseMapper[Organization, OrganizationDTO, OrganizationSchema]):
    model = Organization
    dto_class = OrganizationDTO
    default_schema_class = OrganizationSchema



class BuildingMapper(BaseMapper[Building, BuildingDTO, BuildingSchema]):
    model = Building
    dto_class = BuildingDTO
    default_schema_class = BuildingSchema


class CategoryMapper(BaseMapper[Category, CategoryDTO, CategorySchema]):
    model = Category
    dto_class = CategoryDTO
    default_schema_class = CategorySchema
