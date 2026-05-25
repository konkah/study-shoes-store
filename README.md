# Study Shoes Store

author: Karlos Helton Braga

## How to run the project

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

## How to use the API

The API address is: http://127.0.0.1:8000.

Authentication is required to use the API. The user **admin** with password **admin** is created when the Docker container is built, to make it easier to interact with the API.

O tipo de autenticação usada é o Basic Authentication. É possível entender como ela funciona no seguinte link:

https://developer.mozilla.org/pt-BR/docs/Web/HTTP/Headers/Authorization

Para o usuário e senha citados acima, o header `Authorization` deve ter o valor `Basic YWRtaW46YWRtaW4=`.

### Paginação

Todas as listas da API são paginadas. Dessa forma, retornam no json quatro itens:
- **count:** contagem total de resultados encontrados no banco de dados
- **next:** url da próxima página (retorna `null` se não houver uma próxima página)
- **previous:** url da página anterior (retorna `null` se não houver uma página anterior)
- **results:** resultados da página atual

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