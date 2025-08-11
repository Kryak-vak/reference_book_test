from typing import TypeVar

from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase

ModelType = TypeVar('ModelType', bound=DeclarativeBase)
DTOType = TypeVar('DTOType', bound=BaseModel)
SchemaType = TypeVar('SchemaType', bound=BaseModel)