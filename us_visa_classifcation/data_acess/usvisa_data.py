#here we will focus on getting data and converting it into pandas dataframe

import pandas as pd
from us_visa_classifcation.configuration.mongo_db_connection import MongoDBClient
from us_visa_classifcation.constants import *
from us_visa_classifcation.exception import UsVisaException
import sys
import numpy as np

class USVisaData:
    def __init__(self):
        try:
            self.mongo_client=MongoDBClient(database_name=DATABASE_NAME)
        except Exception as e:
            raise UsVisaException(e,sys)
        
    def export_collection_as_dataframe(self,collection_name:str,database_name:str=None)->pd.DataFrame:
        try:
            if database_name is None:
                collection=self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client.database[database_name][collection_name]
            
            df=pd.DataFrame(list(collection.find())) #getting all the data from mongo db collection and converting it into pandas dataframe
            if "_id" in df.columns:
                df=df.drop(columns=["_id"],axis=1)
            df.replace({"na":np.NAN},inplace=True) #replacing "na" with NAN as pandas understand NAN as empty but na as string.
            return df
        except Exception as e:
            raise UsVisaException(e,sys)