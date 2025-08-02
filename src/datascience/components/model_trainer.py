from matplotlib.widgets import Lasso
import pandas as pd
import os

from sklearn.tree import DecisionTreeRegressor
from src.datascience import logger
from sklearn.linear_model import Lasso
import joblib

from src.datascience.entity.config_entity import ModelTrainerConfig


class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config

    def trainLinearRegressionModel(self):
        train_data = pd.read_csv(self.config.train_data_path)
        test_data = pd.read_csv(self.config.test_data_path)


        train_x = train_data.drop([self.config.target_column], axis=1)
        test_x = test_data.drop([self.config.target_column], axis=1)
        train_y = train_data[[self.config.target_column]]
        test_y = test_data[[self.config.target_column]]

        lr = Lasso(alpha=self.config.alpha, random_state=42)
        lr.fit(train_x, train_y)

        joblib.dump(lr, os.path.join(self.config.root_dir, self.config.lr_model_name))

    

    def trainDecisionTreeModel(self):
        train_data = pd.read_csv(self.config.train_data_path)
        test_data = pd.read_csv(self.config.test_data_path)


        train_x = train_data.drop([self.config.target_column], axis=1)
        test_x = test_data.drop([self.config.target_column], axis=1)
        train_y = train_data[[self.config.target_column]]
        test_y = test_data[[self.config.target_column]]

        dt = DecisionTreeRegressor(max_depth=self.config.max_depth, min_samples_split=self.config.min_samples_split, min_samples_leaf=self.config.min_samples_leaf, random_state=42)
        dt.fit(train_x, train_y)

        joblib.dump(dt, os.path.join(self.config.root_dir, self.config.dt_model_name))


    