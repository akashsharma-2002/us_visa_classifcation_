import os
import sys

from pandas import DataFrame
from sklearn.model_selection import train_test_split

from us_visa_classifcation.entity.config_entity import DataIngestionConfig
from us_visa_classifcation.entity.artifact_entity import DataIngestionArtifact
from us_visa_classifcation.exception import UsVisaException
from us_visa_classifcation.logger import logging
from us_visa_classifcation.data_acess.usvisa_data import USVisaData


class DataIngestion:
    def __init__(self,data_ingestion_config=DataIngestionConfig()):
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise UsVisaException(e,sys)
    
    def export_data_into_feature_store(self)->DataFrame:
        try:
            logging.info("Exporting data from mongodb to feature store")
            usvisa_data=USVisaData()
            dataframe=usvisa_data.export_collection_as_dataframe(collection_name=self.data_ingestion_config.collection_name)
            feature_store_file_path=self.data_ingestion_config.feature_store_file_path
            dir_path=os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            logging.info("Saving exported data into feature store")
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            return dataframe
        except Exception as e:
            raise UsVisaException(e,sys)
        
    def split_data_as_train_test(self,dataframe:DataFrame)->None:
        logging.info("Entered split data as train test method for data ingestion class")
        try:
            train_set,test_set=train_test_split(dataframe,test_size=self.data_ingestion_config.train_test_split_ratio,random_state=42)
            logging.info("Performed train test split on the dataframe")
            logging.info("Exited split data as train test method for data ingestion class")

            dir_path=os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path,exist_ok=True)

            logging.info("exporting training and testing data file  ")
            train_set.to_csv(self.data_ingestion_config.training_file_path,index=False,header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path,index=False,header=True)
            logging.info("exported training and testing data file  ")
        except Exception as e:
            raise UsVisaException(e,sys) from e

    def initiate_data_ingestion(self):
        logging.info("Initiating data ingestion")
        try:
            dataframe=self.export_data_into_feature_store()
            logging.info("Exported data from mongodb to feature store")
            self.split_data_as_train_test(dataframe=dataframe)
            logging.info("Split data into train and test successfully")
            
            data_ingestion_artifact=DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
            )
            logging.info(f"Data Ingestion artifact:{data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise UsVisaException(e,sys) from e 
