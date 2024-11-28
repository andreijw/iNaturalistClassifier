import json
from library.base_io import BaseIO

from common.constants import USERNAME, PASSWORD, APP_ID, APP_SECRET, PROJECT_NAME


class ConfigHelper:
    def __init__(self, config_path):
        if not config_path or not BaseIO.path_exists(config_path):
            raise ValueError("Config path is not valid")
        self.config_path = config_path
        (
            self._username,
            self._password,
            self._app_id,
            self._app_secret,
            self._project_name,
        ) = self.get_config()

    def get_config(self) -> tuple[str, str, str, str, str]:
        """Get the configuration from the config file"""
        config_contents = {}
        try:
            with open(self.config_path, "r") as file:
                config_contents = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise ValueError(f"Error reading config file: {e}")

        required_keys = [USERNAME, PASSWORD, APP_ID, APP_SECRET, PROJECT_NAME]
        for key in required_keys:
            if key not in config_contents:
                raise ValueError(f"Config file is missing required key: {key}")
        return (
            config_contents[USERNAME],
            config_contents[PASSWORD],
            config_contents[APP_ID],
            config_contents[APP_SECRET],
            config_contents[PROJECT_NAME],
        )

    def __str__(self) -> str:
        config_str = f"ConfigHelper Config: |"
        for key, value in self.__dict__.items():
            config_str += f" {key}: {value} |"

        return config_str

    @property
    def username(self) -> str:
        return self._username

    @property
    def password(self) -> str:
        return self._password

    @property
    def app_id(self) -> str:
        return self._app_id

    @property
    def app_secret(self) -> str:
        return self._app_secret

    @property
    def project_name(self) -> str:
        return self._project_name
