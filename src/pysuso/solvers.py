from collections import deque
from typing import Deque

from pysuso.boards import Board, Coordinate
from pysuso.exceptions import BoardNotSolvableException, InvalidCellValueException


class BasicSolver:

    SQUARE_SIZE = 3
    BOARD_SIZE = 9

    def __init__(self, board: Board) -> None:
        self.unsolved_board = board

    def solve(self) -> Board:
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
