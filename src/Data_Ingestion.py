import os
import sys
import pandas as pd
from google.cloud import storage
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import RAW_DIR, CONFIG_PATH
from utils.common_functions import read_yaml

logger = get_logger(__name__)

class Data_Ingestion:
    def __init__(self, config):
        self.config = config["Data Ingestion"]
        self.bucket_name = self.config["bucket_name"]
        self.bucket_file_names = self.config["bucket_file_name"]
        self.train_ratio = self.config["train_ratio"]
        
        os.makedirs(RAW_DIR, exist_ok=True)
        
        logger.info(f"Data Ingestion has started with {self.bucket_name} and the file name is {self.bucket_file_names}")
        
    def download_csv_from_gcp(self):
        try:
            client = storage.Client()
            bucket = client.bucket(self.bucket_name)
            
            for file_name in self.bucket_file_names:
                file_path = os.path.join(RAW_DIR, file_name)
                blob = bucket.blob(file_name)
                
                if "animelist" in file_name.lower():
                    logger.info("Streaming and sampling animelist.csv directly from GCP to save disk space...")
                    
                    # Stream directly from GCP without downloading full file to disk
                    with blob.open("rt", encoding="utf-8") as gcp_stream:
                        # Reduce row count to 1,000,000 (~150MB instead of 3GB)
                        df = pd.read_csv(gcp_stream, nrows=5000000)
                    
                    df.to_csv(file_path, index=False)
                    logger.info(f"Successfully saved sampled dataset ({len(df)} rows) to {file_path}")
                
                else:
                    blob.download_to_filename(file_path)
                    logger.info(f"Successfully downloaded {file_name} to {file_path}")
                    
        except Exception as e:
            logger.error("Error while downloading CSVs from GCP")
            raise CustomException("Failed to download CSV from GCP", sys) from e
    
    def run(self):
        try:
            logger.info("Starting the Data Ingestion Process")
            
            self.download_csv_from_gcp()
            
            logger.info("The Data Ingestion has been completed")
        
        except CustomException as ce:
            logger.error(f"Data Ingestion Failed: {str(ce)}")
            raise ce  # Re-raise so execution stops instantly if ingestion fails!
        
        finally:
            logger.info("Data Ingestion completed step execution")
    
if __name__=="__main__":
    config = read_yaml(CONFIG_PATH)
    data_ingestion_obj = Data_Ingestion(config)
    data_ingestion_obj.run()
        