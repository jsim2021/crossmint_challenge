# !/usr/bin/env python3

# Standard library imports
import random
import time
from typing import List

# Third-party library imports
import requests

class CrossmintService:
    # Constants
    POLYANETS = "polyanets"
    SOLOONS = "soloons"
    COMETHS = "comeths"
    ROW = "row"
    COLUMN = "column"
    COLOR = "color"
    DIRECTION = "direction"
    BASE_URL = "https://challenge.crossmint.io/api"

    def __init__(self, candidate_id: str):
        self.candidate_id = candidate_id

    def _make_request(
            self,
            endpoint: str,
            method: str = "GET",
            data: dict = None,
            params: dict = None,
            max_retries: int = 10,
            base_delay: int = 1,
            max_delay: int = 60
    ):
        """
        Makes an HTTP request to the specified endpoint with retry logic, exponential backoff, and jitter.

        Args:
            endpoint (str): The API endpoint to which the request will be made.
            method (str): The HTTP method to use for the request (e.g., "GET", "POST"). Defaults to "GET".
            data (dict, optional): The payload for POST and PUT requests. Defaults to None.
            params (dict, optional): The query parameters for the request URL. Defaults to None.
            max_retries (int): Max retry attempts if a 429 status code is received. Defaults to 10.
            base_delay (int): Initial delay time in seconds for exponential backoff. Defaults to 1.
            max_delay (int): Max allowable delay between retries in seconds. Defaults to 60.

        Returns:
            dict: JSON response from the server if successful.

        Raises:
            requests.exceptions.HTTPError: If a 4xx or 5xx error occurs (other than 429).
            Exception: If max retries are reached without success.
        """
        retries = 0
        url = f"{self.BASE_URL}/{endpoint}"
        headers = {"Content-Type": "application/json"}

        if data is None:
            data = {} if "goal" not in endpoint else {}
        data['candidateId'] = self.candidate_id

        while retries < max_retries:
            try:
                response = requests.request(method, url, headers=headers, json=data, params=params)
                response.raise_for_status()
                if response.status_code == 200:
                    return response.json()
            except requests.exceptions.HTTPError as http_err:
                if response.status_code == 429:
                    backoff_time = min(base_delay * (2 ** retries), max_delay)
                    jitter = random.uniform(0, backoff_time)
                    time.sleep(jitter)
                    retries += 1
                else:
                    raise http_err
        raise Exception("Max retries reached. Failed to complete the request.")

    def post_polyanets(self, row: int, column: int):
        """Adds a polyanet at a specific location."""
        data = {self.ROW: row, self.COLUMN: column}
        return self._make_request(self.POLYANETS, method="POST", data=data)

    def delete_polyanets(self, row: int, column: int):
        """Deletes a polyanet at a specific location."""
        data = {self.ROW: row, self.COLUMN: column}
        return self._make_request(self.POLYANETS, method="DELETE", data=data)

    def post_soloons(self, row: int, column: int, color: str = None):
        """Adds a soloon at a specific location with an optional color."""
        data = {self.ROW: row, self.COLUMN: column, self.COLOR: color}
        return self._make_request(self.SOLOONS, method="POST", data=data)

    def delete_soloons(self, row: int, column: int):
        """Deletes a soloon at a specific location."""
        data = {self.ROW: row, self.COLUMN: column}
        return self._make_request(self.SOLOONS, method="DELETE", data=data)

    def post_comeths(self, row: int, column: int, direction: str = None):
        """Adds a cometh at a specific location with an optional direction."""
        data = {self.ROW: row, self.COLUMN: column, self.DIRECTION: direction}
        return self._make_request(self.COMETHS, method="POST", data=data)

    def delete_comeths(self, row: int, column: int):
        """Deletes a cometh at a specific location."""
        data = {self.ROW: row, self.COLUMN: column}
        return self._make_request(self.COMETHS, method="DELETE", data=data)

    def get_map(self):
        """Returns the goal map for the current challenge phase."""
        return self._make_request(f"map/{self.candidate_id}/goal")