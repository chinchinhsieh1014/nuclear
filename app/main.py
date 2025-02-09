import psycopg2
import numpy as np
import pandas as pd
from fastapi import FastAPI, Query
from pydantic import BaseModel
from datetime import datetime
from fastapi.responses import JSONResponse
from typing import List
import openai
import time
from threading import Thread
from model import predict_failure

# Set up OpenAI API key
openai.api_key = "your-api-key-here"

app = FastAPI()

current_row_index = 0
limit = 10 

# Database connection parameters
DB_CONFIG = {
    "dbname": "pump_sensor_data",
    "user": "postgres",
    "password": "hackafuture",
    "host": "db",  # Changed from localhost to 'db' (the name of the database service in Docker)
    "port": "5432"
}

# Define the SensorData model
class SensorData(BaseModel):
    timestamp: datetime
    sensor_00: float
    sensor_01: float
    sensor_02: float
    sensor_03: float
    sensor_04: float
    sensor_05: float
    sensor_06: float
    sensor_07: float
    sensor_08: float
    sensor_09: float
    sensor_10: float
    sensor_11: float
    sensor_12: float
    sensor_13: float
    sensor_14: float
    sensor_15: float
    sensor_16: float
    sensor_17: float
    sensor_18: float
    sensor_19: float
    sensor_20: float
    sensor_21: float
    sensor_22: float
    sensor_23: float
    sensor_24: float
    sensor_25: float
    sensor_26: float
    sensor_27: float
    sensor_28: float
    sensor_29: float
    sensor_30: float
    sensor_31: float
    sensor_32: float
    sensor_33: float
    sensor_34: float
    sensor_35: float
    sensor_36: float
    sensor_37: float
    sensor_38: float
    sensor_39: float
    sensor_40: float
    sensor_41: float
    sensor_42: float
    sensor_43: float
    sensor_44: float
    sensor_45: float
    sensor_46: float
    sensor_47: float
    sensor_48: float
    sensor_49: float
    sensor_50: float
    sensor_51: float
    machine_status: str

def fetch_data():
    global current_row_index  # Use the global variable to track the current index

    # Connect to PostgreSQL
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # Fetch rows using the global index with OFFSET
    cursor.execute(f"SELECT * FROM pump_sensor_data LIMIT {limit} OFFSET {current_row_index};")
    rows = cursor.fetchall()

    # Get column names from the cursor description
    column_names = [desc[0] for desc in cursor.description]

    # Convert data into a list of SensorData objects
    sensor_data_list = []
    for row in rows:
        # Map row data to SensorData object
        cleaned_row = {column_names[i]: row[i] for i in range(len(row))}
        sensor_data = SensorData(**cleaned_row)
        sensor_data_list.append(sensor_data)

    # Close the connection
    cursor.close()
    conn.close()

    # Convert SensorData objects to dictionaries
    sensor_data_values = [sensor.dict() for sensor in sensor_data_list]

    # Sanitize the float values to avoid NaN or Infinity
    for sensor_data in sensor_data_values:
        for key, value in sensor_data.items():
            if isinstance(value, float) and (np.isnan(value) or np.isinf(value)):
                sensor_data[key] = 0.0  # Replace NaN or Inf with 0.0 (or any other value)

    # List of sensors to exclude
    exclude_sensors = [
        "sensor_00", "sensor_06", "sensor_07", "sensor_08", "sensor_09",
        "sensor_15", "sensor_37", "sensor_50"
    ]

    # Extract only the sensor values, excluding the ones in the exclude_sensors list
    sensor_values = [
        [sensor_data[f"sensor_{i:02}"] for i in range(52) if f"sensor_{i:02}" not in exclude_sensors]
        for sensor_data in sensor_data_values
    ]

    # Increment the global index by 10 for the next fetch
    current_row_index += limit

    return sensor_values

def process_data_with_model(sensor_data_values):
    # Send data to the model for prediction
    model_responses = []
    for sensor_data in sensor_data_values:
        # Clean the data: Convert to np.array and replace None or NaN with 0
        sensor_data = np.array(sensor_data, dtype=np.float32)
        # Replace NaN, Inf, or None values with 0
        sensor_data = np.nan_to_num(sensor_data, nan=0.0, posinf=0.0, neginf=0.0)
        response = predict_failure(sensor_data)
        model_responses.append(response)
    return model_responses

def get_openai_response(data, results):
    # Format the prompt with the data and model results
    prompt = f"Here is the data and the results for Pump Sensor Prediction model:\n\n"
    for i, row in enumerate(data):
        prompt += f"Data {i+1}: {row}, Model Result: {results[i]}\n"

    prompt += "\nPlease analyze and provide an output based on the above."

    # Send the prompt to OpenAI
    response = openai.Completion.create(
        engine="gpt-3.5-turbo",  # Use the model of your choice
        prompt=prompt,
        max_tokens=150
    )

    return response.choices[0].text.strip()

@app.get("/process_data")
async def process_data():
    # Step 1: Fetch data
    data = fetch_data()
    
    # Step 2: Process data with the model
    results = process_data_with_model(data)

    # Step 3: Send data and results to OpenAI
    # openai_output = get_openai_response(data, results)

    # Step 4: Return the data, results, and OpenAI output to the frontend
    return {
        "data": data,
        "model_results": results,
        # "openai_output": openai_output
    }
