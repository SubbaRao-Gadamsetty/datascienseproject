import os
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from urllib.parse import urlparse
import mlflow
import mlflow.sklearn
import numpy as np
import joblib
import sqlite3
from pathlib import Path

from src.datascience.entity.config_entity import ModelEvaluationConfig
from src.datascience.constants import *
from src.datascience.utils.common import read_yaml, create_directories, save_json
from src.datascience import logger

os.environ["MLFLOW_TRACKING_URI"] = "http://ec2-52-86-214-74.compute-1.amazonaws.com:5000/"
logger.info('Set MLFLOW_TRACKING_URI environment variable.')

# SQLite setup for logging predictions
DB_PATH = "prediction_logs.db"
logger.info(f"Setting up SQLite DB at {DB_PATH}")
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
logger.info("Connected to SQLite DB.")

cursor.execute('''
    CREATE TABLE IF NOT EXISTS prediction_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        model_type TEXT,
        input_data TEXT,
        prediction TEXT,
        metrics TEXT
    )
''')
logger.info("Ensured prediction_logs table exists in SQLite DB.")
conn.commit()

class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        logger.info(f"Initializing ModelEvaluation with config: {config}")
        self.config = config

    def eval_metrics(self, actual, pred):
        logger.info(f"Evaluating metrics for actual: {actual.shape}, pred: {pred.shape}")
        rmse = np.sqrt(mean_squared_error(actual, pred))
        logger.info(f"Computed RMSE: {rmse}")
        mae = mean_absolute_error(actual, pred)
        logger.info(f"Computed MAE: {mae}")
        r2 = r2_score(actual, pred)
        logger.info(f"Computed R2: {r2}")
        return rmse, mae, r2

    def log_prediction(self, model_type, input_data, prediction, metrics):
        logger.info(f"Logging prediction for model: {model_type}")
        cursor.execute(
            "INSERT INTO prediction_logs (model_type, input_data, prediction, metrics) VALUES (?, ?, ?, ?)",
            (model_type, str(input_data), str(prediction), str(metrics))
        )
        conn.commit()
        logger.info("Prediction logged to SQLite DB.")

    def log_lr_model_into_mlflow(self):
        try:
            logger.info("Starting LR model evaluation...")

            test_data = pd.read_csv(self.config.test_data_path)
            logger.info(f"Loaded test data from: {self.config.test_data_path}")
            model = joblib.load(self.config.lr_model_path)
            logger.info(f"Loaded LR model from: {self.config.lr_model_path}")

            test_x = test_data.drop([self.config.target_column], axis=1)
            logger.info(f"Prepared test_x with shape: {test_x.shape}")
            test_y = test_data[[self.config.target_column]]
            logger.info(f"Prepared test_y with shape: {test_y.shape}")

            mlflow.set_registry_uri(self.config.mlflow_uri)
            logger.info(f"Set MLflow registry URI: {self.config.mlflow_uri}")
            tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme
            logger.info(f"MLflow tracking URL type: {tracking_url_type_store}")

            with mlflow.start_run():
                logger.info("Started MLflow run.")

                predicted_qualities = model.predict(test_x)
                logger.info(f"Predicted qualities: {predicted_qualities[:5]}...")

                (rmse, mae, r2) = self.eval_metrics(test_y, predicted_qualities)
                logger.info(f"Evaluation metrics - RMSE: {rmse}, MAE: {mae}, R2: {r2}")

                scores = {"rmse": rmse, "mae": mae, "r2": r2}
                save_json(path=Path(self.config.lr_metric_file_name), data=scores)
                logger.info(f"Saved metrics to {self.config.lr_metric_file_name}")

                mlflow.log_param("alpha", self.config.alpha)
                logger.info(f"Logged param alpha: {self.config.alpha}")

                mlflow.log_metric("rmse", rmse)
                mlflow.log_metric("r2", r2)
                mlflow.log_metric("mae", mae)
                logger.info("Logged metrics to MLflow.")

                self.log_prediction(
                    model_type="LinearRegression",
                    input_data=test_x.head().to_json(),
                    prediction=predicted_qualities[:5].tolist(),
                    metrics=scores
                )

                if tracking_url_type_store != "file":
                    logger.info("Registering model in MLflow Model Registry.")
                    mlflow.sklearn.log_model(model, "model", registered_model_name="LinearRegressionModel")
                else:
                    logger.info("Logging model to MLflow without registry.")
                    mlflow.sklearn.log_model(model, "model")

        except Exception as e:
            logger.error(f"Failed to evaluate LR model: {e}", exc_info=True)

    def log_dt_model_into_mlflow(self):
        try:
            logger.info("Starting DT model evaluation...")

            test_data = pd.read_csv(self.config.test_data_path)
            logger.info(f"Loaded test data from: {self.config.test_data_path}")
            model = joblib.load(self.config.dt_model_path)
            logger.info(f"Loaded DT model from: {self.config.dt_model_path}")

            test_x = test_data.drop([self.config.target_column], axis=1)
            logger.info(f"Prepared test_x with shape: {test_x.shape}")
            test_y = test_data[[self.config.target_column]]
            logger.info(f"Prepared test_y with shape: {test_y.shape}")

            mlflow.set_registry_uri(self.config.mlflow_uri)
            logger.info(f"Set MLflow registry URI: {self.config.mlflow_uri}")
            tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme
            logger.info(f"MLflow tracking URL type: {tracking_url_type_store}")

            with mlflow.start_run():
                logger.info("Started MLflow run.")

                predicted_qualities = model.predict(test_x)
                logger.info(f"Predicted qualities: {predicted_qualities[:5]}...")

                (rmse, mae, r2) = self.eval_metrics(test_y, predicted_qualities)
                logger.info(f"Evaluation metrics - RMSE: {rmse}, MAE: {mae}, R2: {r2}")

                scores = {"rmse": rmse, "mae": mae, "r2": r2}
                save_json(path=Path(self.config.dt_metric_file_name), data=scores)
                logger.info(f"Saved metrics to {self.config.dt_metric_file_name}")

                mlflow.log_param("max_depth", self.config.max_depth)
                logger.info(f"Logged param max_depth: {self.config.max_depth}")
                mlflow.log_param("min_samples_split", self.config.min_samples_split)
                logger.info(f"Logged param min_samples_split: {self.config.min_samples_split}")
                mlflow.log_param("min_samples_leaf", self.config.min_samples_leaf)
                logger.info(f"Logged param min_samples_leaf: {self.config.min_samples_leaf}")

                mlflow.log_metric("rmse", rmse)
                mlflow.log_metric("r2", r2)
                mlflow.log_metric("mae", mae)
                logger.info("Logged metrics to MLflow.")

                self.log_prediction(
                    model_type="DecisionTree",
                    input_data=test_x.head().to_json(),
                    prediction=predicted_qualities[:5].tolist(),
                    metrics=scores
                )

                if tracking_url_type_store != "file":
                    logger.info("Registering model in MLflow Model Registry.")
                    mlflow.sklearn.log_model(model, "model", registered_model_name="DecisionTreeModel")
                else:
                    logger.info("Logging model to MLflow without registry.")
                    mlflow.sklearn.log_model(model, "model")
        except Exception as e:
            logger.error(f"Failed to evaluate DT model: {e}", exc_info=True)

print("ModelEvaluation class is ready for use.")