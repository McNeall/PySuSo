"""This module contains a collection of Sudoku solvers"""

from collections import deque
from typing import Deque

from pysuso.boards import Board, Coordinate
from pysuso.exceptions import BoardNotSolvableException, InvalidCellValueException


class BasicSolver:
    """A basic Soduko solver using a brute force back tracking algorithm

    This solver uses back tracking for the empty cells. Cells are processed left to right, top to
    bottom. It always picks the next higher value valid value. The algorithm stops in case one valid
    solution is found. There is no check if there is another valid solution.
    """

    SQUARE_SIZE = 3
    BOARD_SIZE = 9

    def __init__(self, board: Board) -> None:
        """Setup the solver

        Args:
            board: Board that should be solved
        """
        self.unsolved_board = board

    def solve(self) -> Board:
        """Searches for a valid solution of the board and returns the filled board.

        Raises:
            BoardNotSolvableException: If no valid solution for the board is found.

        Returns:
            A board filled with a valid solution.
        """
        remaining_cells = deque([coordinate for coordinate, value in self.unsolved_board if value == 0])
        history: Deque[Coordinate] = deque()
        while remaining_cells:
            current_coordinate = remaining_cells.pop()
            current_value = self.unsolved_board[current_coordinate]
            for i in range(current_value + 1, self.BOARD_SIZE + 1):
                try:
                    self.unsolved_board[current_coordinate] = i
                    history.append(current_coordinate)
                    break
                except InvalidCellValueException:
                    continue
            else:
                self.unsolved_board[current_coordinate] = 0
                remaining_cells.append(current_coordinate)
                if history:
                    lastest_history_item = history.pop()
                    remaining_cells.append(lastest_history_item)
                else:
                    raise BoardNotSolvableException("No valid solution found.")
        return self.unsolved_board
