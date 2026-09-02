import os
import sys
# import pandas as pd
from src.logger import get_logger
from src.custom_exception import CustomException
import yaml

logger = get_logger(__name__)

def read_yaml(file_path: str) -> dict:
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found at given path: [{file_path}]")
        
        with open(file_path, "r") as yaml_file:
            config = yaml.safe_load(yaml_file)
            logger.info("Loading the yaml file")
            return config
        
    except Exception as e:
        logger.error(f"Error while reading YAML File from [{file_path}]")
        raise CustomException(f"Failed to read the YAML File: {e}", sys) from e