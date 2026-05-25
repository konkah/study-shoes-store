# Copilot Instructions — Study Shoes Store

## Project overview

REST API for shoe sales management, built with Django 6.0 and Django REST Framework 3.17.
This is a local study project — there is no production environment, no Docker Hub image, and no external deployment.

## Stack

- **Python** 3.13
- **Django** 6.0.5
- **Django REST Framework** 3.17.1
- **django-filter** 25.2
- **validate-docbr** 2.0.0 (CPF validation)
- **python-decouple** 3.8 (environment variables)
- **gunicorn** 23.0.0 (WSGI server)
- **whitenoise** 6.9.0 (static files)
- **SQLite** (local database)
- **Docker + Docker Compose** (python:3.13-slim base image, used only for local testing)

## Project structure

```
env/
  .env                # local environment variables (not versioned)
  .env.example        # template for environment variables
study_shoes_store/
  manage.py
  requirements.txt
  shoes_api/          # main app: models, views, serializers, urls
  study_shoes_store/  # Django project config (settings, urls, wsgi, asgi)
shoes-store.Dockerfile
docker-compose.yml
entrypoint.sh
```

## Domain models

| Model     | Key fields                                                              |
|-----------|-------------------------------------------------------------------------|
| `Batch`   | `identifier_code`, `manufacturing_date`, `product_qty`                  |
| `Product` | `identifier_code`, `name`, `batch_number` (FK→Batch), `colour`, `value` |
| `Client`  | `name`, `cpf` (14 chars, unique), `birth_date`                          |
| `Order`   | `order_number`, `client` (FK), `seller` (FK→User), `products` (M2M), `total_value` |

- **Seller** uses Django's built-in `User` model.
- **CPF** is stored without formatting (11 digits) but accepted and returned formatted (`xxx.xxx.xxx-xx`).
- **`total_value`** on `Order` is computed automatically in `OrderSerializer.to_internal_value` by summing the `value` of all related products.
- **`value`** (`Product`) and **`total_value`** (`Order`) use `DecimalField(max_digits=10, decimal_places=2)` for monetary precision.
- **`order_number`** on `Order` has `unique=True`.

## API endpoints

All endpoints require **Basic Authentication**. Default credentials: `admin` / `admin`.
All list responses are paginated.

| Resource | URL prefix       |
|----------|------------------|
| Batch    | `/lotes_api/`    |
| Product  | `/produtos_api/` |
| Client   | `/clientes_api/` |
| Order    | `/pedidos_api/`  |

Orders support ordering via query parameter: `?ordering=total_value` or `?ordering=order_date`.

Read requests (`GET`) on orders use `ListOrderSerializer` (nested objects); write requests use `OrderSerializer` (IDs only).

## Coding conventions

- ViewSets use `rest_framework.viewsets.ModelViewSet`.
- Serializers live in `shoes_api/serializers.py`; views in `shoes_api/views.py`.
- URL routing uses DRF's `DefaultRouter` registered in `shoes_api/urls.py`.
- No custom pagination class — uses DRF default page size settings.
- Colour choices for `Product` are defined as `COLOUR_CHOICES` class constant on the model.

## Running locally (Docker Compose)

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

## Environment variables setup

Copy the example file before running for the first time:
```bash
cp env/.env.example env/.env
```

Edit `env/.env` with your values. Variables read by the project:

| Variable | Description | Default in `.env.example` |
|---|---|---|
| `SECRET_KEY` | Django secret key | placeholder |
| `DEBUG` | Debug mode | `False` |
| `ALLOWED_HOSTS` | Allowed hosts (comma-separated) | `localhost,127.0.0.1` |
| `CSRF_TRUSTED_ORIGINS` | Trusted origins for CSRF (comma-separated) | `http://localhost:8000,http://127.0.0.1:8000` |
| `DJANGO_SUPERUSER_USERNAME` | Admin username created on first run | `admin` |
| `DJANGO_SUPERUSER_EMAIL` | Admin email | `admin@example.com` |
| `DJANGO_SUPERUSER_PASSWORD` | Admin password | `change-me` |

## Django management commands (inside the container)

```bash
# Run any management command inside the running container
docker compose exec web python manage.py <command>

# Apply pending migrations
docker compose exec web python manage.py migrate

# Generate migrations after changing models
docker compose exec web python manage.py makemigrations shoes_api --name <migration_name>

# Open a Django shell inside the container
docker compose exec web python manage.py shell

# Create a superuser manually
docker compose exec web python manage.py createsuperuser
```

> **Note:** With Docker volumes enabled, migration files are generated directly on the host within the `shoes_api/migrations/` directory.

## Code Quality & Testing

**Test Suite (15 tests)**
- `ClientSerializerTestCase`: 4 tests for CPF validation, formatting, and uniqueness
- `OrderSerializerTestCase`: 3 tests for total_value calculation and constraints
- `APIAuthenticationTestCase`: 8 tests for endpoint authentication across all 4 resources

**Run all tests:**
```bash
docker compose exec web python manage.py test shoes_api -v 2
```

**Code Quality Improvements (Completed)**
1. Environment variables management with `python-decouple` (dev/prod config)
2. Explicit authentication classes (`SessionAuthentication` + `BasicAuthentication`)
3. Production-ready WSGI server (`gunicorn` 23.0.0)
4. Static file serving with `WhiteNoise` middleware
5. CSRF protection via `CSRF_TRUSTED_ORIGINS` environment variable
6. Monetary precision: `DecimalField` for `Product.value` and `Order.total_value`
7. Unique constraint on `Order.order_number` to prevent duplicates
8. Product colors as `COLOUR_CHOICES` class constant
9. CPF formatting using `CPF().mask()` method from `validate-docbr`
10. Order total_value calculation using Pythonic `sum()` generator expression
11. Comprehensive test coverage for serializers and API endpoints

API available at: http://127.0.0.1:8000
