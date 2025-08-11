from fastapi import APIRouter

from .routes import buildings, categories, organizations

api_router = APIRouter()
api_router.include_router(organizations.router)
api_router.include_router(buildings.router)
api_router.include_router(categories.router)