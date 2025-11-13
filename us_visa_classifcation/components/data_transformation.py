import sys
import numpy as np
import pandas as pd
from imblearn.combine import SMOTEENN
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler,OneHotEncoder,LabelEncoder,OrdinalEncoder,PowerTransformer
from sklearn.compose import ColumnTransformer

from us_visa_classifcation.constants import TARGET_COLUMN,SCHEMA_FILE_PATH,CURRENT_YEAR
from us_visa_classifcation.entity.config_entity import DataTransformationConfig
from us_visa_classifcation.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact
from us_visa_classifcation.exception import UsVisaException
from us_visa_classifcation.logger import logging
from us_visa_classifcation.utils.main_utils import read_yaml_file,save_numpy_array_data,save_object,drop_column
from us_visa_classifcation.entity.estimator import TargetValueMapping

class DataTransformation:
    def __init__(self,data_ingestion_artifact: DataIngestionArtifact,
                 data_validation_artifact: DataValidationArtifact,
                 data_transformation_config: DataTransformationConfig):
        try:
            logging.info(f"{'>>'*20} Data Transformation {'<<'*20}")
            self.data_ingestion_artifact= data_ingestion_artifact
            self.data_validation_artifact= data_validation_artifact
            self.data_transformation_config= data_transformation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise UsVisaException(e,sys)
    
    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise UsVisaException(e,sys)
    
    def get_data_transformer_object(self) -> Pipeline:
        try:
            logging.info("got num data")
            numeric_transformer=StandardScaler()
            oh_transformer=OneHotEncoder()
            ordinal_ecoder= OrdinalEncoder()
            oh_columns= self._schema_config['oh_columns']
            or_columns=self._schema_config['or_columns']
            transform_columns=self._schema_config.get('transform_columns') or []
            if not transform_columns:
                logging.info("No transform_columns specified in schema; defaulting to empty list")
            num_features=self._schema_config['num_features']

            logging.info("Creating preprocessor object")

            transform_pipe=Pipeline(steps=[
                ('transformer',PowerTransformer(method='yeo-johnson'))
            ])
            preprocessor= ColumnTransformer(
                [
                    ("OneHotEncoder",oh_transformer,oh_columns),
                    ("OrdinalEncoder",ordinal_ecoder,or_columns),
                    ("transformer",transform_pipe,transform_columns),
                    ("StandardScaler",numeric_transformer,num_features)
                ]
            )
            logging.info("Preprocessor object created successfully")

            logging.info("Applying oversampling technique")
            return preprocessor
        except Exception as e:
            raise UsVisaException(e,sys)
    
    def initiate_data_transformation(self)-> DataTransformationArtifact:
        try:
            if self.data_validation_artifact.validation_status:
                logging.info("Reading training and testing data for data transformation")
                preprocessor=self.get_data_transformer_object() 
                logging.info("Reading training data")

                train_df= DataTransformation.read_data(file_path=self.data_ingestion_artifact.trained_file_path)
                test_df= DataTransformation.read_data(file_path=self.data_ingestion_artifact.test_file_path)
                input_feature_train_df= train_df.drop(columns=[TARGET_COLUMN],axis=1)
                target_feature_train_df= train_df[TARGET_COLUMN]

                logging.info('Got train feature')
                input_feature_train_df['company_age']= CURRENT_YEAR-input_feature_train_df['yr_of_estab']
                logging.info('Got company age')
                columns_to_drop=self._schema_config['drop_columns']
                logging.info('Dropping columns')
                input_feature_train_df= drop_column(df=input_feature_train_df,columns=columns_to_drop)
                target_feature_train_df=target_feature_train_df.replace(TargetValueMapping().reverse_mapping())
                input_feature_test_df=test_df.drop(columns=[TARGET_COLUMN],axis=1)
                target_feature_test_df=test_df[TARGET_COLUMN]
                input_feature_test_df['company_age']= CURRENT_YEAR-input_feature_test_df['yr_of_estab']
                logging.info("addeded age")
                input_feature_test_df= drop_column(df=input_feature_test_df,columns=columns_to_drop)
                logging.info("dropped columns")
                target_feature_test_df=target_feature_test_df.replace(TargetValueMapping().reverse_mapping())

                logging.info("replaced the values in target column")
                input_feature_train_arr=preprocessor.fit_transform(input_feature_train_df)

                logging.info("Transforming training and testing data")
                input_feature_test_arr=preprocessor.transform(input_feature_test_df)
                logging.info("Saving transformed data")

                smt=SMOTEENN(sampling_strategy="minority")
                input_feature_train_final,target_feature_train_final=smt.fit_resample(input_feature_train_arr,target_feature_train_df)

                logging.info("saving transformed array")
                logging.info("Saving preprocessing object")

                input_feature_test_final,target_feature_test_final=smt.fit_resample(input_feature_test_arr,target_feature_test_df)
                logging.info("saving transformed array")

                train_arr=np.c_[input_feature_train_final,np.array(target_feature_train_final)]
                test_arr=np.c_[input_feature_test_final,np.array(target_feature_test_final)]

                save_object(self.data_transformation_config.transformed_object_file_path,preprocessor)
                save_numpy_array_data(self.data_transformation_config.transformed_train_file_path,array=train_arr)
                save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,array=test_arr)

                logging.info("Saved transformed array")

                datatransformation_artifact=DataTransformationArtifact(
                    transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                    transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
                    preprocessed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                )
                
                return datatransformation_artifact
            else:
                logging.info("Data validation failed hence exiting data transformation")
                raise Exception("Data Validation Failed")
        
        except Exception as e:
            raise UsVisaException(e,sys)
