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
