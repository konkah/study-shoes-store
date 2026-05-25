# Study Shoes Store

author: Karlos Helton Braga

## Setup

Before running the project for the first time, copy the environment variables template:

```bash
cp env/.env.example env/.env
```

Edit `env/.env` with your values. The default values in the file work out of the box for local development.

## How to run the project

```bash
# Build and start (blocking terminal)
docker compose up --build

# Build and start in background
docker compose up --build -d

# Start without rebuilding (after first build)
docker compose up -d

# View logs of all services (when running in background)
docker compose logs -f

# View logs of a specific service
docker compose logs -f web

# Stop containers
docker compose stop

# Stop and remove containers, images and volumes
docker compose down --rmi all --volumes
```

### Docker Volume Configuration

The project uses Docker volumes for **live code reloading** during development:
- `./study_shoes_store` → `/var/www/study_shoes_store` (app code)
- `./env` → `/var/www/env` (environment configuration)

This enables:
- ✅ Instant code reloading without rebuild
- ✅ Direct access to generated migration files
- ✅ Real-time test execution
- ✅ No file copying needed between container and host

### Single container (manual Docker)

```bash
# Build the image
docker build . -f shoes-store.Dockerfile -t study_shoes_store --network=host

# Run a single container in background
docker run --name shoes-store -p 8000:8000 -d study_shoes_store

# Run a single container (blocking terminal)
docker run --name shoes-store -p 8000:8000 -it study_shoes_store

# Stop a single container
docker stop shoes-store

# Restart a stopped container
docker start shoes-store

# Remove a stopped container
docker rm shoes-store

# Force remove a running container
docker rm -f shoes-store

# Remove the image
docker rmi study_shoes_store

# Force remove the image (even if used by a container)
docker rmi -f study_shoes_store
```

### Docker inspection and cleanup

```bash

# List running containers (name, image, status, ports)
docker ps

# List all containers including stopped ones
docker ps -a

# Show detailed info of a container (network, ports, mounts, etc.)
docker inspect <container_name>

# List networks
docker network ls

# Remove all stopped containers, unused networks and dangling images
docker system prune

# Remove all unused images (not just dangling ones)
docker system prune -a

# Remove all unused images, networks, containers and volumes
docker system prune -a --volumes
```

## Django management commands

All management commands must be run inside the running container:

```bash
# Apply pending migrations
docker compose exec web python manage.py migrate

# Generate migrations after changing models
docker compose exec web python manage.py makemigrations shoes_api --name <migration_name>

# Open a Django shell
docker compose exec web python manage.py shell

# Create a superuser manually
docker compose exec web python manage.py createsuperuser
```

> **Note:** With Docker volumes enabled, migration files are generated directly on the host. No copying needed!

## Running tests

All tests are written using Django's `TestCase` and DRF's `APITestCase`. Tests cover:
- **CPF validation**: Valid CPF acceptance, invalid CPF rejection, formatting, uniqueness
- **Order calculations**: Total value calculation from product values
- **API authentication**: Endpoint protection and authentication requirements

```bash
# Run all tests
docker compose exec web python manage.py test

# Run tests for shoes_api app only
docker compose exec web python manage.py test shoes_api

# Run a specific test class
docker compose exec web python manage.py test shoes_api.tests.ClientSerializerTestCase

# Run a specific test method
docker compose exec web python manage.py test shoes_api.tests.ClientSerializerTestCase.test_valid_cpf_accepted

# Run with verbose output (v=2 shows test method names)
docker compose exec web python manage.py test shoes_api -v 2

# Run tests with coverage report
docker compose exec web pip install coverage
docker compose exec web coverage run --source='shoes_api' manage.py test shoes_api
docker compose exec web coverage report
```

## Manual lint (Ruff)

Run lint before opening a PR, after refactors, or whenever you change files in `shoes_api/`.

The commands below are executed inside the running `web` container and use the same working directory, target, and flags as CI (excluding migrations):

```bash
# 1) Auto-fix lint issues (when possible)
docker compose exec web sh -lc "cd /var/www/study_shoes_store && ruff check shoes_api --select=E,W,F --exclude=shoes_api/migrations --fix"

# 2) Apply formatting
docker compose exec web sh -lc "cd /var/www/study_shoes_store && ruff format shoes_api --exclude=shoes_api/migrations"

# 3) Validate lint without changing files
docker compose exec web sh -lc "cd /var/www/study_shoes_store && ruff check shoes_api --select=E,W,F --exclude=shoes_api/migrations"

# 4) Validate formatting without changing files
docker compose exec web sh -lc "cd /var/www/study_shoes_store && ruff format shoes_api --check --exclude=shoes_api/migrations"
```

If CI shows Ruff errors while local lint passes, verify that lint-related changes were committed and pushed before running the workflow, then re-run CI on the latest commit SHA.

## Continuous Integration (CI/CD)

**Status:** ⏸️ Temporarily paused

A GitHub Actions workflow has been configured at `.github/workflows/tests.yml` with the following jobs:
- **setup**: Install dependencies
- **lint**: Code style checks (ruff)
- **security**: Security scanning (bandit)
- **test**: Run test suite and generate coverage reports

Each job is implemented as a reusable custom action in `.github/actions/`.

**Current limitation:** GitHub-hosted runners are disabled for this repository (GitHub Enterprise restriction). To enable CI/CD automation:
1. Contact your GitHub Enterprise Administrator
2. Request to enable "GitHub-hosted runners" for this repository
3. Once enabled, uncomment the `push` and `pull_request` triggers in `.github/workflows/tests.yml`

Alternatively, a self-hosted runner can be configured on your own infrastructure.

## Code Quality Improvements

This project implements systematic code quality improvements:

| # | Improvement | Details |
|---|---|---|
| 1 | Environment Management | `python-decouple` for secure config from `.env` |
| 2 | Authentication | Explicit `SessionAuthentication` + `BasicAuthentication` |
| 3 | WSGI Server | Production-ready `gunicorn` (replaces Django runserver) |
| 4 | Static Files | `WhiteNoise` middleware for CSS/JS serving |
| 5 | CSRF Security | `CSRF_TRUSTED_ORIGINS` from environment |
| 6 | Monetary Precision | `DecimalField` for `value` and `total_value` |
| 7 | Data Integrity | `unique=True` constraint on `Order.order_number` |
| 8 | Code Constants | `Product.COLOUR_CHOICES` class constant |
| 9 | CPF Formatting | `CPF().mask()` method for proper formatting |
| 10 | Calculation Logic | `sum()` generator for `Order.total_value` |
| 11 | Test Coverage | 15 comprehensive tests across serializers and API |
| 12 | API Documentation | Swagger/OpenAPI with `drf-spectacular` |
| 13 | CI/CD Pipeline | GitHub Actions with custom actions (setup, lint, security, test) |

**Test Results:** ✅ All 15 tests passing
- 4 tests: CPF validation, formatting, uniqueness
- 3 tests: Order total_value calculation
- 8 tests: API authentication requirements

## How to use the API

The API address is: http://127.0.0.1:8000.

Authentication is required to use the API. The user **admin** with password **admin** is created when the Docker container is built, to make it easier to interact with the API.

The authentication type used is Basic Authentication. You can understand how it works at the following link:

https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Authorization

For the credentials mentioned above, the `Authorization` header should have the value `Basic YWRtaW46YWRtaW4=`.

### API Documentation (Swagger UI)

Interactive API documentation is available via Swagger UI:

- **Swagger UI:** http://127.0.0.1:8000/api/docs/
- **ReDoc (alternative):** http://127.0.0.1:8000/api/redoc/
- **OpenAPI Schema (JSON):** http://127.0.0.1:8000/api/schema/

Use Swagger UI to:
- ✅ Browse all endpoints
- ✅ View request/response schemas
- ✅ Test endpoints directly in the browser
- ✅ See authentication requirements

### Pagination

All list endpoints in the API are paginated. They return a JSON object with four fields:
- **count:** total number of results found in the database
- **next:** URL of the next page (`null` if there is no next page)
- **previous:** URL of the previous page (`null` if there is no previous page)
- **results:** results of the current page

### Lote

#### Criação

**Path:** `/lotes_api/`
**Method:** `POST`
**Json Body:**
```json
{
    "identifier_code": "L1",
    "manufacturing_date": "2021-07-11",
    "product_qty": "10"
}
```

**Response:**
```json
{
    "id": 1,
    "identifier_code": "L1",
    "manufacturing_date": "2021-07-11",
    "product_qty": 10
}
```

#### Leitura da Lista

**Path:** `/lotes_api/`
**Method:** `GET`

**Response:**
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "identifier_code": "L1",
            "manufacturing_date": "2021-07-11",
            "product_qty": 10
        }
    ]
}
```

#### Leitura de um item

**Path:** `/lotes_api/1/`
**Method:** `GET`

**Response:**
```json
{
    "id": 1,
    "identifier_code": "L1",
    "manufacturing_date": "2021-07-11",
    "product_qty": 10
}
```

#### Atualização

**Path:** `/lotes_api/1/`
**Method:** `PUT`
**Json Body:**
```json
{
    "identifier_code": "L1",
    "manufacturing_date": "2021-07-11",
    "product_qty": "10"
}
```

**Response:**
```json
{
    "id": 1,
    "identifier_code": "L1",
    "manufacturing_date": "2021-07-11",
    "product_qty": 10
}
```

#### Exclusão

**Path:** `/lotes_api/1/`
**Method:** `DELETE`
**Response:** *empty*

### Produto

#### Criação

**Path:** `/produtos_api/`
**Method:** `POST`
**Json Body:**
```json
{
    "identifier_code": "P1",
    "name": "Tenis",
    "batch_number": 1,
    "colour": "red",
    "description": "Tênis Vermelho",
    "value": 199.99
}
```

***batch_number** deve ser o id do lote onde o produto será cadastrado*

**Response:**
```json
{
    "id": 1,
    "identifier_code": "P1",
    "name": "Tenis",
    "batch_number": 1,
    "colour": "red",
    "description": "Tênis Vermelho",
    "value": 199.99
}
```

#### Leitura da Lista

**Path:** `/produtos_api/`
**Method:** `GET`

**Response:**
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "identifier_code": "P1",
            "name": "Tenis",
            "batch_number": 1,
            "colour": "red",
            "description": "Tênis Vermelho",
            "value": 199.99
        }
    ]
}
```

#### Leitura de um item

**Path:** `/produtos_api/1/`
**Method:** `GET`

**Response:**
```json
{
    "id": 1,
    "identifier_code": "P1",
    "name": "Tenis",
    "batch_number": 1,
    "colour": "red",
    "description": "Tênis Vermelho",
    "value": 199.99
}
```

***batch_number** é o id do lote onde o produto foi cadastrado*

#### Atualização

**Path:** `/produtos_api/1/`
**Method:** `PUT`
**Json Body:**
```json
{
    "identifier_code": "P1",
    "name": "Tênis",
    "batch_number": 1,
    "colour": "blue",
    "description": "Tênis Azul",
    "value": 99.99
}
```

***batch_number** deve ser o id do lote para onde o produto será atualizado*

**Response:**
```json
{
    "id": 1,
    "identifier_code": "P1",
    "name": "Tênis",
    "batch_number": 1,
    "colour": "blue",
    "description": "Tênis Azul",
    "value": 99.99
}
```

#### Exclusão

**Path:** `/produtos_api/1/`
**Method:** `DELETE`
**Response:** *empty*

### Cliente

#### Criação

**Path:** `/clientes_api/`
**Method:** `POST`
**Json Body:**
```json
{
    "name": "Lucas",
    "cpf": "123.456.789-09",
    "birth_date": "1986-03-27"
}
```

**Response:**
```json
{
    "id": 1,
    "name": "Lucas",
    "cpf": "123.456.789-09",
    "birth_date": "1986-03-27"
}
```

#### Leitura da Lista

**Path:** `/clientes_api/`
**Method:** `GET`

**Response:**
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Lucas",
            "cpf": "123.456.789-09",
            "birth_date": "1986-03-27"
        }
    ]
}
```

#### Leitura de um item

**Path:** `/clientes_api/1/`
**Method:** `GET`

**Response:**
```json
{
    "id": 1,
    "name": "Lucas",
    "cpf": "123.456.789-09",
    "birth_date": "1986-03-27"
}
```

#### Atualização

**Path:** `/clientes_api/1/`
**Method:** `PUT`
**Json Body:**
```json
{
    "name": "Luke",
    "cpf": "123.456.789-09",
    "birth_date": "1986-03-27"
}
```

**Response:**
```json
{
    "id": 1,
    "name": "Luke",
    "cpf": "123.456.789-09",
    "birth_date": "1986-03-27"
}
```

#### Exclusão

**Path:** `/clientes_api/1/`
**Method:** `DELETE`
**Response:** *empty*

### Pedido

#### Criação

**Path:** `/pedidos_api/`
**Method:** `POST`
**Json Body:**
```json
{
    "order_number": 1,
    "client": 1,
    "order_date": "2021-07-11",
    "seller": 1,
    "products": [ 1 ]
}
```

***client** deve ser o id do cliente comprador*
***seller** deve ser o id do usuário vendedor*
***products** deve ser um array com os ids dos produtos comprados*

**Response:**
```json
{
    "id": 1,
    "order_number": 1,
    "client": 1,
    "order_date": "2021-07-11",
    "seller": 1,
    "products": [
        1
    ]
}
```

#### Leitura da Lista

**Path:** `/pedidos_api/`
**Method:** `GET`

**Response:**
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "order_number": 1,
            "client": {
                "id": 1,
                "name": "Luke",
                "cpf": "12345678909",
                "birth_date": "1986-03-27"
            },
            "order_date": "2021-07-11",
            "seller": "(admin)",
            "products": [
                {
                    "id": 1,
                    "identifier_code": "P1",
                    "name": "Tênis",
                    "colour": "blue",
                    "description": "Tênis Azul",
                    "value": 99.99,
                    "batch_number": 1
                }
            ],
            "total_value": 99.99
        }
    ]
}
```

Para fazer a ordenação por valor ou data, adicionar na url o parâmetro `ordering`.

**Paths:**
- `/pedidos_api/?ordering=order_date`
- `/pedidos_api/?ordering=total_value`

#### Leitura de um item

**Path:** `/pedidos_api/1/`
**Method:** `GET`

**Response:**
```json
{
    "id": 1,
    "order_number": 1,
    "client": {
        "id": 1,
        "name": "Luke",
        "cpf": "12345678909",
        "birth_date": "1986-03-27"
    },
    "order_date": "2021-07-11",
    "seller": "(admin)",
    "products": [
        {
            "id": 1,
            "identifier_code": "P1",
            "name": "Tênis",
            "colour": "blue",
            "description": "Tênis Azul",
            "value": 99.99,
            "batch_number": 1
        }
    ],
    "total_value": 99.99
}
```

#### Atualização

**Path:** `/pedidos_api/1/`
**Method:** `PUT`
**Json Body:**
```json
{
    "id": 1,
    "order_number": 1,
    "client": 1,
    "order_date": "2021-05-11",
    "seller": 1,
    "products": [
        1
    ]
}
```

**Response:**
```json
{
    "id": 1,
    "order_number": 1,
    "client": 1,
    "order_date": "2021-05-11",
    "seller": 1,
    "products": [
        1
    ]
}
```

#### Exclusão

**Path:** `/pedidos_api/1/`
**Method:** `DELETE`
**Response:** *empty*

## Architecture decisions

### Django user used as seller record

To provide login and password for sellers, Django's built-in admin user model was used.

### CPF set with 14 digits

The Rest Framework serializer does not allow entering a CPF with dots and dashes,
even though they are stripped before being saved to the database, unless the CPF
has 14 characters in the database.

## External libraries used

### Django (6.0.5)

Web framework used to build the API.

https://www.djangoproject.com/

### Django Rest Framework (3.17.1)

Used to simplify API development.

https://www.django-rest-framework.org/

### Validate DOC BR (2.0.0)

Used to validate the customer's CPF.

https://pypi.org/project/validate-docbr/

### python-decouple (3.8)

Used to manage environment variables from the `env/.env` file.

https://pypi.org/project/python-decouple/

### Gunicorn (23.0.0)

WSGI server used to serve the application in the Docker container.

https://gunicorn.org/

### WhiteNoise (6.9.0)

Used to serve static files (admin CSS/JS) directly from the WSGI application without a separate web server.

https://whitenoise.readthedocs.io/
