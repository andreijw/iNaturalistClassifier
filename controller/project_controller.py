from common.constants import API_V1, PROJECTS_ENDPOINT
from urllib.parse import quote
from library.request_helper import get_local_session

import logging

logger = logging.getLogger(__name__)


class ProjectController:
    """Custom ProjectController to use to get, create and update information about projects"""

    def __init__(self):
        self.endpoint = f"{API_V1}/{PROJECTS_ENDPOINT}"
        self.session = get_local_session()

    def get_project_id_by_name(self, project_name: str) -> str:
        """Gets the id for the associated project by name

            * project_name: project name for which to get the id

        Examples:

            With direct keyword arguments:

            >>>  project_id = get_project_id_by_name(
            >>>     project_name='testName',
            >>> )

        Args:
            project_name: project name for which to get the id

        Returns:
            string project_id
        """
        project_info = self.get_project_info_by_name(project_name)
        if (
            project_info
            and "results" in project_info
            and len(project_info["results"]) > 0
        ):
            return project_info["results"][0]["id"]
        else:
            logger.error(f"No project found with name: {project_name}")
            return None

    def get_project_info_by_name(self, project_name: str) -> str:
        """Gets the information for the associated project by name

            * project_name: project name for which to get the information

        Examples:

            With direct keyword arguments:

            >>>  project_info = get_project_info_by_name(
            >>>     project_name='testName',
            >>> )

        Args:
            project_name: project name for which to get the information

        Returns:
            string project-info
        """
        params = {"q": project_name}
        logging.debug(f"creating pararms {params}")

        project_info = self.session.send_request(
            method="GET", url=self.endpoint, return_type="json", params=params
        )
        return project_info
