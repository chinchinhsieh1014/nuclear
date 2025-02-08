#!/bin/bash

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
until nc -z -v -w30 db 5432
do
  echo "Waiting for database connection..."
  sleep 1
done

# Run the getdata.py script to populate the database
echo "Running data initialization script..."
python3 app/database.py

# Start FastAPI with Uvicorn
echo "Starting FastAPI application..."
exec uvicorn app.GetData:app --host 0.0.0.0 --port 8001 --reload