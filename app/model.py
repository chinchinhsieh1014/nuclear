import tensorflow as tf
import numpy as np

# Define the model path
MODEL_PATH = "/app/models/Pump_LSTM_Fapi_OOP_1.h5"

# Define the custom objects
def custom_objects():
    return {}

# Try loading the model with custom objects
try:
    lstm_model = tf.keras.models.load_model(MODEL_PATH, custom_objects=custom_objects(), compile=False)
    print("✅ Model loaded successfully!")
except Exception as e:
    lstm_model = None
    print(f"Error loading model: {e}")
    # Optionally log more details:
    import traceback
    traceback.print_exc()

def predict_failure(sensor_data: np.array):
    if lstm_model is None:
        return {"error": "Model could not be loaded."}

    try:
        # Ensure input data is a NumPy array
        sensor_data = np.array(sensor_data, dtype=np.float32)

        # Ensure sensor data has the correct shape (batch_size=1, timesteps=1, features=num_features)
        reshaped_data = sensor_data.reshape(1, 1, -1)  # Reshaping to [1, 1, num_features]

        # Run inference using the LSTM model
        signal_pred, class_pred = lstm_model.predict(reshaped_data)

        # Extract classification prediction (class with highest probability)
        predicted_class = np.argmax(class_pred, axis=1)[0]

        return {
            "signal_prediction": float(signal_pred[0][0]),  # Convert NumPy array to float
            "class_probabilities": class_pred[0].tolist(),  # Convert NumPy array to list
            "predicted_class": int(predicted_class),  # Convert NumPy index to integer
            "status": "CRITICAL" if predicted_class == 2 else "WARNING" if predicted_class == 1 else "NORMAL"
        }

    except Exception as e:
        return {"error": str(e)}