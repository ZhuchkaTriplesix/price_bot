FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_SYSTEM_PYTHON=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

COPY requirements.txt /app/requirements.txt
RUN uv pip install --no-cache -r /app/requirements.txt

# bring in proto to generate client stubs
COPY database/proto /app/database/proto
RUN python -m grpc_tools.protoc -I/app/database/proto --python_out=/app/database/proto --grpc_python_out=/app/database/proto /app/database/proto/database.proto

COPY bot /app/bot

EXPOSE 8080

CMD ["uv", "run", "python", "-m", "bot.src.main"]


