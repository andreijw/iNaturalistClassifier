"""
Entry point to the Flies and AI application
This is the main runner with argument options. It will allow us to run the different comamnds
"""

import logging
import argparse

from common.command import Command, validate_command, string_to_command
from common.config import ConfigHelper
from library.base_io import BaseIO
from controller.project_controller import ProjectController


def run_application(args: str) -> None:
    """
    Runs the entire application based on the input arguments

    """
    command = Command(args.command)
    config = ConfigHelper(args.config_path)
    logging.debug(f"Config: {config}")

    match (command):
        case Command.DOWNLOAD:
            logging.info(f"Clearing dataset directory: {args.dataset_path}")
            BaseIO.clear_directory(args.dataset_path)

            # Get the project ID from the config name
            projectController = ProjectController()
            project_id = projectController.get_project_id_by_name(config.project_name)

            logging.debug(f"Found the following project id {project_id}")
        case Command.PREDICT:
            logging.info(f"Predicting dataset: {args.predict_path}")
            # Predict the dataset
        case _:
            logging.error(f"Command not found: {args.command}")


def validate_args(args: argparse.Namespace) -> bool:
    """
    Validate that the required arguemnts are passed in"""
    if not args.command or not validate_command(args.command):
        logging.error("Please provide a valid command")
        return False

    if not BaseIO.is_path_valid(args.config_path):
        logging.error(f"Config path {args.config_path} is not valid")
        return False

    command = string_to_command(args.command)
    if command is None:
        logging.error(f"Command: {args.command} is not valid")
        return False

    operating_path = (
        args.dataset_path if command == Command.DOWNLOAD else args.predict_path
    )

    if not BaseIO.is_path_directory(operating_path):
        logging.debug(f"Input path {operating_path} is not valid. Creating it...")
        BaseIO.create_directory(operating_path)

    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "Collects obersvations and images to classify as being male/female and if they have a prey or not"
    )
    parser.add_argument(
        "-v",
        "--verbose",
        default=False,
        help="Extra log verbosity",
        action=argparse.BooleanOptionalAction,
    )
    parser.add_argument(
        "-c", "--config_path", help="Path to the config.json file", required=True
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
        help="Command to run. Options are: download, predict",
    )

    # Subparser for the download command
    download_parser = subparsers.add_parser(
        str(Command.DOWNLOAD.value).lower(), help="Download and create a dataset"
    )
    download_parser.add_argument(
        "-d",
        "--dataset_path",
        help="Path to save the downloaded dataset",
        required=True,
    )

    # Subparser for the classify command
    classify_parser = subparsers.add_parser(
        str(Command.PREDICT.value).lower(), help="Predict a dataset"
    )
    classify_parser.add_argument(
        "-p", "--predict_path", help="Path to the dataset to predict", required=True
    )

    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(encoding="utf-8", level=logging.DEBUG)
    else:
        logging.basicConfig(encoding="utf-8", level=logging.ERROR)
    logging.debug(f"Arguments: {args}")

    if validate_args(args):
        run_application(args)
