"""
Entry point to the Flies and AI application
This is the main runner with argument options. It will allow us to run the different comamnds
"""

import os
import logging
import argparse


def run_application(args: str) -> None:
    """
    Runs the entire application based on the input arguments

    """
    if args.verbose:
        logging.basicConfig(encoding="utf-8", level=logging.DEBUG)
    else:
        logging.basicConfig(encoding="utf-8", level=logging.ERROR)


def validate_args(args: str) -> bool:
    """
    Validate that the required arguemnts are passed in"""

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

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subparser for the download command
    download_parser = subparsers.add_parser(
        "download", help="Download and create a dataset"
    )
    download_parser.add_argument(
        "-d",
        "--dataset_path",
        help="Path to save the downloaded dataset",
        required=True,
    )

    # Subparser for the classify command
    classify_parser = subparsers.add_parser("classify", help="Classify a dataset")
    classify_parser.add_argument(
        "-p", "--classify_path", help="Path to the dataset to classify", required=True
    )

    args = parser.parse_args()

    if validate_args(args):
        run_application(args)
