from flask import Flask, request, jsonify, Response
import numpy as np
from src.datascience.pipeline.prediction_pipeline import PredictionPipeline
import os
import sqlite3
from pydantic import BaseModel, ValidationError
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# --- Pydantic Model for Input Validation ---
class PredictInput(BaseModel):
    MedInc: float
    HouseAge: float
    AveRooms: float
    AveBedrms: float
    Population: float
    AveOccup: float
    Latitude: float
    Longitude: float
    model: str = "linear"

# --- Prometheus Counter ---
PREDICTION_COUNTER = Counter('prediction_requests_total', 'Total prediction requests', ['model'])

@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "API is up and running!"})

@app.route('/train',methods=['GET'])  # route to train the pipeline
def training():
    os.system("python main.py")
    return "Training Successful!" 

@app.route("/predict", methods=["POST"])
def predict():
    try:
        content = request.get_json()
        # Validate input using Pydantic
        validated = PredictInput(**content)
        features = [
            validated.MedInc,
            validated.HouseAge,
            validated.AveRooms,
            validated.AveBedrms,
            validated.Population,
            validated.AveOccup,
            validated.Latitude,
            validated.Longitude
        ]
        data = np.array([features])
        pipeline = PredictionPipeline(model_type=validated.model)
        prediction = pipeline.predict(data)

        # Increment Prometheus metric
        PREDICTION_COUNTER.labels(model=validated.model).inc()

        return jsonify({
            "model_used": validated.model,
            "prediction": round(prediction[0], 3),
            "unit": "x 100,000"
        })

    except ValidationError as ve:
        return jsonify({"error": ve.errors()}), 422
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/metrics", methods=["GET"])
def metrics():
    conn = sqlite3.connect("prediction_logs.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*), MAX(id) FROM prediction_logs")
    count, last_id = cursor.fetchone()
    cursor.execute("SELECT model_type, prediction FROM prediction_logs ORDER BY id DESC LIMIT 1")
    last = cursor.fetchone()
    conn.close()
    return jsonify({
        "total_predictions": count,
        "last_prediction_id": last_id,
        "last_prediction": last[1] if last else None,
        "last_model_type": last[0] if last else None
    })

# --- Prometheus Metrics Endpoint ---
@app.route("/metrics/prometheus")
def prometheus_metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

# --- Model Retraining Trigger Endpoint ---
@app.route("/retrain", methods=["POST"])
def retrain():
    try:
        new_data = request.get_json()
        # Save new data for retraining (append to a file)
        with open("new_training_data.json", "a") as f:
            f.write(str(new_data) + "\n")
        # Trigger retraining (could be improved to use subprocess or background job)
        os.system("python main.py --retrain")
        return jsonify({"status": "Retraining triggered!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)