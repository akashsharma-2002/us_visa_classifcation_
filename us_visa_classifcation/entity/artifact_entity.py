#here inside artifact_entity.py we will define all the artifact entities like data ingestion artifact ,data validation artifact ,data transformation artifact ,model trainer artifact etc.
#artifacts means the output of any component

from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    trained_file_path:str
    test_file_path:str
    
@dataclass
class DataValidationArtifact:
    validation_status:bool
    message:str
    drift_report_file_path:str

@dataclass
class DataTransformationArtifact:
    transformed_train_file_path:str
    transformed_test_file_path:str
    preprocessed_object_file_path:str

    