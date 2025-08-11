from fastapi import APIRouter, HTTPException

from app.schemas import CategoryCreateSchema, CategorySchema
from app.services import CategoryService

from ..deps import service_dep

router = APIRouter(
    prefix="/categories",
    tags=["categories"]
)


@router.post("/", response_model=CategorySchema)
async def create_category(
    category_in: CategoryCreateSchema,
    category_service: CategoryService = service_dep(CategoryService),
) -> CategorySchema:
    """
    Create new category.
    """
    category_dto_in = category_service.mapper.to_from_schema(
        category_in, category_service.mapper.dto_class
    )
    category_dto = await category_service.create(category_dto_in)
    category_schema = category_service.mapper.to_from_schema(category_dto)
    return category_schema


@router.get("/", response_model=list[CategorySchema])
async def read_categories(
    category_service: CategoryService = service_dep(CategoryService)
) -> list[CategorySchema]:
    """
        Retrieve categories.
    """
    category_dtos = await category_service.read()
    category_schemas: list[CategorySchema] = [
        category_service.mapper.to_from_schema(dto) for dto in category_dtos
    ]
    return category_schemas


@router.get("/{id}", response_model=CategorySchema)
async def get_category(
    id: int,
    category_service: CategoryService = service_dep(CategoryService),
) -> CategorySchema:
    """
    Get category by ID.
    """
    category_dto = await category_service.get(id)
    if not category_dto:
        raise HTTPException(status_code=404, detail="category not found")
    
    category_schema = category_service.mapper.to_from_schema(category_dto)
    return category_schema


@router.delete("/{id}")
async def delete_category(
    id: int,
    category_service: CategoryService = service_dep(CategoryService),
) -> dict[str, str]:
    """
    Delete an category.
    """
    await category_service.delete(id)
    return {"message": "category deleted successfully"}