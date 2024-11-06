#!/usr/bin/env python3

# Standard library imports
from typing import List


class GridModel:
    def __init__(self, grid: List[List[str]]):
        self.grid = grid
        self.num_rows = len(grid)
        self.num_columns = len(grid[0])

    def display_grid(self):
        """Print the grid in a formatted style."""
        for row in self.grid:
            print(" ".join(row))
