from fastapi import FastAPI
import pandas as pd
import numpy as np

app = FastAPI()


data = pd.read_csv("app/data/data_nuclear.csv")

@app.get("/predictive_maintenance")
def predictive_maintenance():    
    # Get the last row of data    
    last_row = data.tail(1)        
    # Replace NaN values with None to make them JSON serializable    
    last_row = last_row.replace({np.nan: None})        
    # Convert to dictionary and return    
    return {"message": "Predictive maintenance results", "data": last_row.to_dict('records')[0]}

@app.get("/anomaly_detection")
def anomaly_detection():   
     # Replace with actual anomaly detection logic    
    return {"message": "Anomaly detection results"}

@app.get("/grid_optimization")
def grid_optimization():    
# Replace with actual grid optimization logic    
    return {"message": "Grid optimization results"}

@app.get("/digital_twin")
def digital_twin():    
# Replace with actual digital twin logic   
    return {"message": "Digital twin representation"}

@app.get("/compliance_check")
def compliance_check():    
    # Replace with actual compliance checking logic    
    return {"message": "Compliance check results"}

@app.get("/sensor_data")
def sensor_data():
    latest_data = data.tail(1).to_dict()    
    return {"latest_sensor_data": latest_data}

@app.get("/alerts")
def alerts():    
    # Replace with actual alert logic    
    return {"message": "Alerts based on sensor data"}

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

