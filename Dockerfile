FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# Install dependencies first for better Docker layer caching
COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev

# Copy application
COPY src src

EXPOSE 8001

CMD ["uv", "run", "--no-dev", "python", "src/main.py"]