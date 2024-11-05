from typing import Any, BinaryIO, Dict, Iterable, Union

# iNaturalist URLs
BASE_URL = "https://www.inaturalist.org"
API_V1 = f"{BASE_URL}/v1"
EXPORT_URL = f"{BASE_URL}/observations/export"

# projects
PROJECTS_ENDPOINT = "projects/autocomplete"

# rate limiting
CONNECT_TIMEOUT = 5
REQUEST_TIMEOUT = 10
RATE_LIMIT = 60

# iNaturalist Config
USERNAME = "username"
PASSWORD = "password"
APP_ID = "app_id"
APP_SECRET = "app_secret"
PROJECT_NAME = "project_name"
