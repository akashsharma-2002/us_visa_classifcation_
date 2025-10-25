#now this is training pipeline where we will integrate all the components together to form a pipeline

import sys
from us_visa_classifcation.exception import UsVisaException
from us_visa_classifcation.logger import logging
from us_visa_classifcation.components.data_ingestion import DataIngestion
from us_visa_classifcation.entity.config_entity import DataIngestionConfig
from us_visa_classifcation.entity.artifact_entity import DataIngestionArtifact

class TrainingPipeline:
    def __init__(self):
        self.data_ingestion_config=DataIngestionConfig()

    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            logging.info("starting data ingestion")
            data_ingestion=DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
            logging.info("completed data ingestion")
            return data_ingestion_artifact
        except Exception as e:
            raise UsVisaException(e,sys) from e
    def run_pipeline(self):
        try:
            data_ingestion_artifact=self.start_data_ingestion()
        except Exception as e:
            raise UsVisaException(e,sys) from e