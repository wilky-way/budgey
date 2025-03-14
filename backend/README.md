# Budgey Backend API

The Backend API provides RESTful endpoints to access the YNAB data stored in the PostgreSQL database. It serves as the data access layer for the Budgey frontend and any other clients.

## Architecture

The Backend API is built with FastAPI, a modern, high-performance web framework for building APIs with Python 3.13. It follows a layered architecture:

- **API Layer**: REST endpoints organized by resource
- **Service Layer**: Business logic and data processing
- **Data Access Layer**: Database interactions using SQLAlchemy

## Key Features

- **RESTful API**: Clean, consistent API design following REST principles
- **OpenAPI Documentation**: Auto-generated API documentation with Swagger UI
- **Type Safety**: Leverages Python type hints and Pydantic for validation
- **Efficient Queries**: Optimized database queries with SQLAlchemy
- **Authentication**: Secure API access (to be implemented)

## Directory Structure

```
backend/
├── Dockerfile          # Container definition
├── requirements.txt    # Python dependencies
├── app/
│   ├── __init__.py
│   ├── main.py         # Application entry point
│   ├── api/            # API endpoints
│   │   ├── __init__.py
│   │   └── api_v1/     # API version 1
│   │       ├── __init__.py
│   │       ├── api.py  # API router
│   │       └── endpoints/  # Resource endpoints
│   │           ├── __init__.py
│   │           ├── budgets.py
│   │           └── ...
│   ├── core/           # Core configuration
│   │   └── config.py   # Settings
│   ├── db/             # Database
│   │   └── session.py  # DB session
│   ├── models/         # SQLAlchemy models
│   │   ├── __init__.py
│   │   └── budget.py
│   ├── schemas/        # Pydantic schemas
│   │   ├── __init__.py
│   │   └── budget.py
│   └── services/       # Business logic
└── tests/              # Unit and integration tests
```

## API Endpoints

The API provides the following endpoints:

- `/api/v1/budgets`: Budget operations
- `/api/v1/accounts`: Account operations
- `/api/v1/categories`: Category operations
- `/api/v1/transactions`: Transaction operations
- `/api/v1/payees`: Payee operations

## Configuration

The service is configured using environment variables:

- `DATABASE_URL`: PostgreSQL connection string
- `CORS_ORIGINS`: Allowed CORS origins

## Running the Service

### Using Docker

```bash
docker-compose up backend
```

### Standalone

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## API Documentation

When the service is running, you can access the auto-generated API documentation at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Development

To add new endpoints or modify existing ones:

1. Create or update the appropriate model in `app/models/`
2. Create or update the corresponding schema in `app/schemas/`
3. Implement the endpoint in `app/api/api_v1/endpoints/`
4. Register the endpoint in `app/api/api_v1/api.py`
5. Write tests in the `tests/` directory