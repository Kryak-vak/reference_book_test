from __future__ import annotations

from pydantic import BaseModel, Field


class PhoneNumberSchema(BaseModel):
    id: int | None
    number: str | None = None

    model_config = {
        "from_attributes": True,
    }


class BuildingSchema(BaseModel):
    id: int | None
    address: str
    coordinates: str

    model_config = {
        "from_attributes": True,
    }


class BuildingCreateSchema(BaseModel):
    address: str
    coordinates: str

    model_config = {
        "from_attributes": True,
    }


class CategorySchema(BaseModel):
    id: int | None
    name: str
    parent_id: int | None = None
    children: list['CategorySchema'] = Field(default_factory=list)

    model_config = {
        "from_attributes": True,
    }


class CategoryCreateSchema(BaseModel):
    name: str
    parent_id: int | None = None
    children: list['CategoryChildSchema'] = Field(default_factory=list)

    model_config = {
        "from_attributes": True,
    }


class CategoryChildSchema(BaseModel):
    id: int | None = None
    name: str | None = None
    children: list['CategoryChildSchema'] = Field(default_factory=list)

    model_config = {"from_attributes": True}


class OrganizationSchema(BaseModel):
    id: int | None
    name: str
    building: BuildingSchema | None = None
    phone_numbers: list[PhoneNumberSchema] = Field(default_factory=list)
    categories: list[CategorySchema] = Field(default_factory=list)

    model_config = {
        "from_attributes": True,
    }


class OrganizationCreateSchema(BaseModel):
    name: str
    building_id: int
    phone_numbers: list[str] = Field(default_factory=list)
    category_ids: list[int] = Field(default_factory=list)

    model_config = {
        "from_attributes": True,
    }