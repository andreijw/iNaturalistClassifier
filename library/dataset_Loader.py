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

    def save_json_to_dataset(self, dataset_path: str, json_content: str):
        """Save the dataset to the input path as a JSON file

        Args:
            dataset_path: Path to save the dataset
            json_content: JSON string containing the dataset
        """
        try:
            json_dataset = json_content["dataset"]
            dataset = [
                pd.json_normalize(dataset_fragment) for dataset_fragment in json_dataset
            ]
            df = pd.concat(dataset, ignore_index=True)
            print(df.head(10))
            breakpoint()
            logging.debug(f"Found {len(df)} images")

            logger.info(f"Dataset saved to {dataset_path} from JSON")
        except Exception as e:
            logger.error(f"Failed to save dataset to {dataset_path} from JSON: {e}")
            raise
