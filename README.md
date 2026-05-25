# Study Shoes Store

author: Karlos Helton Braga

## How to run the project

The Docker image for this project is available on Docker Hub.

```
docker run --name shoes-store -it -p 8000:8000 study_shoes_store
```

To stop, press CTRL+C.

If you want to build from the Dockerfile available in the repository, run:

```
docker build . -f shoes-store.Dockerfile -t study_shoes_store --network=host
```

## How to use the API

O endereço da API depende do IP da máquina docker. Usualmente, o docker sobe a máquina no IP 172.17.0.2. A porta da API é 8000. Nesse caso, o endereço final da API é: http://172.17.0.2:8000.

Só é possível utilizar a API com login. O usuário **admin** com senha **admin** é inserido na criação da máquina em docker, para facilitar a manipulação da API.

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

## Decisões de arquitetura

### Usado usuário do django como cadastro do vendedor

Para o vendedor ter login e senha, foi usado o usuário nativo do django admin.

### CPF colocado com 14 dígitos

O Serializador do Rest Framework não deixa a pessoa colocar um CPF com pontos e traços,
mesmo eles sendo removidos antes de ir para o banco de dados, se o CPF não tiver
14 caracteres no banco de dados.

## Bibliotecas externas usadas

### Django Rest Framework (3.12.4)

Usada para facilitar o desenvolvimento da API.

https://www.django-rest-framework.org/

### Validate DOC BR (1.8.2)

Usada para validar o CPF do cliente.

https://pypi.org/project/validate-docbr/