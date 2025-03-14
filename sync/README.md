# Budgey Sync Service

The Sync Service is responsible for fetching data from the YNAB API and storing it in the PostgreSQL database. It serves as the data integration layer of the Budgey platform.

## Architecture

The Sync Service is built with Python 3.13 and uses the official YNAB SDK to interact with the YNAB API. It follows a service-oriented architecture with the following components:

- **Main Module**: Entry point that schedules and orchestrates the sync process
- **YNAB Service**: Handles API communication with rate limiting and error handling
- **Database Service**: Manages database operations and schema updates

## Key Features

- **Delta Sync**: Uses YNAB's server_knowledge parameter to fetch only changed data
- **Rate Limiting**: Respects YNAB's 200 requests/hour limit with retry mechanisms
- **Comprehensive Data Model**: Syncs all YNAB entities (budgets, accounts, categories, transactions, etc.)
- **Error Handling**: Robust error handling with logging and retries

## Directory Structure

```
sync/
├── Dockerfile          # Container definition
├── pyproject.toml      # Poetry project definition and dependencies
├── poetry.lock         # Poetry lock file (dependency resolution)
├── src/
│   ├── main.py         # Entry point
│   ├── models/         # Data models
│   ├── services/       # Service classes
│   │   ├── __init__.py
│   │   ├── db_service.py    # Database operations
│   │   └── ynab_service.py  # YNAB API interactions
│   └── utils/          # Utility functions
└── tests/              # Unit and integration tests
```

## Configuration

The service is configured using environment variables:

- `YNAB_PERSONAL_ACCESS_TOKEN`: Your YNAB API personal access token
- `DATABASE_URL`: PostgreSQL connection string

## Running the Service

### Using Docker

```bash
docker-compose up sync
```

### Standalone

```bash
cd sync
# Install Poetry if not already installed
# pip install poetry
poetry install
poetry run python -m src.main
```

## Development

To add new features or modify the sync service:

1. Update the appropriate service class in `src/services/`
2. Add any new models in `src/models/`
3. Write tests in the `tests/` directory
4. Run tests before submitting changes

### Managing Dependencies

This project uses Poetry for dependency management:

```bash
# Add a new dependency
poetry add package-name

# Add a development dependency
poetry add --dev package-name

# Update dependencies
poetry update

# Generate requirements.txt (if needed)
poetry export -f requirements.txt > requirements.txt
```

## Sync Process

1. Initial sync fetches all data from YNAB
2. Subsequent syncs use delta updates to minimize API calls
3. Data is stored in PostgreSQL with the same structure as YNAB
4. Server knowledge is tracked to enable efficient delta syncs