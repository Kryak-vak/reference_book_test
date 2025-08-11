from fastapi import APIRouter, HTTPException

from app.schemas import OrganizationCreateSchema, OrganizationSchema
from app.services import OrganizationService

from ..deps import service_dep

router = APIRouter(
    prefix="/organizations",
    tags=["organizations"]
)


@router.post("/", response_model=OrganizationSchema)
async def create_organization(
    org_in: OrganizationCreateSchema,
    org_service: OrganizationService = service_dep(OrganizationService),
) -> OrganizationSchema:
    """
    Create new organization.
    """
    org_dto_in = org_service.mapper.to_from_schema(org_in, org_service.mapper.dto_class)
    org_dto = await org_service.create(org_dto_in)
    org_schema = org_service.mapper.to_from_schema(org_dto)
    return org_schema


@router.get("/", response_model=list[OrganizationSchema])
async def read_organizations(
    org_service: OrganizationService = service_dep(OrganizationService)
) -> list[OrganizationSchema]:
    """
        Retrieve organizations.
    """
    org_dtos = await org_service.read()
    org_schemas: list[OrganizationSchema] = [
        org_service.mapper.to_from_schema(dto) for dto in org_dtos
    ]
    return org_schemas


@router.get("/{id}", response_model=OrganizationSchema)
async def get_organization(
    id: int,
    org_service: OrganizationService = service_dep(OrganizationService),
) -> OrganizationSchema:
    """
    Get organization by ID.
    """
    org_dto = await org_service.get(id)
    if not org_dto:
        raise HTTPException(status_code=404, detail="organization not found")
    
    org_schema = org_service.mapper.to_from_schema(org_dto)
    return org_schema


@router.get("/by-name/{name}", response_model=OrganizationSchema)
async def get_organization_by_name(
    name: str,
    org_service: OrganizationService = service_dep(OrganizationService),
) -> OrganizationSchema:
    """
    Get organization by name.
    """
    org_dto = await org_service.get_by_name(name)
    if not org_dto:
        raise HTTPException(status_code=404, detail="organization not found")

    return org_service.mapper.to_from_schema(org_dto)


@router.get("/by-building/{building_id}", response_model=list[OrganizationSchema])
async def get_organizations_by_building(
    building_id: int,
    org_service: OrganizationService = service_dep(OrganizationService),
) -> list[OrganizationSchema]:
    """
    Get organizations by the specified building.
    """
    org_dtos = await org_service.get_organizations_by_building(building_id)
    org_schemas = [org_service.mapper.to_from_schema(dto) for dto in org_dtos]
    return org_schemas


@router.get("/by-category/{category_id}", response_model=list[OrganizationSchema])
async def get_by_category(
    category_id: int,
    tree: bool = False,
    org_service: OrganizationService = service_dep(OrganizationService),
) -> list[OrganizationSchema]:
    """
    Get organizations by the specified category. If `tree=true`, include descendant categories.
    """
    if tree:
        org_dtos = await org_service.get_organizations_by_category_tree(category_id)
    else:
        org_dtos = await org_service.get_organizations_by_category(category_id)
    
    org_schemas = [org_service.mapper.to_from_schema(dto) for dto in org_dtos]

    return org_schemas


@router.delete("/{id}")
async def delete_organization(
    id: int,
    org_service: OrganizationService = service_dep(OrganizationService),
) -> dict[str, str]:
    """
    Delete an organization.
    """
    await org_service.delete(id)
    return {"message": "organization deleted successfully"}