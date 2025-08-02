from dataclasses import dataclass
from pathlib import Path

@dataclass
class DataIngestionConfig:
    root_dir: Path
    download_dir: Path


@dataclass
class DataValidationConfig:
    root_dir:Path
    STATUS_FILE:str
    input_data_dir:Path
    all_schema:dict

@dataclass
class DataTransformationConfig:
    root_dir: Path
    data_path: Path

@dataclass
class ModelTrainerConfig:
    root_dir: Path
    train_data_path: Path
    test_data_path: Path
    lr_model_name: str
    alpha: float
    dt_model_name: str
    max_depth: int
    min_samples_split: int
    min_samples_leaf: int
    target_column: str

@dataclass
class ModelEvaluationConfig:
    root_dir: Path
    test_data_path: Path
    lr_model_path: Path
    alpha: float
    max_depth: int
    min_samples_split: int
    min_samples_leaf: int 
    lr_metric_file_name: Path
    dt_model_path: Path
    dt_metric_file_name: Path
    target_column: str
    mlflow_uri: str