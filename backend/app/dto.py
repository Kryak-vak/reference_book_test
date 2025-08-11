from __future__ import annotations

from pydantic import BaseModel, Field


class BuildingDTO(BaseModel):
    id: int | None = None
    address: str
    coordinates: str

    model_config = {
        "from_attributes": True,
    }


class CategoryDTO(BaseModel):
    id: int | None = None
    name: str
    parent_id: int | None = None
    children: list['CategoryDTO'] = Field(default_factory=list)

    model_config = {
        "from_attributes": True,
    }


class OrganizationDTO(BaseModel):
    id: int | None = None
    name: str
    building_id: int
    phone_numbers: list[str] = Field(default_factory=list)
    categories: list[CategoryDTO] = Field(default_factory=list)

    model_config = {
        "from_attributes": True,
    }