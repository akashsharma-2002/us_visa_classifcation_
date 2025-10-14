#modular coding approach
#creating all the folders and files required for the project in one go
import os
from pathlib import Path

project_root="us_visa_classifcation" # project root folder name

list_of_files = [
    f"{project_root}/__init__.py",

    f"{project_root}/components/__init__.py",  #creating components folder and files inside it with __init__.py
    f"{project_root}/components/data_ingestion.py",
    f"{project_root}/components/data_validation.py",
    f"{project_root}/components/data_transformation.py",
    f"{project_root}/components/model_trainer.py",
    f"{project_root}/components/model_evaluation.py",
    f"{project_root}/components/model_pusher.py",

    f"{project_root}/configuration/__init__.py",

    f"{project_root}/constants/__init__.py",


    f"{project_root}/entity/__init__.py",
    f"{project_root}/entity/artifact_entity.py",
    f"{project_root}/entity/config_entity.py",

    f"{project_root}/exception/__init__.py",

    f"{project_root}/logger/__init__.py",

    f"{project_root}/pipeline/__init__.py",
    f"{project_root}/pipeline/training_pipeline.py",
    f"{project_root}/pipeline/prediction_pipeline.py",

    f"{project_root}/utils/__init__.py",
    f"{project_root}/utils/main_utils.py",

    "app.py",
    "requirements.txt",
    "setup.py",
    "Dockerfile",
    ".dockerignore",
    "config/model.yaml",
    "config/schema.yaml",

]

for filepath in list_of_files:
    filepath=Path(filepath) #this make sure the path is correct for any os
    file_dir,filename=os.path.split(filepath) #splitting the path into directory and filename
    #ex: file_dir= "us_visa_classifcation_/components" , filename="data_ingestion.py"

    if file_dir!="": #if directory is not empty
        os.makedirs(file_dir,exist_ok=True) 
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath)==0):
        with open(filepath,'w') as f:
            pass
    else:
        print(f"{filename} already exists")