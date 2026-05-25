# Copilot Instructions — Study Shoes Store

## Project overview

REST API for shoe sales management, built with Django 6.0 and Django REST Framework 3.17.
This is a local study project — there is no production environment, no Docker Hub image, and no external deployment.

## Stack

- **Python** 3.12
- **Django** 6.0.5
- **Django REST Framework** 3.17.1
- **django-filter** 25.2
- **validate-docbr** 2.0.0 (CPF validation)
- **SQLite** (local database)
- **Docker + Docker Compose** (Ubuntu 24.04 base image, used only for local testing)

## Project structure

```
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
- Colour choices for `Product` are defined as a list of tuples directly on the model field.

## Running locally (Docker Compose)

```bash
# Build and start (blocking terminal)
docker compose up --build

# Build and start in background
docker compose up --build -d

# View logs of all services (when running in background)
docker compose logs -f

# View logs of a specific service
docker compose logs -f web

# Stop containers
docker compose stop

# Stop and remove containers, images and volumes
docker compose down --rmi all --volumes

# --- Single container ---

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

# --- Inspection ---

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

API available at: http://127.0.0.1:8000