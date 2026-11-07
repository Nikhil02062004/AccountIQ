#!/bin/sh
set -e

# Ensure persistent data directory exists
mkdir -p /app/data

# If persistent database does not exist yet, check if seed file exists
if [ ! -f /app/data/accountiq.db ] && [ -f /app/seed_accountiq.db ]; then
  echo "[AccountIQ] Initializing /app/data/accountiq.db from packaged seed..."
  cp /app/seed_accountiq.db /app/data/accountiq.db
fi

echo "[AccountIQ] Starting AccountIQ FastAPI server on 0.0.0.0:8000..."
exec uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
