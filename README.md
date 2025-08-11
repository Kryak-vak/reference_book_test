# Reference Book API

FastAPI backend with PostgreSQL and Docker.

## Features

- FastAPI + Uvicorn
- PostgreSQL
- SQLAlchemy + Alembic
- Docker + Docker Compose
- uv for dependency management

## API Endpoints

- GET	/api/v1/docs	                                               Swagger UI
- GET	/api/v1/redoc	                                               Redoc documentation
- GET	/api/v1/organizations/{id}	                                   Retrieve by id
- GET	/api/v1/organizations/by-name/{name}	                       Retrieve by name
- GET	/api/v1/organizations/by-building/{building_id}	               Retrieve by building
- GET	/api/v1/organizations/by-category/{category_id}	               Retrieve by category
- GET	/api/v1/organizations/by-category/{category_id}?tree=true	   Retrieve by category with tree traversal

## Running with Docker

1. Create a `.env` file in the root directory. Example:

```env
# Environment
ENVIRONMENT=local

PROJECT_NAME="reference book"

# Backend
SECRET_KEY=TOM6DsKO8yDpDnkZALllVrMWOqHgePug4lvhx_CnFjc
FIRST_SUPERUSER=fastapi_super
FIRST_SUPERUSER_PASSWORD=nxS6Z-KoAjI3W5J7hhXBD8ZZ5mrRKmF7sMSm6zioJDg

# Postgres
POSTGRES_SERVER=db
POSTGRES_PORT=5432
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

# Docker
DOCKER_IMAGE_BACKEND=backend
```

2. Run docker-compose up --build at project root