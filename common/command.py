from enum import Enum


class Command(Enum):
    """
    Enum for the commands that can be run
    """

    DOWNLOAD = "download"
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
