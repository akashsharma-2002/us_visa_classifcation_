# from us_visa_classifcation.logger import logging
# from us_visa_classifcation.exception import UsVisaException
# import sys

# logging.info("checking logging module in exception file")

# try:
#     a=1/0
# except Exception as e:
#     raise UsVisaException(e,sys)

           
#testing data ingestion code
from us_visa_classifcation.pipeline.training_pipeline import TrainingPipeline

obj=TrainingPipeline()
obj.run_pipeline()