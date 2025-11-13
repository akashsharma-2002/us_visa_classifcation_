import json
import sys
import json
import pandas as pd
from evidently.dashboard import Dashboard
from evidently.tabs import DataDriftTab,CatTargetDriftTab
from evidently.model_profile import Profile
from evidently.profile_sections import DataDriftProfileSection

from pandas import DataFrame
from us_visa_classifcation.exception import UsVisaException
from us_visa_classifcation.logger import logging
from us_visa_classifcation.utils.main_utils import read_yaml_file,write_yaml_file
from us_visa_classifcation.entity.config_entity import DataValidationConfig
from us_visa_classifcation.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from us_visa_classifcation.constants import *

class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_config=data_validation_config
            self._schema_config=read_yaml_file(file_path=SCHEMA_FILE_PATH)
        except Exception as e:
            raise UsVisaException(e,sys)
        
    def validate_number_of_columns(self,dataframe:DataFrame)->bool:
        try:
            status=len(dataframe.columns)==len(self._schema_config['columns'])
            logging.info(f"Is number of columns are as per schema?-> {status}")
            return status
        except Exception as e:
            raise UsVisaException(e,sys)

    def is_columns_exist(self,df:DataFrame)->bool:
        try:
            dataframe_columns= df.columns
            missing_numerical_columns=[]
            missing_categorical_columns=[]
            for column in self._schema_config["numerical_columns"]:
                if column not in dataframe_columns:
                    missing_numerical_columns.append(column)
            if len(missing_numerical_columns)>0:
                logging.info(f"Missing numerical columns: {missing_numerical_columns}")
            for column in self._schema_config["categorical_columns"]:
                if column not in dataframe_columns:
                    missing_categorical_columns.append(column)
            if len(missing_categorical_columns)>0:
                logging.info(f"Missing categorical columns: {missing_categorical_columns}")

            return False if len(missing_categorical_columns)>0 or len(missing_numerical_columns)>0 else True
        except Exception as e:
            raise UsVisaException(e,sys)
    @staticmethod
    def read_data(file_path)->DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise UsVisaException(e,sys)
    
    def detect_dataset_drift(self,reference_df:DataFrame,current_df=DataFrame)->bool:
        try:
            data_drift_profile=Profile(sections=[DataDriftProfileSection()])
            data_drift_profile.calculate(reference_df,current_df)
            report =data_drift_profile.json()
            json_report=json.loads(report)

            write_yaml_file(file_path=self.data_validation_config.drift_report_file_path,
                            conten=json_report)
            n_features=json_report["data_drift"]["data"]["metrics"]["n_features"]
            n_drifted_features=json_report["data_drift"]["data"]["metrics"]["n_drifted_features"]
            logging.info(f"{n_drifted_features}/{n_features} features are drifted")
            drift_status=json_report["data_drift"]["data"]["metrics"]["dataset_drift"]
            return drift_status
        except Exception as e:
            raise UsVisaException(e,sys) from e
        
    def initiate_data_validation(self)->DataValidationArtifact: 
        try:
            validation_error_msg=""
            logging.info("starting data validation")
            train_df,test_df=(DataValidation.read_data(file_path=self.data_ingestion_artifact.trained_file_path),
                                  DataValidation.read_data(file_path=self.data_ingestion_artifact.test_file_path)
                            )
            status=self.validate_number_of_columns(dataframe=train_df)
            if not status:
                validation_error_msg=f"{validation_error_msg}Train dataframe does not contain all columns as per schema. \n"
            status=self.validate_number_of_columns(dataframe=test_df)
            if not status:
                validation_error_msg=f"{validation_error_msg}Test dataframe does not contain all columns as per schema. \n"
            status=self.is_columns_exist(df=train_df)
            if not status:
                validation_error_msg=f"{validation_error_msg}Train dataframe does not contain all columns as per schema. \n"
            status=self.is_columns_exist(df=test_df)
            if not status:
                validation_error_msg=f"{validation_error_msg}Test dataframe does not contain all columns as per schema. \n"
            validation_status=len(validation_error_msg)==0
            if validation_status:
                drift_status=self.detect_dataset_drift(train_df,test_df)
                if drift_status:
                    logging.info("Data drift found")
                else:
                    logging.info("No data drift found")
            else:
                logging.info(f"Data validation failed with following error message:\n{validation_error_msg}")
                raise Exception(validation_error_msg)
            data_validation_artifact=DataValidationArtifact(
                validation_status=validation_status,
                message=validation_error_msg,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )
            logging.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise UsVisaException(e,sys)
            
