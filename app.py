from flask import Flask, request, jsonify
import numpy as np
from src.datascience.pipeline.prediction_pipeline import PredictionPipeline
import os
import sqlite3

app = Flask(__name__)

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
        model_type = content.get("model", "linear")  # default: linear

        features = [
            content["MedInc"],
            content["HouseAge"],
            content["AveRooms"],
            content["AveBedrms"],
            content["Population"],
            content["AveOccup"],
            content["Latitude"],
            content["Longitude"]
        ]

        data = np.array([features])
        pipeline = PredictionPipeline(model_type=model_type)
        prediction = pipeline.predict(data)

        return jsonify({
            "model_used": model_type,
            "prediction": round(prediction[0], 3),
            "unit": "x 100,000"
        })

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
