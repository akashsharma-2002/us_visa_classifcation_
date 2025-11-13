import sys
from pandas import DataFrame
from sklearn.pipeline import Pipeline
from us_visa_classifcation.exception import UsVisaException
from us_visa_classifcation.logger import logging

class TargetValueMapping:
    def __init__(self)->None:
        try:
            self.target_mapping= {
                "CERTIFIED":1,
                "DENIED":0
            }
        except Exception as e:
            raise UsVisaException(e,sys)
    
    def to_dict(self)->dict:
        try:
            return self.target_mapping
        except Exception as e:
            raise UsVisaException(e,sys)
    
    def reverse_mapping(self)->dict:
        try:
            return {value:key for key,value in self.target_mapping.items()}
        except Exception as e:
            raise UsVisaException(e,sys)


class USvisaModel:
    def __init__(self, preprocessing_object: Pipeline, trained_model_object: object):
        """
        :param preprocessing_object: Input Object of preprocesser
        :param trained_model_object: Input Object of trained model 
        """
        self.preprocessing_object = preprocessing_object
        self.trained_model_object = trained_model_object

    def predict(self, dataframe: DataFrame) -> DataFrame:
        """
        Function accepts raw inputs and then transformed raw input using preprocessing_object
        which guarantees that the inputs are in the same format as the training data
        At last it performs prediction on transformed features
        """
        logging.info("Entered predict method of UTruckModel class")

        try:
            logging.info("Using the trained model to get predictions")

            transformed_feature = self.preprocessing_object.transform(dataframe)

            logging.info("Used the trained model to get predictions")
            return self.trained_model_object.predict(transformed_feature)

        except Exception as e:
            raise UsVisaException(e, sys) from e

    def __repr__(self):
        return f"{type(self.trained_model_object).__name__}()"

    def __str__(self):
        return f"{type(self.trained_model_object).__name__}()"
    