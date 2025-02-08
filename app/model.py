import tensorflow as tf
import numpy as np
import joblib

# Load pre-trained AI models
lstm_model = tf.keras.models.load_model("models/lstm_model.h5")
xgb_model = joblib.load("models/xgb_model.pkl")

def predict_failure(sensor_data: np.array):
    """Predicts failure risk using AI models"""
    lstm_prediction = lstm_model.predict(sensor_data.reshape(1, -1))
    xgb_prediction = xgb_model.predict(sensor_data.reshape(1, -1))
    return {"failure_risk": float(lstm_prediction[0][0]), "status": "ALERT" if xgb_prediction[0] == 1 else "NORMAL"}