#now this is training pipeline where we will integrate all the components together to form a pipeline

import sys
from us_visa_classifcation.exception import UsVisaException
from us_visa_classifcation.logger import logging

from us_visa_classifcation.components.data_ingestion import DataIngestion
from us_visa_classifcation.components.data_validation import DataValidation
from us_visa_classifcation.components.data_transformation import DataTransformation
from us_visa_classifcation.components.model_trainer import ModelTrainer

from us_visa_classifcation.entity.config_entity import DataIngestionConfig
from us_visa_classifcation.entity.config_entity import DataValidationConfig
from us_visa_classifcation.entity.config_entity import DataTransformationConfig
from us_visa_classifcation.entity.config_entity import ModelTrainerConfig

from us_visa_classifcation.entity.artifact_entity import DataIngestionArtifact
from us_visa_classifcation.entity.artifact_entity import DataValidationArtifact
from us_visa_classifcation.entity.artifact_entity import DataTransformationArtifact
from us_visa_classifcation.entity.artifact_entity import ModelTrainerArtifact


class TrainingPipeline:
    def __init__(self):
        self.data_ingestion_config=DataIngestionConfig()
        self.data_validation_config=DataValidationConfig()
        self.data_transformation_config=DataTransformationConfig()
        self.model_trainer_config = ModelTrainerConfig()

    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            logging.info("starting data ingestion")
            data_ingestion=DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
            logging.info("completed data ingestion")
            return data_ingestion_artifact
        except Exception as e:
            raise UsVisaException(e,sys) from e
        
    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact
                              )->DataValidationArtifact:
        try:
            logging.info("starting data validation")
            data_validation=DataValidation(data_ingestion_artifact=data_ingestion_artifact,
                                           data_validation_config=self.data_validation_config)
            data_validation_artifact=data_validation.initiate_data_validation()
            logging.info("completed data validation")
            return data_validation_artifact
        except Exception as e:
            raise UsVisaException(e,sys) from e
    
    def start_data_transformation(self,data_ingestion_artifact:DataIngestionArtifact
                                 ,data_validation_artifact:DataValidationArtifact)->DataTransformationArtifact:
        try:
            logging.info("starting data transformation")
            data_transformation=DataTransformation(data_ingestion_artifact=data_ingestion_artifact,
                                                   data_transformation_config=self.data_transformation_config,
                                                   data_validation_artifact=data_validation_artifact)
            
            data_transformation_artifact=data_transformation.initiate_data_transformation()
            return data_transformation_artifact
        except Exception as e:
            raise UsVisaException(e,sys) from e
    
    def start_model_trainer(self, data_transformation_artifact: DataTransformationArtifact) -> ModelTrainerArtifact:
        """
        This method of TrainPipeline class is responsible for starting model training
        """
        try:
            model_trainer = ModelTrainer(data_transformation_artifact=data_transformation_artifact,
                                         model_trainer_config=self.model_trainer_config
                                         )
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            return model_trainer_artifact

        except Exception as e:
            raise UsVisaException(e, sys)
        
    def run_pipeline(self):
        try:
            data_ingestion_artifact=self.start_data_ingestion()
            data_validation_artifact=self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact=self.start_data_transformation(data_ingestion_artifact=data_ingestion_artifact,
                                                                         data_validation_artifact=data_validation_artifact)
            model_trainer_artifact=self.start_model_trainer(
                data_transformation_artifact=data_transformation_artifact
            )
            return model_trainer_artifact
        except Exception as e:
            raise UsVisaException(e,sys) from e
