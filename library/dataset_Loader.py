from common.constants import (
    DATASET_COLUMNS,
    SQUARE_SUFIX,
    MEDIUM_SUFIX,
    UNKNOWN,
    SPECIES_NAME,
    PHOTOS,
    TAXON_NAME,
    TAXON_RANK,
    SPECIES_GUESSES,
    USER_LOGIN,
    ENCODED_LABELS,
)

import pandas as pd
import logging
import os
from library.base_io import BaseIO
from tqdm import tqdm
from sklearn.preprocessing import OneHotEncoder
from library.request_helper import get_request
from numpy.typing import NDArray

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

    def normalize_text(self, text: str) -> str:
        return str(text).lower().strip()

    @staticmethod
    def encode_labels(labels: NDArray) -> dict:
        onehot_encoder = OneHotEncoder()
        onehot_labels = onehot_encoder.fit_transform(labels.reshape(-1, 1))
        species_to_onehot = {
            species: onehot_labels[i] for i, species in enumerate(labels)
        }
        return species_to_onehot

    def transform_json_to_dataset(self, json_content: str) -> pd.DataFrame:
        """Transform the JSON content to a dataset

        Args:
            json_content: JSON string containing the dataset

        Returns:
            pd.DataFrame: Transformed dataset
        """
        df = pd.json_normalize(json_content)

        df = df[DATASET_COLUMNS]
        df[PHOTOS] = df[PHOTOS].apply(
            lambda x: (
                [photo["url"].replace(SQUARE_SUFIX, MEDIUM_SUFIX) for photo in x]
                if isinstance(x, list)
                else []
            )
        )
        df[SPECIES_GUESSES] = df[SPECIES_GUESSES].apply(
            lambda x: self.normalize_text(x) if x else UNKNOWN
        )
        df[USER_LOGIN] = df[USER_LOGIN].apply(lambda x: x if x else UNKNOWN)
        df[TAXON_NAME] = df[TAXON_NAME].apply(
            lambda x: self.normalize_text(x) if x else UNKNOWN
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
            logging.debug(f"Transforming the dataset to a DataFrame")
            dataset = [
                self.transform_json_to_dataset(fragment) for fragment in json_dataset
            ]
            df = pd.concat(dataset, ignore_index=True)
            df = df[df[TAXON_RANK] == SPECIES_NAME]
            logging.debug(f"Kept {len(df)} images")

            # One hot encoding for the labels
            unique_values = df[TAXON_NAME].unique()
            logging.debug(f"Found this many labels: {unique_values.shape}")
            encoded_labels = DatasetLoader.encode_labels(unique_values)
            df[ENCODED_LABELS] = df[TAXON_NAME].apply(lambda x: encoded_labels[x])

            logger.info(f"Dataset saved to {dataset_file_name} from JSON")
            df.to_csv(dataset_file_name, index=False)
        except Exception as e:
            logger.error(
                f"Failed to save dataset to {dataset_file_name} from JSON: {e}"
            )
            raise

    def download_dataset(self, dataset_path: str, run_dir: str) -> None:
        """Download the dataset to the input path

        Args:
            dataset_path: Path to save the dataset
        """
        df = self.load_dataset(dataset_path)
        df = df[[TAXON_NAME, PHOTOS]]

        for index, row in tqdm(df.iterrows(), total=df.shape[0]):
            species_name = row[TAXON_NAME]
            photo_urls = eval(row[PHOTOS])  # convert string to list
            species_dir = os.path.join(run_dir, species_name)
            if not BaseIO.path_exists(species_dir):
                BaseIO.create_directory(species_dir)

            for i, url in enumerate(photo_urls):
                try:
                    response = get_request(url, stream=True)
                    if response.status_code == 200:
                        with open(
                            os.path.join(species_dir, f"{index}_{i}.jpg"), "wb"
                        ) as f:
                            for chunk in response.iter_content(1024):
                                f.write(chunk)
                except Exception as e:
                    logger.error(f"Failed to download photo {url}: {e}")
                    continue
