# fincore-api

API Backend de um sistema de Gestão Financeira Pessoal/Empresarial, construída em Django + Django REST Framework, com PostgreSQL rodando via Docker.

## O que é

Backend financeiro com contas, categorias, transações (receita/despesa/transferência), orçamentos mensais e transações recorrentes. Todos os models seguem um padrão corporativo obrigatório de:

- **Auditoria**: `created_at`, `updated_at`, `deleted_at` em todo model.
- **Soft delete**: nenhum registro é apagado fisicamente — usa `SoftDeleteManager`, `soft_delete()`, `restore()`, `is_deleted`.
- **Índices** em `created_at`, `updated_at`, `deleted_at` (e campos de negócio relevantes, como `transaction_date`).

## Stack

- Python 3.14 + Django 6.1.1
- Django REST Framework
- PostgreSQL 16 (container Docker)
- `psycopg2-binary` (driver do Postgres) + `python-dotenv` (variáveis de ambiente)

## Estrutura do projeto

```
fincore-api/
├── docker-compose.yml       # container do Postgres
├── .env / .env.example      # credenciais do banco (local, gitignorado)
├── backend/
│   ├── manage.py
│   ├── requirements.txt
│   ├── config/               # settings, urls, wsgi/asgi
│   └── finance/               # app principal
│       ├── models/
│       │   ├── base.py                  # BaseModel abstrato (auditoria + soft delete)
│       │   ├── account.py               # Conta financeira
│       │   ├── category.py              # Categoria (com hierarquia pai/filho)
│       │   ├── transaction.py           # Transação (receita/despesa/transferência)
│       │   ├── budget.py                # Orçamento mensal por categoria
│       │   └── recurring_transaction.py # Transação recorrente (aluguel, assinatura...)
│       ├── seeds/                       # dados de exemplo (categorias padrão)
│       ├── management/commands/seed.py  # comando `manage.py seed`
│       ├── admin.py
│       └── migrations/
└── frontend/                 # (ainda não iniciado)
```

## Setup do zero

### 1. Ambiente virtual

```bash
cd fincore-api
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
```

### 2. Variáveis de ambiente

Copie o exemplo e ajuste se precisar (os valores padrão já funcionam para dev local):

```bash
cp .env.example .env
```

| Variável | Padrão | Descrição |
|---|---|---|
| `POSTGRES_DB` | `fincore` | Nome do banco |
| `POSTGRES_USER` | `fincore` | Usuário do banco |
| `POSTGRES_PASSWORD` | `fincore` | Senha (dev only) |
| `POSTGRES_HOST` | `localhost` | Host do Postgres |
| `POSTGRES_PORT` | `5433` | Porta exposta pelo container (5432 já estava em uso por outro projeto local) |

### 3. Subir o Postgres

```bash
docker compose up -d
docker compose ps   # confirma status "healthy"
```

### 4. Rodar as migrations

```bash
cd backend
python manage.py migrate
```

Isso cria todas as tabelas (`finance_account`, `finance_category`, `finance_transaction`, `finance_budget`, `finance_recurring_transaction`) e aplica os índices.

### 5. Popular dados de exemplo (seed)

```bash
python manage.py seed
```

Cria as categorias padrão definidas em `finance/seeds/categories.py`. É idempotente — pode rodar de novo sem duplicar (usa `get_or_create`).

### 6. Criar um superusuário (acesso ao /admin)

```bash
python manage.py createsuperuser
```

### 7. Rodar o servidor

```bash
python manage.py runserver
```

Acesse `http://127.0.0.1:8000/admin/`.

## Comandos do dia a dia

| Ação | Comando |
|---|---|
| Ativar venv | `source venv/bin/activate` (a partir da raiz do projeto) |
| Rodar servidor | `python manage.py runserver` |
| Criar migration após mudar um model | `python manage.py makemigrations` |
| Aplicar migrations | `python manage.py migrate` |
| Popular categorias padrão | `python manage.py seed` |
| Checar erros de config | `python manage.py check` |
| Acessar o banco via terminal | `docker exec -it fincore-postgres psql -U fincore -d fincore` |
| Parar o Postgres | `docker compose down` (dados persistem no volume) |

## Entidades

| Model | Descrição |
|---|---|
| `Account` (Conta) | De onde o dinheiro sai/entra: banco, carteira, cartão, investimento |
| `Category` (Categoria) | Agrupa receitas/despesas, com hierarquia opcional (categoria pai) |
| `Transaction` (Transação) | Lançamento central: receita, despesa ou transferência entre contas |
| `Budget` (Orçamento) | Teto de gasto por categoria/mês/ano |
| `RecurringTransaction` (Recorrência) | Template para lançamentos fixos/recorrentes (aluguel, assinatura) |

## Status do projeto (checklist)

- [x] Base models (auditoria + soft delete)
- [x] Modelagem das 5 entidades com `clean()`, `Meta`, índices
- [x] Migrations aplicadas
- [x] Seed de categorias padrão
- [ ] Serializers, ViewSets e rotas (DRF) — pendente
- [ ] Cálculo de saldo por conta — pendente
- [ ] Testes automatizados (soft delete, transferências, saldo) — pendente

## Observações

- Ambiente de desenvolvimento apenas — `DEBUG=True` e `SECRET_KEY` ainda hardcoded em `config/settings.py`, não usar essa config em produção.
- Banco de dados: PostgreSQL via Docker na porta `5433` (não `5432`, para não conflitar com outro projeto local).
