from library.request_helper import get_local_session
from library.dataset_Loader import DatasetLoader
from common.constants import (
    API_V1,
    ResponseResult,
    ASCENDING_ORDER,
    DESCENDING_ORDER,
    ID_ORDER,
    CREATION_ORDER,
    OBSERVATIONS_ENDPOINT,
    DATASET_NAME,
)
from datetime import datetime

import os
import logging
import time

logger = logging.getLogger(__name__)


class ObservationController:
    def __init__(self):
        self.session = get_local_session()
        self.endpoint = f"{API_V1}/{OBSERVATIONS_ENDPOINT}"
        self.dataset_loader = DatasetLoader()
        self.rate_limit_per_minute = 60  # 60 requests per minute
        self.delay_between_requests = 60 / self.rate_limit_per_minute

    def get_project_observations(
        self,
        project_id: str,
        per_page: int = 200,
        order: str = DESCENDING_ORDER,
        order_by: str = CREATION_ORDER,
        page: int = None,
        id_above: int = None,
    ) -> ResponseResult:
        """Gets the observations for the input taxon

        * project_id: Get all the observations for the input project_id
        * per_page: Number of observations to return per page
        * order: Order of the observations (asc or desc)
        * order_by: Order by id or species, created_at, etc
        * page: Page number to get the observations for
        * id_above: Get observations with IDs above the input id

        Examples:

            With direct keyword arguments:

            >>>  observations = get_observations(
            >>>     project_id="1111",
            >>> )

        Args:
            project_id: string taxon to get observations for
            per_page: number of observations to return per page
            order: order of the observations (asc or desc)
            order_by: order by id or species, created_at, etc
            page: page number to get the observations for
            id_above: get observations with IDs above the input id

        Returns:
            list of observation responses as json or text
        """
        params = {
            "project_id": project_id,
            "per_page": per_page,
            "order": order,
            "order_by": order_by,
        }
        if page:
            params["page"] = page
        if id_above:
            params["id_above"] = id_above
        logging.debug(f"creating pararms {params}")

        observations = self.session.send_request(
            method="GET", url=self.endpoint, return_type="json", params=params
        )

        return observations

    def save_observations_as_dataset(
        self, project_id: str, dataset_path: str, run_id: str = None
    ) -> None:
        """Save the observations as a dataset to the input path

        Args:
            project_id: Project ID to get the observations for
            dataset_path: Path to save the dataset
            run_id: Unique ID for the run
        """
        total_images = 0
        all_observations = []
        per_page = 200  # INaturalist API returns max of 200 results per call
        id_above = None
        page = 1

        while True:
            results = self.get_project_observations(
                project_id,
                id_above=id_above,
                per_page=per_page,
                order=ASCENDING_ORDER,
                order_by=ID_ORDER,
            )
            observations = results["results"]
            if not observations:
                break
            total_images += len(observations)
            all_observations.extend(observations)
            page += 1
            logger.debug(f"Foun {len(observations)} observations on page {page-1}")

            # Get the highest ID from the current batch to use as id_above for the next batch
            id_above = observations[-1]["id"]

            time.sleep(self.delay_between_requests)

        logging.info(
            f"finished getting all the observations after {page-1} pages.\n Total images found: {total_images}"
        )

        # Generate a unique file name with run ID or timestamp
        if run_id is None:
            run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"{DATASET_NAME}_{run_id}.csv"

        self.dataset_loader.save_json_dataset(
            os.path.join(dataset_path, file_name), {"dataset": all_observations}
        )
