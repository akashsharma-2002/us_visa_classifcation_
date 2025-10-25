#here inside config_entity.py we will create all the configuration related entities
# creating directory which we have assinged in constant we will create that directory here.

import os
from us_visa_classifcation.constants import *
from dataclasses import dataclass
from datetime import datetime

TIMESTAMP:str= datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

@dataclass #this we use to create class without init method basically we make class but no constructor
class TrainingPipelineConfig:
    pipeline_name:str= PIPELINE_NAME
    artifact_dir:str=os.path.join(ARTIFACT_DIR,TIMESTAMP) #artifact dir where output will be storeed.
    timestamp: str= TIMESTAMP

trainingPipelineConfig: TrainingPipelineConfig = TrainingPipelineConfig()   #creating instance of trainingpipelineconfig class and storing it into variable

@dataclass
class DataIngestionConfig:
    data_ingestion_dir:str=os.path.join(trainingPipelineConfig.artifact_dir,DATA_INGESTION_DIR_NAME)
    feature_store_file_path:str=os.path.join(data_ingestion_dir,DATA_INGESTION_FEATURE_STORE_DIR,FILE_NAME)
    training_file_path:str=os.path.join(data_ingestion_dir,DATA_INGESTION_INGESTED_DIR,TRAIN_FILE_NAME)
    testing_file_path:str=os.path.join(data_ingestion_dir,DATA_INGESTION_INGESTED_DIR,TEST_FILE_NAME)
    train_test_split_ratio:float=DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
    collection_name:str=DATA_INGESTION_COLLECTION_NAME
