from library.request_helper import get_local_session
from common.constants import (
    API_V1,
    ResponseResult,
    DESCENDING_ORDER,
    ORDER_BY,
    OBSERVATIONS_ENDPOINT,
)

import logging

logger = logging.getLogger(__name__)


class ObservationController:
    def __init__(self):
        self.session = get_local_session()
        self.endpoint = f"{API_V1}/{OBSERVATIONS_ENDPOINT}"

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
