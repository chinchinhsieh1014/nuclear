# 2025 Hackafuture
- download the data ***pump_sensor.csv*** and put it in app/data
- run `docker-compose up --build`
- http://localhost:8001/data

1. Database Management: Efficient handling and storage of sensor data in a PostgreSQL database, ensuring data integrity and optimal access for model processing.

2. Model Inference: The system sends processed sensor data to a pre-trained machine learning model for failure prediction. In the event of errors in model loading, the system handles them gracefully and provides meaningful feedback.

3. Error Handling and Logging: Implemented robust error handling to manage issues related to model loading, ensuring the system remains resilient in production environments.

4. Integration with FastAPI: The application communicates seamlessly with the frontend via FastAPI, providing real-time responses with sensor data and model predictions.

5. Docker Deployment: The entire application, including database and model inference, is containerized using Docker for scalability, portability, and efficient deployment in production environments.
