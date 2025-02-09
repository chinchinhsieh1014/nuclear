#!/bin/bash

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
until nc -z -v -w30 db 5432
do
  echo "Waiting for database connection..."
  sleep 1
done

echo "Starting database initialization"
python3 /app/database.py
echo "Database initialization complete"

sleep 5

# Start FastAPI with Uvicorn
echo "Starting FastAPI application..."
exec uvicorn main:app --host 0.0.0.0 --port 8001 --reload