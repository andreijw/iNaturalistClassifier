from library.request_helper import get_local_session
from library.dataset_Loader import DatasetLoader
from common.constants import (
    API_V1,
    ResponseResult,
    DESCENDING_ORDER,
    ORDER_BY,
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
        order_by: str = ORDER_BY,
        page: int = 0,
    ) -> ResponseResult:
        """Gets the observations for the input taxon

        * taxon_id: Get all the observations for the input taxon

        Examples:

            With direct keyword arguments:

            >>>  observations = get_observations(
            >>>     taxon_id="tigers",
            >>> )

        Args:
            taxon_id: string taxon to get observations for

        Returns:
            list of observation responses as json or text
        """
        params = {
            "project_id": project_id,
            "per_page": per_page,
            "order": order,
            "order_by": order_by,
            "page": page,
        }
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
        """
        page = 1
        total_images = 0
        all_observations = []
        per_page = 200  # INaturalist API returns max of 200 results per call
        total_images = 0

        while True:
            results = self.get_project_observations(
                project_id, page=page, per_page=per_page
            )
            observations = results["results"]
            if not observations:
                break
            total_images += len(observations)
            page += 1
            all_observations.extend(observations)
            logger.debug(f"Foun {len(observations)} observations on page {page-1}")

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
