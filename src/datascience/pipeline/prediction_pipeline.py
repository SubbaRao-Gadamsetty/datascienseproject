import joblib
import numpy as np
import pandas as pd
from pathlib import Path

class PredictionPipeline:
    def __init__(self, model_type='linear'):
        # Choose model: 'linear' or 'tree'
        if model_type == 'tree':
            self.model_path = Path('artifacts/model_trainer/decisiontreemodel.joblib')
        else:
            self.model_path = Path('artifacts/model_trainer/linearregressionmodel.joblib')
        
        self.model = joblib.load(self.model_path)

    def predict(self, input_data: np.ndarray):
        prediction = self.model.predict(input_data)
        return prediction
