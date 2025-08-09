from flask import Flask, request, jsonify, Response
import numpy as np
from src.datascience.pipeline.prediction_pipeline import PredictionPipeline
import os
import sqlite3
import json
import subprocess
import threading
from datetime import datetime
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

# --- Pydantic Model for Training Data Input ---
class TrainingDataInput(BaseModel):
    MedInc: float
    HouseAge: float
    AveRooms: float
    AveBedrms: float
    Population: float
    AveOccup: float
    Latitude: float
    Longitude: float
    MedHouseValue: float  # Target variable for training

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
        
        # Validate input data
        if isinstance(new_data, list):
            # Multiple training samples
            validated_data = [TrainingDataInput(**sample) for sample in new_data]
        else:
            # Single training sample
            validated_data = [TrainingDataInput(**new_data)]
        
        # Save new data for retraining (proper JSON format)
        timestamp = datetime.now().isoformat()
        training_batch = {
            "timestamp": timestamp,
            "data": [sample.dict() for sample in validated_data]
        }
        
        # Ensure directory exists
        os.makedirs("artifacts/retraining", exist_ok=True)
        
        # Save to a JSON file with timestamp
        filename = f"artifacts/retraining/new_training_data_{timestamp.replace(':', '-')}.json"
        with open(filename, "w") as f:
            json.dump(training_batch, f, indent=2)
        
        # Log the retraining request
        log_retraining_request(len(validated_data), filename)
        
        # Trigger retraining in background (non-blocking)
        def run_retraining():
            try:
                result = subprocess.run(
                    ["python", "main.py"], 
                    capture_output=True, 
                    text=True, 
                    timeout=300  # 5 minute timeout
                )
                log_retraining_result(result.returncode == 0, result.stdout, result.stderr)
            except subprocess.TimeoutExpired:
                log_retraining_result(False, "", "Retraining timed out after 5 minutes")
            except Exception as e:
                log_retraining_result(False, "", str(e))
        
        # Start retraining in background thread
        retraining_thread = threading.Thread(target=run_retraining)
        retraining_thread.daemon = True
        retraining_thread.start()
        
        return jsonify({
            "status": "Retraining triggered successfully!",
            "samples_received": len(validated_data),
            "training_file": filename,
            "message": "Retraining is running in the background. Check logs for progress."
        })
        
    except ValidationError as ve:
        return jsonify({
            "error": "Invalid training data format",
            "details": ve.errors()
        }), 422
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def log_retraining_request(sample_count, filename):
    """Log retraining request to database"""
    try:
        conn = sqlite3.connect("prediction_logs.db")
        cursor = conn.cursor()
        
        # Create retraining logs table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS retraining_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                sample_count INTEGER,
                training_file TEXT,
                status TEXT,
                stdout TEXT,
                stderr TEXT
            )
        """)
        
        cursor.execute("""
            INSERT INTO retraining_logs (timestamp, sample_count, training_file, status)
            VALUES (?, ?, ?, ?)
        """, (datetime.now().isoformat(), sample_count, filename, "STARTED"))
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error logging retraining request: {e}")

def log_retraining_result(success, stdout, stderr):
    """Log retraining result to database"""
    try:
        conn = sqlite3.connect("prediction_logs.db")
        cursor = conn.cursor()
        
        status = "COMPLETED" if success else "FAILED"
        cursor.execute("""
            UPDATE retraining_logs 
            SET status = ?, stdout = ?, stderr = ?
            WHERE id = (SELECT MAX(id) FROM retraining_logs)
        """, (status, stdout, stderr))
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error logging retraining result: {e}")

# --- Get Retraining Status Endpoint ---
@app.route("/retrain/status", methods=["GET"])
def retrain_status():
    try:
        conn = sqlite3.connect("prediction_logs.db")
        cursor = conn.cursor()
        
        # Get latest retraining logs
        cursor.execute("""
            SELECT timestamp, sample_count, status, stdout, stderr 
            FROM retraining_logs 
            ORDER BY id DESC 
            LIMIT 5
        """)
        logs = cursor.fetchall()
        conn.close()
        
        return jsonify({
            "recent_retraining_logs": [
                {
                    "timestamp": log[0],
                    "sample_count": log[1],
                    "status": log[2],
                    "stdout": log[3][:500] if log[3] else None,  # Truncate long outputs
                    "stderr": log[4][:500] if log[4] else None
                }
                for log in logs
            ]
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)


    