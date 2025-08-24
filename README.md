# Price Bot

Production-ready Telegram bot with modular architecture, optional gRPC database microservice, observability stack, tests, and CI/CD.

- Docs: [Architecture](docs/architecture.md), [gRPC API](docs/grpc.md), [Observability](docs/observability.md)

## Features
- Aiogram 3.x router/action/schema separation
- Pydantic v2 settings and validation
- orjson for fast JSON serialization
- Optional gRPC DB microservice (SQLAlchemy 2.x)
- Dockerized dev and prod setups
- Observability: Loki, Promtail, Prometheus, Grafana
- Health and metrics endpoints: `/healthz`, `/ready`, `/metrics`
- Tests (pytest) and Ruff linting
- GitHub Actions CI/CD

## Architecture
- `bot/src`: bot app (routers, actions, schemas, misc, services)
- `database`: gRPC DB microservice (models, repository, server)
- `monitoring`: configs for Loki/Promtail/Prometheus/Grafana
- `docker-compose.*.yml`: base, local overlay, prod overlay

## Requirements
- Docker and Docker Compose
- Python 3.11 for local dev/tests

## Setup
```
cp .env.example .env
```
Update `.env` with your secrets (TOKEN, Postgres, etc.).

## Run (local)
```
docker compose -f docker-compose.yaml -f docker-compose.local.yml up -d --build
```
- Bot: polls Telegram, exposes `/healthz`, `/ready`, `/metrics` on 8080
- Database service: gRPC on 50051
- Postgres: 5432

## Run (prod)
```
docker compose -f docker-compose.yaml -f docker-compose.prod.yml up -d --build
```
Reads configuration from `.env`.

## Monitoring
```
docker compose -f docker-compose.yaml -f docker-compose.local.yml up -d loki promtail prometheus grafana
```
- Grafana: http://localhost:3000 (admin/admin)
- Prometheus: http://localhost:9090
- Loki readiness: http://localhost:3100/ready
See `docs/observability.md` for details.

## Testing
```
python -m pip install -r requirements.txt
pytest -q
```
Postgres-backed tests expect `TEST_DATABASE_DSN` or running local Postgres (see CI).

## Linting
```
ruff format .
ruff check .
```

## CI/CD
- `.github/workflows/ci.yml`: Ruff + pytest + Docker build
- `.github/workflows/cd.yml`: Build & push images to GHCR on main/master/prod

## License
MIT