import os
import pandas as pd
import psycopg2
from psycopg2 import sql, extras
from urllib.parse import urlparse
from psycopg2 import OperationalError

# Get DATABASE_URL from environment variables
database_url = os.getenv('DATABASE_URL')

# Error handling for missing DATABASE_URL
if not database_url:
    raise ValueError("DATABASE_URL environment variable is not set")

# Parse the database URL
url = urlparse(database_url)

# Establish a connection to the PostgreSQL database
try:
    conn = psycopg2.connect(
        dbname=url.path[1:],  # Extract the database name from the URL
        user=url.username,     # Extract the username
        password=url.password, # Extract the password
        host=url.hostname,     # Extract the host
        port=url.port          # Extract the port
    )
    print("✅ Database connection successful")
except OperationalError as e:
    print(f"Error connecting to the database: {e}")
    exit(1)

# Load the CSV file into a pandas DataFrame
try:
    df = pd.read_csv("/app/data/pump_sensor.csv")
except Exception as e:
    print(f"Error reading CSV file: {e}")
    exit(1)

# Ensure the timestamp is in the correct format
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

# Drop rows with invalid timestamps
df.dropna(subset=['timestamp'], inplace=True)

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Create the table if it doesn't exist
create_table_query = '''
CREATE TABLE IF NOT EXISTS pump_sensor_data (
    timestamp TIMESTAMP,
    sensor_00 FLOAT,
    sensor_01 FLOAT,
    sensor_02 FLOAT,
    sensor_03 FLOAT,
    sensor_04 FLOAT,
    sensor_05 FLOAT,
    sensor_06 FLOAT,
    sensor_07 FLOAT,
    sensor_08 FLOAT,
    sensor_09 FLOAT,
    sensor_10 FLOAT,
    sensor_11 FLOAT,
    sensor_12 FLOAT,
    sensor_13 FLOAT,
    sensor_14 FLOAT,
    sensor_15 FLOAT,
    sensor_16 FLOAT,
    sensor_17 FLOAT,
    sensor_18 FLOAT,
    sensor_19 FLOAT,
    sensor_20 FLOAT,
    sensor_21 FLOAT,
    sensor_22 FLOAT,
    sensor_23 FLOAT,
    sensor_24 FLOAT,
    sensor_25 FLOAT,
    sensor_26 FLOAT,
    sensor_27 FLOAT,
    sensor_28 FLOAT,
    sensor_29 FLOAT,
    sensor_30 FLOAT,
    sensor_31 FLOAT,
    sensor_32 FLOAT,
    sensor_33 FLOAT,
    sensor_34 FLOAT,
    sensor_35 FLOAT,
    sensor_36 FLOAT,
    sensor_37 FLOAT,
    sensor_38 FLOAT,
    sensor_39 FLOAT,
    sensor_40 FLOAT,
    sensor_41 FLOAT,
    sensor_42 FLOAT,
    sensor_43 FLOAT,
    sensor_44 FLOAT,
    sensor_45 FLOAT,
    sensor_46 FLOAT,
    sensor_47 FLOAT,
    sensor_48 FLOAT,
    sensor_49 FLOAT,
    sensor_50 FLOAT,
    sensor_51 FLOAT,
    machine_status VARCHAR(50)
);
'''

# Execute the create table query
cursor.execute(create_table_query)
conn.commit()

# Prepare the insert query
insert_query = """
INSERT INTO pump_sensor_data (
    timestamp, sensor_00, sensor_01, sensor_02, sensor_03, sensor_04, sensor_05, 
    sensor_06, sensor_07, sensor_08, sensor_09, sensor_10, sensor_11, sensor_12, 
    sensor_13, sensor_14, sensor_15, sensor_16, sensor_17, sensor_18, sensor_19, 
    sensor_20, sensor_21, sensor_22, sensor_23, sensor_24, sensor_25, sensor_26, 
    sensor_27, sensor_28, sensor_29, sensor_30, sensor_31, sensor_32, sensor_33, 
    sensor_34, sensor_35, sensor_36, sensor_37, sensor_38, sensor_39, sensor_40, 
    sensor_41, sensor_42, sensor_43, sensor_44, sensor_45, sensor_46, sensor_47, 
    sensor_48, sensor_49, sensor_50, sensor_51, machine_status
) 
VALUES %s
"""

# Create a list of tuples from DataFrame rows
values = [tuple(row) for index, row in df.iterrows()]

# Insert the data using psycopg2's execute_values for bulk insert
try:
    extras.execute_values(cursor, insert_query, values)
    conn.commit()
except Exception as e:
    print(f"Error inserting data: {e}")
    conn.rollback()

# Close the cursor and connection
cursor.close()
conn.close()

print("Data inserted successfully.")