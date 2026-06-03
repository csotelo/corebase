FROM python:3.12-slim AS base

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY base.txt ./

# ── Development ────────────────────────────────────────────────────────────────
FROM base AS development

COPY dev.txt ./
RUN pip install --no-cache-dir -r dev.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "config.asgi:application", "--host", "0.0.0.0", "--port", "8000", "--reload", "--reload-dir", "/app"]

# ── Production ─────────────────────────────────────────────────────────────────
FROM base AS production

RUN pip install --no-cache-dir -r base.txt gunicorn

COPY . .

EXPOSE 8000
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "120"]
