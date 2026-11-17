# API de Ocorrências (FastAPI)

API REST para registro de ocorrências em rodovias (acidentes, buracos, alagamentos e obstruções), feita com FastAPI, SQLAlchemy 2.0 e PostgreSQL.

Existe uma versão equivalente em Go: [ocorrencias-api-go](https://github.com/jot4-ge/ocorrencias-api-go).

## Stack

- Python 3.12 e FastAPI
- Pydantic (validação e documentação automática)
- SQLAlchemy 2.0 e PostgreSQL 16
- Docker Compose (banco de dados)
- pytest (testes automatizados)

## Como rodar

Pré-requisitos: Python 3.12+, Docker Desktop e Git.

```bash
# 1. Clonar e entrar na pasta
git clone https://github.com/jot4-ge/ocorrencias-api.git
cd ocorrencias-api

# 2. Subir o PostgreSQL
docker compose up -d

# 3. Criar e ativar o ambiente virtual
python -m venv .venv
.venv\Scripts\Activate.ps1        # Windows (PowerShell)
# source .venv/bin/activate       # Linux/macOS

# 4. Instalar as dependências
pip install "fastapi[standard]" sqlalchemy "psycopg[binary]" pytest

# 5. Iniciar a API
fastapi dev main.py
```

A documentação interativa fica em http://127.0.0.1:8000/docs.

A conexão com o banco usa a variável `DATABASE_URL`. Sem ela, o padrão é
`postgresql+psycopg://postgres:postgres@localhost:5432/ocorrencias` (apenas para desenvolvimento local).

## Endpoints

| Método | Rota | Descrição |
|---|---|---|
| GET | `/ocorrencias` | Lista com filtros `rodovia`, `tipo` e `limite` (1 a 50) |
| GET | `/ocorrencias/total` | Total de ocorrências |
| GET | `/ocorrencias/{id}` | Busca por id (404 se não existir) |
| POST | `/ocorrencias` | Cria uma ocorrência (201) |
| PUT | `/ocorrencias/{id}` | Substitui a ocorrência inteira |
| PATCH | `/ocorrencias/{id}` | Altera apenas os campos enviados |
| DELETE | `/ocorrencias/{id}` | Remove (204) |

### Regras de validação

- `rodovia`: formato `BR-` seguido de 3 dígitos (ex.: `BR-040`)
- `tipo`: `acidente`, `buraco`, `alagamento` ou `obstrucao`
- `km`: inteiro de 0 a 5000
- `descricao`: opcional, até 200 caracteres

### Exemplo

```bash
curl -X POST http://127.0.0.1:8000/ocorrencias \
  -H "Content-Type: application/json" \
  -d '{"rodovia": "BR-040", "tipo": "acidente", "km": 12}'
```

## Testes

```bash
pytest -v
```

Os testes usam SQLite em memória (via `dependency_overrides`), então não dependem do PostgreSQL nem do Docker.

## Estrutura

```
├── main.py            # rotas e ciclo de vida da aplicação
├── database.py        # engine, sessão e get_db
├── models.py          # modelo SQLAlchemy
├── schemas.py         # schemas Pydantic (Create, Update, Response)
├── docker-compose.yml # PostgreSQL
└── tests/             # testes com pytest
```

## Próximos passos

- Migrações com Alembic
- Front-end em React consumindo a API