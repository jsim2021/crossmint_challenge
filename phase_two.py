#!/usr/bin/env python3

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


class PhaseTwo:
    # Constants
    CANDIDATE_ID = "7fadf671-ad83-4988-b9b8-0320b73bf640"
    EMPTY = "🌌"
    POLYANET_IMG = "🪐"
    SOLOON_IMG = "🌕"
    COMETH_IMG = "☄"
    POLYANET = "POLYANET"
    SOLOON = "SOLOON"
    COMETH = "COMETH"
    SPACE = "SPACE"
    GOAL = "goal"

    def __init__(self):
        """Initialize API service, model, and map."""
        self.api_service = CrossmintService(candidate_id=self.CANDIDATE_ID)
        self.map_data = self.api_service.get_map()
        self.grid_model = GridModel(self.map_data[self.GOAL])

        self.new_map = [
            [self.EMPTY for _ in range(self.grid_model.num_rows)]
            for _ in range(self.grid_model.num_columns)
        ]

        self.process_map_items()
        self._pretty_print(self.new_map)

    def process_map_items(self):
        """Iterate over grid items and process each item."""
        for row_index, row in enumerate(self.grid_model.grid):
            for column_index, item in enumerate(row):
                if item != self.SPACE:
                    self._process_item(row_index, column_index, item)

    def _is_within_bounds(self, row, column):
        """Check if the position is within the bounds of the grid."""
        return 0 <= row < self.grid_model.num_rows and 0 <= column < self.grid_model.num_columns

    def _place_entity(self, image, row, column):
        """Place an entity on the new map if within bounds."""
        if self._is_within_bounds(row, column):
            self.new_map[row][column] = image

    def _is_adjacent_to_polyanet(self, row, column):
        """Check if a cell is adjacent to a Polyanet."""
        neighbors = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        for delta_row, delta_column in neighbors:
            neighbor_row = row + delta_row
            neighbor_col = column + delta_column
            if (self._is_within_bounds(neighbor_row, neighbor_col) and
                    self.grid_model.grid[neighbor_row][neighbor_col] == self.POLYANET):
                return True
        return False

    def _process_item(self, row_index, column_index, item):
        """Process individual grid items based on their type."""
        if item == self.POLYANET:
            self._place_entity(self.POLYANET_IMG, row_index, column_index)

            try:
                response = self.api_service.post_polyanets(row=row_index, column=column_index)
            except requests.exceptions.HTTPError as http_err:
                logger.error(
                    f"HTTP error occurred while posting polyanet at row {row_index}, column {column_index}: {http_err}")
            except Exception as err:
                logger.error(f"An error occurred while posting polyanet at row {row_index}, column {column_index}: {err}")
        elif self.SOLOON in item:
            if self._is_adjacent_to_polyanet(row_index, column_index):
                self._place_entity(self.SOLOON_IMG, row_index, column_index)
                color, _ = item.split("_")
                try:
                    response = self.api_service.post_soloons(row_index, column_index, color.lower())
                except requests.exceptions.HTTPError as http_err:
                    logger.error(
                        f"HTTP error occurred while posting soloons at row {row_index}, column {column_index}: {http_err}")
                except Exception as err:
                    logger.error(
                        f"An error occurred while posting soloons at row {row_index}, column {column_index}: {err}")
        elif self.COMETH in item:
            self._place_entity(self.COMETH_IMG, row_index, column_index)
            direction, _ = item.split("_")
            try:
                response = self.api_service.post_comeths(row_index, column_index, direction.lower())
            except requests.exceptions.HTTPError as http_err:
                logger.error(
                    f"HTTP error occurred while posting comeths at row {row_index}, column {column_index}: {http_err}")
            except Exception as err:
                logger.error(f"An error occurred while posting comeths at row {row_index}, column {column_index}: {err}")

    def _pretty_print(self, arr):
        """Print the grid in a formatted style."""
        for row in arr:
            print("".join(map(str, row)))


# Run the process
if __name__ == "__main__":
    phase_two = PhaseTwo()