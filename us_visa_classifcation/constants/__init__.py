#here i will define all constant  variables required for the project

import os 
from datetime import datetime

DATABASE_NAME="US_VISA"
COLLECTION_NAME="US_VISA_PROJECT"
MONGODB_URL_KEY="mongodb+srv://akashbest2002:Luciferbest@cluster0.8bolwpy.mongodb.net/"

PIPELINE_NAME: str = "us_visa"
ARTIFACT_DIR: str = "artifact"

MODEL_FILE_NAME = "model.pkl"

"""
DATA INGESTION CONSTANTS
"""

DATA_INGESTION_COLLECTION_NAME: str = "US_VISA_PROJECT" #same as collection name in mongo db
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2

TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"

FILE_NAME: str = "us_visa.csv"
MODEL_FILE_NAME: str = "model.pkl"  

