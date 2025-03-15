import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get data directories from environment variables
DATA_DIR = os.getenv("DATA_DIRECTORY", "data")
RAW_DATA_DIR = os.getenv("RAW_DATA_DIRECTORY", "data/raw")
PROCESSED_DATA_DIR = os.getenv("PROCESSED_DATA_DIRECTORY", "data/processed")


def load_json(filename: str, directory: Optional[str] = None) -> Dict[str, Any]:
    """
    Load data from a JSON file.
    
    Args:
        filename (str): Name of the JSON file to load
        directory (str, optional): Directory where the file is located. 
                                  If None, uses PROCESSED_DATA_DIR from .env
    
    Returns:
        Dict[str, Any]: The loaded JSON data as a dictionary
    
    Raises:
        FileNotFoundError: If the file doesn't exist
        json.JSONDecodeError: If the file contains invalid JSON
    """
    if directory is None:
        directory = PROCESSED_DATA_DIR
    
    # Ensure the filename has .json extension
    if not filename.endswith('.json'):
        filename += '.json'
    
    # Create the full file path
    file_path = Path(directory) / filename
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"Successfully loaded data from {file_path}")
        return data
    except FileNotFoundError:
        print(f"Error: File {file_path} not found")
        raise
    except json.JSONDecodeError:
        print(f"Error: File {file_path} contains invalid JSON")
        raise


def save_json(data: Dict[str, Any], filename: str, directory: Optional[str] = None, indent: int = 4) -> bool:
    """
    Save data to a JSON file.
    
    Args:
        data (Dict[str, Any]): The data to save
        filename (str): Name of the JSON file to save to
        directory (str, optional): Directory where the file should be saved.
                                  If None, uses PROCESSED_DATA_DIR from .env
        indent (int): Number of spaces for indentation in the JSON file
    
    Returns:
        bool: True if the data was saved successfully, False otherwise
    """
    if directory is None:
        directory = PROCESSED_DATA_DIR
    
    # Ensure the filename has .json extension
    if not filename.endswith('.json'):
        filename += '.json'
    
    # Create the directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)
    
    # Create the full file path
    file_path = Path(directory) / filename
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=indent)
        print(f"Successfully saved data to {file_path}")
        return True
    except Exception as e:
        print(f"Error saving data to {file_path}: {e}")
        return False


def get_data_directory(data_type: str = "processed") -> str:
    """
    Get the appropriate data directory based on data type.
    
    Args:
        data_type (str): Type of data directory to get ('raw' or 'processed')
    
    Returns:
        str: Path to the requested data directory
    """
    if data_type.lower() == "raw":
        return RAW_DATA_DIR
    elif data_type.lower() == "processed":
        return PROCESSED_DATA_DIR
    else:
        return DATA_DIR
