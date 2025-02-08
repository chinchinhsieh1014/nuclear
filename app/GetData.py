import psycopg2
import numpy as np
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from datetime import datetime

app = FastAPI()

# Database connection parameters
DB_CONFIG = {
    "dbname": "pump_sensor_data",
    "user": "postgres",
    "password": "hackafuture",
    "host": "db",  # Changed from localhost to 'db' (the name of the database service in Docker)
    "port": "5432"
}

@app.get("/data")
def get_sensor_data():
    """Fetch and return all sensor data from the PostgreSQL database."""
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Fetch all rows from the table
        cursor.execute("SELECT * FROM pump_sensor_data LIMIT 10;")
        rows = cursor.fetchall()

        # Get column names from the cursor description
        column_names = [desc[0] for desc in cursor.description]

        # Clean and format data into a list of dictionaries
        cleaned_data = []
        for row in rows:
            cleaned_row = {}
            for idx, value in enumerate(row):
                # Convert datetime objects to string (ISO format)
                if isinstance(value, datetime):
                    cleaned_row[column_names[idx]] = value.isoformat()
                # Convert NaN or Infinity to None
                elif isinstance(value, float) and (np.isnan(value) or np.isinf(value)):
                    cleaned_row[column_names[idx]] = None
                else:
                    cleaned_row[column_names[idx]] = value
            cleaned_data.append(cleaned_row)

        # Close the connection
        cursor.close()
        conn.close()

        # Return data as a JSON response
        return JSONResponse(content={"data": cleaned_data}, status_code=200)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
