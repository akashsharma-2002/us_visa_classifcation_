import os
import sys
import numpy as np
import pandas as pd
import dill  #save or load python object
import yaml  #to read/write yaml file
from us_visa_classifcation.exception import UsVisaException
from us_visa_classifcation.logger import logging

def read_yaml_file(file_path:str)->dict:
    try:
        with open(file_path,'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise UsVisaException(e,sys)

def write_yaml_file(file_path:str,conten:object , replace:bool=False)->None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        file_dir=os.path.dirname(file_path)
        os.makedirs(file_dir,exist_ok=True)
        with open(file_path,'w') as yaml_file:
            yaml.dump(conten,yaml_file)
    except Exception as e:
        raise UsVisaException(e,sys)
    
def save_object(file_path:str,obj:object)->None:
    logging.info("Entered the save_object method of main_utils")
    try:
        file_dir=os.path.dirname(file_path)
        os.makedirs(file_dir,exist_ok=True)
        with open(file_path,'wb') as file_obj:
            dill.dump(obj,file_obj)
        logging.info("Exited the save_object method of main_utils")
    except Exception as e:
        raise UsVisaException(e,sys)
    
def load_object(file_path:str)->object:
    logging.info("Entered the load_object method of main_utils")
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file {file_path} does not exist")
        with open(file_path,'rb') as file_obj:
            obj=dill.load(file_obj)
        logging.info("Exited the load_object method of main_utils")
        return obj
    except Exception as e:
        raise UsVisaException(e,sys)

def save_numpy_array_data(file_path:str,array:np.array)->None: 
    try:
        file_dir=os.path.dirname(file_path)
        os.makedirs(file_dir,exist_ok=True)
        with open(file_path,'wb') as file_obj:
            np.save(file_obj,array)
    except Exception as e:
        raise UsVisaException(e,sys) 

def drop_column(df:pd.DataFrame, columns:list)->pd.DataFrame:
    """
    Drops the specified columns from the provided dataframe.
    """
    try:
        missing_df = df is None
        missing_cols = columns is None
        if missing_df or missing_cols:
            raise ValueError("Both df and columns parameters must be provided")
        return df.drop(columns=columns,axis=1)
    except Exception as e:
        raise UsVisaException(e,sys)
