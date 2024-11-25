from typing import Optional
from datetime import datetime, timedelta

import requests

from helpers.decorators import retry
from helpers.exceptions import ApiPermissionError


class FootballDataApiWrapper:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self._base_url = "https://api.football-data.org/v4"

    @retry(max_retries=3, delay=5)
    def fecth_matches(
        self,
        date_from: Optional[datetime] = datetime.today() + timedelta(days=-2),
        date_to: Optional[datetime] = datetime.today(),
    ):
        """Fetches matches from the API within the specified date range"""
        # Some match results and details (e.g., status, scores) may be updated in the API the next day,
        # so we include data from two days ago to ensure we capture any delayed updates.

        response = requests.get(
            f"{self._base_url}/matches",
            headers={"X-Auth-Token": self.api_key},
            params={"dateFrom": date_from.date(), "dateTo": date_to.date()},
        )
        response_data = response.json()

        # For other endpoints, the API responds with an error, but for this one, it returns a response
        # with 'permission' set to None in the 'filters'
        if not response_data["filters"]["permission"]:
            raise ApiPermissionError(
                "Permission information is missing in the API response. This could be due to an invalid API key, "
                "insufficient permissions \n"
                "Please verify the following:\n"
                "1. Ensure the API key is correct\n"
                "2. Check that the API key has the necessary permissions for the requested data\n"
            )

        if not response.ok:
            error_details = response_data.get("message", "No error message provided")
            raise requests.HTTPError(
                f"API returned error: {response.status_code} {response.reason} \n"
                f"Details: {error_details}"
            )
        return response_data

    @retry(max_retries=3, delay=5)
    def fetch_teams(self):
        """Fetches teams from the API"""

        response = requests.get(
            f"{self._base_url}/teams",
            headers={"X-Auth-Token": self.api_key},
        )
        response_data = response.json()
        if not response.ok:
            error_details = response_data.get("message", "No error message provided")
            raise requests.HTTPError(
                f"API returned error: {response.status_code} {response.reason} \n"
                f"Details: {error_details}"
            )

        return response_data

    @retry(max_retries=3, delay=5)
    def fetch_competitions(self):
        """Fetches competitions from the API"""

        response = requests.get(
            f"{self._base_url}/competitions",
            headers={"X-Auth-Token": self.api_key},
        )
        response_data = response.json()

        if not response.ok:
            error_details = response_data.get("message", "No error message provided")
            raise requests.HTTPError(
                f"API returned error: {response.status_code} {response.reason} \n"
                f"Details: {error_details}"
            )

        return response_data
