FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app \
    DATABASE_URL="sqlite:////app/data/accountiq.db"

WORKDIR /app

# Install curl for healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies first for layer caching
COPY backend/requirements.txt /app/backend/requirements.txt
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

# Copy entrypoint script and sanitize line endings (CRLF -> LF)
COPY backend/entrypoint.sh /app/entrypoint.sh
RUN sed -i 's/\r$//' /app/entrypoint.sh && chmod +x /app/entrypoint.sh

# Copy backend application source
COPY backend /app/backend

# Copy existing seed database if present in build context
COPY *accountiq.d[b] /app/seed_accountiq.db

# Ensure persistent storage mount point exists
RUN mkdir -p /app/data

EXPOSE 8000

HEALTHCHECK --interval=5s --timeout=5s --start-period=5s --retries=5 \
  CMD curl -f http://localhost:8000/api/health || exit 1

ENTRYPOINT ["/app/entrypoint.sh"]
