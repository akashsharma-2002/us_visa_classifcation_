#creating logger folder and __init__.py file inside it
#this will help in logging the events that happen during the execution of the code

import os
import logging
from from_root import from_root
from datetime import datetime

LOG_FILE= f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
logs_dir='logs'
logs_path=os.path.join(from_root(),logs_dir,LOG_FILE) #path to logs directory
os.makedirs(logs_dir,exist_ok=True) #creating logs directory if not exists

#now this is logic where logging will be done and above we create path for log file
logging.basicConfig(
    filename=logs_path,
    format="[%(asctime)s ] %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
)
