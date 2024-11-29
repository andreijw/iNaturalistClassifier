from enum import Enum


class Command(Enum):
    """
    Enum for the commands that can be run
    """

    DOWNLOAD = "download"
    TRAIN = "train"
    PREDICT = "predict"


def validate_command(command: str) -> bool:
    """
    Validate that the command string is a valid command
    """
    try:
        Command(command)
        return True
    except ValueError:
        return False


def string_to_command(command: str) -> Command:
    """
    Convert a string to a Command enum
    """
    return Command(command)
