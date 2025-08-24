# Database Service

- gRPC server exposing DB operations
- SQLAlchemy 2.0, session generator, repositories

## Environment
- DATABASE_DSN: SQLAlchemy DSN (e.g., postgresql+psycopg://user:pass@postgres:5432/db)
- GRPC_HOST, GRPC_PORT: optional, default 0.0.0.0:50051

## Run
- docker build -f database/Dockerfile -t price-db .
- docker-compose up database

