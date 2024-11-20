import pandas as pd
import logging

logger = logging.getLogger(__name__)


class DatasetLoader:
    def __init__(self):
        pass

    def load_dataset(self, path: str) -> pd.DataFrame:
        """Load the dataset from the input path

        Args:
            path: Path to the dataset file

        Returns:
            pd.DataFrame: Loaded dataset
        """
        try:
            dataset = pd.read_csv(path)
            logger.info(f"Dataset loaded from {path}")
            return dataset
        except Exception as e:
            logger.error(f"Failed to load dataset from {path}: {e}")
            raise

    def save_json_to_dataset(self, dataset_path: str, json_dataset: str):
        """Save the dataset to the input path as a JSON file

        Args:
            dataset_path: Path to save the dataset
            json_dataset: JSON string containing the dataset
        """
        try:
            dataset = pd.read_json(json_dataset)
            dataset.to_csv(dataset_path, index=False)
            logger.info(f"Dataset saved to {dataset_path} from JSON")
        except Exception as e:
            logger.error(f"Failed to save dataset to {dataset_path} from JSON: {e}")
            raise
