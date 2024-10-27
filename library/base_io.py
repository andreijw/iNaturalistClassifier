import os
import shutil
from typing import Any


class BaseIO:
    """Custom Base IO class that performs basic file / directory io operations

    * directory_path to use
    """

    def __init__(self):
        pass

    def create_directory(self, directory_path: str) -> None:
        """Create the directory if it does not exist

        Args:
            directory_path: Directory Path for usage
        """
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

    def clear_directory(self, directory_path: str) -> None:
        """Iterate over the input directory and delete all the files and directories if any are found

        Args:
            directory_path: Directory Path for usage
        """
        for file_name in os.listdir(directory_path):
            file_path = os.path.join(directory_path, file_name)

            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

    def delete_directory(self, directory_path: str) -> None:
        """Delete the directory and input files

        Args:
            directory_path: Directory Path for usage
        """
        os.rmdir(directory_path)

    def is_path_directory(self, directory_path: str) -> bool:
        """Check if the input path is a directory

        Args:
            directory_path: Directory Path for usage
        """
        return os.path.isdir(directory_path)

    def is_path_file(self, file_path: str) -> bool:
        """Check if the input path is a file

        Args:
            file_path: File Path for usage
        """
        return os.path.isfile(file_path)

    def is_path_valid(self, path: str) -> bool:
        """Check if the input path is a valid path

        Args:
            path: Path for usage
        """
        return path is None and os.path.exists(path)

    def save_file(self, directory_path: str, file_name: str, contents: Any) -> None:
        """Save the file_name to the directory_path

        Args:
            directory_path: Directory Path for usage
            file_name: file_name to save the contents to
            contents: contents of the fileName
        """

        full_path = os.path.join(directory_path, file_name)
        with open(full_path, "w") as file:
            file.write(contents)

    def read_file(self, full_path: str) -> Any:
        """Read the contents from the input file

        Args:
            full_path: file_name to read the contents from
        """
        if not self.is_path_file(full_path):
            return None

        with open(full_path, "r") as file:
            return file.readlines()
