from typing import Any, BinaryIO, Dict, Iterable, Union

# iNaturalist URLs
BASE_URL = "https://www.inaturalist.org"
BASE_API_URL = "https://api.inaturalist.org"
API_V1 = f"{BASE_API_URL}/v1"
UNKNOWN = "unknown"

# projects
PROJECTS_ENDPOINT = "projects/autocomplete"
OBSERVATIONS_ENDPOINT = "observations"

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

# Request Arguments
DESCENDING_ORDER = "desc"
ASCENDING_ORDER = "asc"
SPECIES_RANK = "species"
ID_ORDER = "id"
CREATION_ORDER = "created_at"

# Typing
ResponseResult = Dict[str, Any]

# Dataset Loader
SQUARE_SUFIX = "square"
MEDIUM_SUFIX = "medium"
LARGE_SUFIX = "large"
SMALL_SUFIX = "small"

TAXON_NAME = "taxon.name"
TAXON_RANK = "taxon.rank"
SPECIES_GUESSES = "species_guess"
USER_LOGIN = "user.login"
PHOTOS = "photos"
ENCODED_LABELS = "encoded_labels"

DATASET_COLUMNS = [
    "id",
    "species_guess",
    "time_observed_at",
    "identifications_most_agree",
    "user.login",
    "uri",
    "photos",
    "taxon.id",
    "taxon.rank",
    "taxon.rank_level",
    TAXON_NAME,
]

DATASET_NAME = "dataset"
OUTPUT_NAME = "prediction"
MODEL_NAME = "model"
SPECIES_NAME = "species"
