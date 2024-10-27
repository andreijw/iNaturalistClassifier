import os
import json

from common.constants import USERNAME, PASSWORD, APP_ID, APP_SECRET


class ConfigHelper:
    def __init__(self, config_path):
        if (
            not config_path
            or not os.path.exists(config_path)
            or not os.path.isfile(config_path)
        ):
            raise ValueError("Config path is not valid")
        self.config_path = config_path
        self.username, self.password, self.app_id, self.app_secret = self.get_config()

    def get_config(self) -> tuple[str, str, str]:
        """Get the configuration from the config file"""
        config_contents = {}
        with open(self.config_path, "r") as file:
            config_contents = json.load(file)

        if (
            USERNAME not in config_contents
            or PASSWORD not in config_contents
            or APP_ID not in config_contents
            or APP_SECRET not in config_contents
        ):
            raise ValueError("Config file is not valid")
        return (
            config_contents[USERNAME],
            config_contents[PASSWORD],
            config_contents[APP_ID],
            config_contents[APP_SECRET],
        )