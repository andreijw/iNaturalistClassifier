from common.constants import (
    DATASET_COLUMNS,
    SQUARE_SUFIX,
    MEDIUM_SUFIX,
    UNKNOWN,
    SPECIES_NAME,
)

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

    def _normalize_text(self, text: str) -> str:
        return str(text).lower().strip()

    def transform_json_to_dataset(self, json_content: str) -> pd.DataFrame:
        """Transform the JSON content to a dataset

        Args:
            json_content: JSON string containing the dataset

        Returns:
            pd.DataFrame: Transformed dataset
        """
        df = pd.json_normalize(json_content)

        df = df[DATASET_COLUMNS]
        df["photos"] = df["photos"].apply(
            lambda x: (
                [photo["url"].replace(SQUARE_SUFIX, MEDIUM_SUFIX) for photo in x]
                if isinstance(x, list)
                else []
            )
        )
        df["species_guess"] = df["species_guess"].apply(
            lambda x: self._normalize_text(x) if x else UNKNOWN
        )
        df["user.login"] = df["user.login"].apply(lambda x: x if x else UNKNOWN)
        df["taxon.name"] = df["taxon.name"].apply(
            lambda x: self._normalize_text(x) if x else UNKNOWN
        )

        return df

    def save_json_dataset(self, dataset_file_name: str, json_content: dict) -> None:
        """Save the dataset to the input path as a JSON file

        Args:
            dataset_file_name: Path to save the dataset
            json_content: JSON string containing the 'dataset' key and value
        """

        try:
            json_dataset = json_content["dataset"]
            dataset = [
                self.transform_json_to_dataset(fragment) for fragment in json_dataset
            ]
            df = pd.concat(dataset, ignore_index=True)
            df = df[df["taxon.rank"] == SPECIES_NAME]
            logging.debug(f"Found {len(df)} images")

            logger.info(f"Dataset saved to {dataset_file_name} from JSON")
            df.to_csv(dataset_file_name, index=False)
        except Exception as e:
            logger.error(
                f"Failed to save dataset to {dataset_file_name} from JSON: {e}"
            )
            raise
