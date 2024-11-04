import os
import shutil
from typing import Any
import logging

logger = logging.getLogger(__name__)


class BaseIO:
    """Custom Base IO class that performs basic file / directory io operations

    * directory_path to use
    """

    @staticmethod
    def create_directory(directory_path: str) -> None:
        """Create the directory if it does not exist

        Args:
            directory_path: Directory Path for usage
        """
        if not os.path.exists(directory_path):
            logger.debug(f"Creating directory: {directory_path}")
            os.makedirs(directory_path)

    @staticmethod
    def clear_directory(directory_path: str) -> None:
        """Iterate over the input directory and delete all the files and directories if any are found

        Args:
            directory_path: Directory Path for usage
        """
        for file_name in os.listdir(directory_path):
            logger.debug(f"Deleting files from directory: {file_name}")
            file_path = os.path.join(directory_path, file_name)

            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

    @staticmethod
    def delete_directory(directory_path: str) -> None:
        """Delete the directory and input files

        Args:
            directory_path: Directory Path for usage
        """
        logger.debug(f"Deleting directory: {directory_path}")
        os.rmdir(directory_path)

    @staticmethod
    def is_path_directory(directory_path: str) -> bool:
        """Check if the input path is a directory

        Args:
            directory_path: Directory Path for usage
        """
        is_dir = os.path.isdir(directory_path)
        logger.debug(f"Path: {directory_path} is a directory: {is_dir}")
        return is_dir

    @staticmethod
    def is_path_file(file_path: str) -> bool:
        """Check if the input path is a file

        Args:
            file_path: File Path for usage
        """
        is_file = os.path.isfile(file_path)
        logger.debug(f"Path: {file_path} is a file: {is_file}")
        return is_file

    @staticmethod
    def is_path_valid(path: str) -> bool:
        """Check if the input path is a valid path

        Args:
            path: Path for usage
        """
        logger.debug(f"Checking if path: {path} is valid: {path}")
        if path is None or not os.path.exists(path):
            logger.debug(f"Path: {path} does not exist: {path}")
            return False
        if not BaseIO.is_path_directory(path) and not BaseIO.is_path_file(path):
            logger.debug(f"Path: {path} is not valid: {path}")
            return False
        logger.debug(f"Path: {path} is valid: {path}")
        return True

    @staticmethod
    def save_file(directory_path: str, file_name: str, contents: Any) -> None:
        """Save the file_name to the directory_path

        Args:
            directory_path: Directory Path for usage
            file_name: file_name to save the contents to
            contents: contents of the fileName
        """
        logger.debug(f"Saving file: {file_name} to directory: {directory_path}")
        full_path = os.path.join(directory_path, file_name)
        with open(full_path, "w") as file:
            file.write(contents)

    @staticmethod
    def read_file(full_path: str) -> Any:
        """Read the contents from the input file

        Args:
            full_path: file_name to read the contents from
        """
        if not BaseIO.is_path_file(full_path):
            return None

        with open(full_path, "r") as file:
            return file.readlines()
