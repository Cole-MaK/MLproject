import os
import sys
from src.exception import CustomException
from src.logger import logging

import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from src.components.data_transform import DataTranformation, DataTranformationConfig
from src.components.model_train import ModelTrainerConfig, ModelTrainer

@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join('artifact','train.csv')
    test_data_path: str = os.path.join('artifact','test.csv')
    raw_data_path: str = os.path.join('artifact','data.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()
    
    def initiate_data_ingestion(self):
        logging.info("Entered the data Ingestion method or component")
        try:
            # read the dataset from anywhere
            df = pd.read_csv('notebook/data/stud.csv')
            logging.info("Read dataset as df")

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)

            #make raw data into csv
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

            # train test split and make data into csv
            logging.info("train test split initiated")
            train_set, test_set = train_test_split(df, test_size=.2, random_state=420)

            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

            logging.info('data ingestion | train test split complete')

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        
        except Exception as e:
            raise CustomException(e, sys)
        
if __name__ == '__main__':
    obj = DataIngestion()
    train_data, test_data = obj.initiate_data_ingestion()
    data_tranformation = DataTranformation()
    train_arr, test_arr, _ = data_tranformation.initiate_data_tranformation(train_data, test_data)

    model_trainer = ModelTrainer()
    print(model_trainer.initiate_model_trainer(train_arr, test_arr))

            