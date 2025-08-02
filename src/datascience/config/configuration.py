from src.datascience.constants import *
from src.datascience.utils.common import read_yaml, create_directories

from src.datascience.entity.config_entity import (DataIngestionConfig,DataValidationConfig,
                                                  DataTransformationConfig,ModelTrainerConfig,
                                                  ModelEvaluationConfig)

class ConfigurationManager:
    def __init__(self,
                 config_filepath=CONFIG_FILE_PATH,
                 params_filepath = PARAMS_FILE_PATH,
                 schema_filepath = SCHEMA_FILE_PATH):
        self.config=read_yaml(config_filepath)
        self.params=read_yaml(params_filepath)
        self.schema=read_yaml(schema_filepath)

        create_directories([self.config.artifacts_root])


    def get_data_ingestion_config(self)-> DataIngestionConfig:
        config=self.config.data_ingestion
        create_directories([config.root_dir])

        data_ingestion_config=DataIngestionConfig(
            root_dir=config.root_dir,
            download_dir=config.download_dir
        )
        return data_ingestion_config
    
    def get_data_validation_config(self) -> DataValidationConfig:
        config = self.config.data_validation
        schema = self.schema.COLUMNS

        create_directories([config.root_dir])

        data_validation_config = DataValidationConfig(
            root_dir=config.root_dir,
            STATUS_FILE=config.STATUS_FILE,
            input_data_dir = config.input_data_dir,
            all_schema=schema,
        )

        return data_validation_config
    
    def get_data_transformation_config(self) -> DataTransformationConfig:
        config=self.config.data_transformation
        create_directories([config.root_dir])
        data_transformation_config=DataTransformationConfig(
            root_dir=config.root_dir,
            data_path=config.data_path
        )
        return data_transformation_config
    
    def get_model_trainer_config(self) -> ModelTrainerConfig:
        config = self.config.model_trainer
        paramsLasso = self.params.Lasso
        paramsDecisionTree = self.params.DecisionTree
        schema =  self.schema.TARGET_COLUMN

        create_directories([config.root_dir])

        model_trainer_config = ModelTrainerConfig(
            root_dir=config.root_dir,
            train_data_path = config.train_data_path,
            test_data_path = config.test_data_path,
            lr_model_name = config.lr_model_name,
            alpha = paramsLasso.alpha,
            dt_model_name = config.dt_model_name,
            max_depth = paramsDecisionTree.max_depth,   
            min_samples_split = paramsDecisionTree.min_samples_split,
            min_samples_leaf = paramsDecisionTree.min_samples_leaf,
            target_column = schema.name
            
        )

        return model_trainer_config
    
    def get_model_evaluation_config(self) -> ModelEvaluationConfig:
        config=self.config.model_evaluation
        paramsLasso=self.params.Lasso
        paramsDecisionTree = self.params.DecisionTree
        schema=self.schema.TARGET_COLUMN

        create_directories([config.root_dir])

        model_evaluation_config=ModelEvaluationConfig(
            root_dir=config.root_dir,
            test_data_path=config.test_data_path,
            alpha=paramsLasso.alpha,
            max_depth = paramsDecisionTree.max_depth,   
            min_samples_split = paramsDecisionTree.min_samples_split,
            min_samples_leaf = paramsDecisionTree.min_samples_leaf,
            lr_model_path = config.lr_model_path,
            lr_metric_file_name = config.lr_metric_file_name,
            dt_model_path = config.dt_model_path,
            dt_metric_file_name = config.dt_metric_file_name,
            target_column = schema.name,
            mlflow_uri="https://dagshub.com/SubbaRao-Gadamsetty/datascienseproject.mlflow"

        )
        return model_evaluation_config