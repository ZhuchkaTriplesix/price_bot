# Architecture Overview

This project separates Telegram bot concerns into clear layers, and moves database responsibilities into a dedicated gRPC microservice.

## Bot layers (ot/src)
- handlers/ (routers): routes, answers
- actions: business logic, optional gRPC calls
- schemas: Pydantic v2 validation
- misc: utilities (translation, orjson)
- services: external clients (e.g., DatabaseClient)
- config.py: pydantic-settings
- main.py: entrypoint + health/metrics

### Example flow (admin)
1) Router matches command (/add_admin)
2) Validate input via schema
3) Call async action
4) Access check via OWNER/ADMIN env; optional gRPC DB call
5) Router replies

## Database microservice (database)
- models: SQLAlchemy 2.x
- repository: data access logic
- db.py: engine + session scope generator
- server.py: gRPC service
- proto/database.proto: contract

## Observability
- Bot: /healthz, /ready, /metrics
- Loki, Promtail, Prometheus, Grafana via compose

## CI/CD
- GitHub Actions: Ruff, pytest, Docker build; push to GHCR on prod branches

## Conventions
- No DB calls in bot layer
- Keep routers thin; actions testable
- Validate user input with Pydantic
- Prefer orjson for JSON

