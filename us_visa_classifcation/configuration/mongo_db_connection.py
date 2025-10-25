import os
from us_visa_classifcation.constants import *
from us_visa_classifcation.exception import UsVisaException
from us_visa_classifcation.logger import logging
import sys
import pymongo #for mongo db connection
import certifi # to verify the ssl certificate of mongo db server. sometime timeout issue occurs without this

ca=certifi.where()
class MongoDBClient:
    client=None
    def __init__(self,database_name=DATABASE_NAME) -> None:
        try:
            if MongoDBClient.client is None:
                mongo_db_url= MONGODB_URL_KEY #mongodb url
                if mongo_db_url is None:
                    raise Exception("MongoDB URL is not provided")
                MongoDBClient.client=pymongo.MongoClient(mongo_db_url,tlsCAFile=ca) #establishing connection with mongo db server
            self.client=MongoDBClient.client
            self.database=self.client[database_name]
            self.database_name=database_name

            logging.info(f"MongoDB connection is established with database : {database_name}")

        except Exception as e:
            raise UsvisaException(e,sys) from e


    