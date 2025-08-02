import os
import urllib.request as request
from src.datascience import logger
import zipfile
import pandas as pd
from sklearn.datasets import fetch_california_housing


from src.datascience.entity.config_entity import (DataIngestionConfig)


## component-Data Ingestion

class DataIngestion:
    def __init__(self,config:DataIngestionConfig):
        self.config=config

    def extract_california_housing_data(self):
        """
        Extracts the California housing data from scikit-learn dataset
        and saves it to the specified directory.
        """
        # Create target directory if it doesn't exist
        os.makedirs(self.config.download_dir, exist_ok=True)

        # Load dataset
        housing = fetch_california_housing()
        df = pd.DataFrame(housing.data, columns=housing.feature_names)
        df['MedHouseValue'] = housing.target

        # Save to specified location inside download_dir
        csv_file_path = os.path.join(self.config.download_dir, 'california_housing.csv')
        df.to_csv(csv_file_path, index=False)

        logger.info(f"California housing data extracted to {csv_file_path}")
