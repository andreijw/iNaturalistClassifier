import os
import glob
import pandas as pd
from torch.utils import Dataset
from torchvision import transforms
from PIL import Image
from common.constants import TAXON_NAME
from library.dataset_Loader import DatasetLoader

from library.base_io import BaseIO


class SpeciesDataset(Dataset):
    def __init__(self, dataset_dir: str, transform=transforms.Compose = None):
        self.dataset_dir = dataset_dir
        self.transform = transform
        self.image_paths = []
        self.label_names = []

        # Dynamically create the labels from the dataset
        self.lables_to_index = self.generate_labels(dataset_dir, ".csv")

        for label in os.listdir(dataset_dir):
            label_dir = os.path.join(dataset_dir, label)
            if BaseIO.is_path_directory(label_dir):

                for image_name in os.listdir(label_dir):
                    image_path = os.path.join(label_dir, image_name)
                    self.image_paths.append(image_path)
                    self.label_names.append(label)
                    

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        image_path = self.image_paths[idx]
        label = self.label_names[idx]
        encoded_label = self.lables_to_index[label]
        image = Image.open(image_path)

        if self.transform:
            image = self.transform(image)
        return image, encoded_label
    
    def generate_labels(self, dataset_dir:str, extension: str) -> dict:
        """ Generate the labels from the dataset directory """
        dataset_file = glob.glob(f"{dataset_dir}/*{extension}")
        if not dataset_file:
            raise FileNotFoundError(f"No dataset file found in {dataset_dir}")
        
        dataset_file = dataset_file[0]
        df = pd.read_csv(dataset_file)
        df = df[TAXON_NAME]

        label_values = df[TAXON_NAME].unique()
        return DatasetLoader.encode_labels(label_values)
