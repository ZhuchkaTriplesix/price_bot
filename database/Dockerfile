FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_SYSTEM_PYTHON=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl ca-certificates build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

COPY database/requirements.txt /app/requirements.txt
RUN uv pip install --no-cache -r /app/requirements.txt

# Generate gRPC code
COPY database/proto /app/database/proto
RUN python -m grpc_tools.protoc -I/app/database/proto --python_out=/app/database/proto --grpc_python_out=/app/database/proto /app/database/proto/database.proto

COPY database/src /app/database/src
COPY database/__init__.py /app/database/__init__.py

EXPOSE 50051

CMD ["uv", "run", "python", "-m", "database.src.server"]


