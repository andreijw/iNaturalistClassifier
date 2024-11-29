from library.species_dataset import SpeciesDataset
from model.cnn import CNN

import logging
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, random_split
from torchvision import transforms
from tqdm import tqdm

logger = logging.getLogger(__name__)


class ModelTrainer:
    def __init__(
        self,
        model_path: str,
        dataset_dir: str,
        output_path: str,
        num_epochs: int = 1,
    ) -> None:
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model_path = model_path
        self.dataset_dir = dataset_dir
        self.output_path = output_path

        # Transforms for the images
        self.transform = transforms.Compose(
            [
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
            ]
        )

        # Load the dataset
        logger.info(f"Loading the dataset: {dataset_dir}")
        dataset = SpeciesDataset(self.dataset_dir, transform=self.transform)

        # Define the split sizes
        train_size = int(0.75 * len(dataset))
        val_size = len(dataset) - train_size
        batch_size = 256
        train_dataset, val_dataset = random_split(dataset, [train_size, val_size])

        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
        logger.info(
            f"Loaded the dataset: {dataset_dir} | Train size: {train_size} | Val size: {val_size}"
        )

        num_clases = len(dataset.lables_to_index)
        self.model = CNN(num_classes=num_clases).to(self.device)
        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.001)
        self.num_epochs = num_epochs

        self.train_model(
            self.model,
            train_loader,
            self.criterion,
            self.optimizer,
            self.model_path,
            self.num_epochs,
        )

        avg_loss, accuracy = self.evaluate_model(
            self.model, val_loader, self.criterion, self.output_path
        )

    def train_model(
        self,
        model: CNN,
        dataloader: DataLoader,
        criterion: nn.Module,
        optimizer: optim.Optimizer,
        model_path: str,
        num_epochs: int,
    ):
        model.train()
        logger.info(
            f"Training the model for {num_epochs} epochs | device: {self.device}"
        )
        for epoch in range(num_epochs):
            running_loss = 0.0
            for inputs, labels in tqdm(dataloader):
                inputs, labels = inputs.to(self.device), labels.to(self.device)

                optimizer.zero_grad()

                outputs = model(inputs)
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()

                running_loss += loss.item() * inputs.size(0)

            epoch_loss = running_loss / len(dataloader.dataset)
            logger.debug(f"Epoch {epoch+1}/{num_epochs}, Loss: {epoch_loss:.4f}")

        torch.save(model.state_dict(), model_path)
        logger.info(f"Model saved to: {model_path}")

    def evaluate_model(
        self, model, dataloader: DataLoader, criterion: nn.Module, output_path: str
    ):
        """Evaluate the input model with the input data"""
        model.eval()
        running_loss = 0.0
        correct_predictions = 0
        total_predictions = 0

        with torch.no_grad():
            for inputs, labels in tqdm(dataloader):
                inputs, labels = inputs.to(self.device), labels.to(self.device)

                outputs = model(inputs)
                loss = criterion(outputs, labels)
                running_loss += loss.item() * inputs.size(0)

                _, predicted = torch.max(outputs, 1)
                _, labels_max = torch.max(labels, 1)
                correct_predictions += (predicted == labels_max).sum().item()
                total_predictions += labels.size(0)

        avg_loss = running_loss / len(dataloader.dataset)
        accuracy = correct_predictions / total_predictions

        logger.info(f"Evaluation Loss: {avg_loss:.4f}, Accuracy: {accuracy:.4f}")

        with open(output_path, "w") as f:
            f.write(f"Evaluation Loss: {avg_loss:.4f}, Accuracy: {accuracy:.4f}")

        logger.debug(f"Output saved to: {output_path}")

        return avg_loss, accuracy
