# !/usr/bin/env python3

# Standard library imports
import logging

# Third-party library imports
import requests

# Local application imports
from grid_model import GridModel
from service_module import CrossmintService


# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class PhaseOne:
    # Constants
    POLYANET = "POLYANET"

    def __init__(self):
        # Initialize API service and models
        self.api_service = CrossmintService(candidate_id="7fadf671-ad83-4988-b9b8-0320b73bf640")
        self.map_data = self.api_service.get_map()
        self.grid_model = GridModel(self.map_data.json()['goal'])

        # Process map items
        self.process_map_items()

    def process_map_items(self):
        for row_index, row in enumerate(self.grid_model.grid):
            for item_index, item in enumerate(row):
                if item == self.POLYANET:
                    self._post_polyanet(row_index, item_index)

    def _post_polyanet(self, row_index, item_index):
        try:
            response = self.api_service.post_polyanets(row=row_index, column=item_index)
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred while posting polyanet at row {row_index}, column {item_index}: {http_err}")
        except Exception as err:
            logger.error(f"An error occurred while posting polyanet at row {row_index}, column {item_index}: {err}")


# Run the process
if __name__ == "__main__":
    phase_one = PhaseOne()