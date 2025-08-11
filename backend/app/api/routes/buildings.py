from fastapi import APIRouter, HTTPException

from app.schemas import BuildingCreateSchema, BuildingSchema
from app.services import BuildingService

from ..deps import service_dep

router = APIRouter(
    prefix="/buildings",
    tags=["buildings"]
)


@router.post("/", response_model=BuildingSchema)
async def create_building(
    building_in: BuildingCreateSchema,
    building_service: BuildingService = service_dep(BuildingService),
) -> BuildingSchema:
    """
    Create new building.
    """
    building_dto_in = building_service.mapper.to_from_schema(
        building_in, building_service.mapper.dto_class
    )
    building_dto = await building_service.create(building_dto_in)
    building_schema = building_service.mapper.to_from_schema(building_dto)
    return building_schema


@router.get("/", response_model=list[BuildingSchema])
async def read_buildings(
    building_service: BuildingService = service_dep(BuildingService)
) -> list[BuildingSchema]:
    """
        Retrieve buildings.
    """
    building_dtos = await building_service.read()
    building_schemas: list[BuildingSchema] = [
        building_service.mapper.to_from_schema(dto) for dto in building_dtos
    ]
    return building_schemas


@router.get("/{id}", response_model=BuildingSchema)
async def get_building(
    id: int,
    building_service: BuildingService = service_dep(BuildingService),
) -> BuildingSchema:
    """
    Get building by ID.
    """
    building_dto = await building_service.get(id)
    if not building_dto:
        raise HTTPException(status_code=404, detail="building not found")
    
    building_schema = building_service.mapper.to_from_schema(building_dto)
    return building_schema


@router.delete("/{id}")
async def delete_building(
    id: int,
    building_service: BuildingService = service_dep(BuildingService),
) -> dict[str, str]:
    """
    Delete an building.
    """
    await building_service.delete(id)
    return {"message": "building deleted successfully"}