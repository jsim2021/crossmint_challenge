# !/usr/bin/env python3

# Standard library imports
import logging

# Third-party library imports
import requests

# Local application imports
from grid_model import GridModel
from service_module import CrossmintService


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class PhaseOne:
    # Constants
    POLYANET = "POLYANET"
    GOAL = "goal"
    CANDIDATE_ID = "7fadf671-ad83-4988-b9b8-0320b73bf640"

    def __init__(self):
        # Initialize API service and models
        self.api_service = CrossmintService(candidate_id=self.CANDIDATE_ID)
        logger.info("Retrieving map data.")
        self.map_data = self._get_map()
        self.grid_model = GridModel(self.map_data[self.GOAL])

        # Process map items
        logger.info("Processing map items")
        self.process_map_items()

    def process_map_items(self):
        for row_index, row in enumerate(self.grid_model.grid):
            for column_index, item in enumerate(row):
                if item == self.POLYANET:
                    logger.info("Sending POST request to the /polyanet endpoint")
                    self._post_polyanet(row_index, column_index)
        logger.info("Successfully processed all map items!")

    def _get_map(self) -> dict:
        try:
            return self.api_service.get_map()
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred while retrieving map: {http_err}")
        except Exception as err:
            logger.error(f"An error occurred while retrieving map: {err}")

    def _post_polyanet(self, row_index, column_index):
        try:
            _ = self.api_service.post_polyanets(row=row_index, column=column_index)
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred while posting polyanet at row {row_index}, column {column_index}: {http_err}")
        except Exception as err:
            logger.error(f"An error occurred while posting polyanet at row {row_index}, column {column_index}: {err}")


# Run the process
if __name__ == "__main__":
    phase_one = PhaseOne()