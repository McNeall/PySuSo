from __future__ import annotations

import os
from collections.abc import Iterator
from dataclasses import dataclass
from typing import List, Set, Tuple

from pysuso.exceptions import (
    InvalidBoardException,
    InvalidCellValueException,
    InvalidIndexException,
)


@dataclass(frozen=True)
class Coordinate:
    row: int
    col: int

    def __post_init__(self) -> None:
        if self.row < 0 or self.row >= 9:
            raise ValueError(f"Row index needs to be between zero and eight. Given {self.row}")
        if self.col < 0 or self.col >= 9:
            raise ValueError(f"Column index needs to be between zero and eight. Given {self.col}")


class Board:
    _BOARD_DIM = 9
    _SQUARE_SIZE = 3
    _VALID_VALUES = set(range(1, _BOARD_DIM + 1))

    def __init__(self, values: List[int], _is_direct: bool = True) -> Board:
        if _is_direct:
            raise RuntimeError(
                "Calling the Board constructure is not supported. Use one of the factory methods to create a board."
            )
        self._values: List[int] = values
        self._initial_empty_cells: Set[Coordinate] = {
            Coordinate(i // self._BOARD_DIM, i % self._BOARD_DIM) for i, value in enumerate(values) if value == 0
        }

    @classmethod
    def from_nested_lists(cls, values: List[List[int]]) -> Board:
        if len(values) != cls._BOARD_DIM:
            raise InvalidBoardException(
                f"Cannot create board. Expected {cls._BOARD_DIM} rows but received {len(values)}."
            )

        invalid_row_length = {i: len(row) for i, row in enumerate(values) if len(row) != cls._BOARD_DIM}
        if invalid_row_length:
            message = ["Cannot create board. Rows found with invalid length"]
            message.extend(
                (
                    f"{row_index}: Expectec length {cls._BOARD_DIM}, actual length {row_length}"
                    for row_index, row_length in invalid_row_length.items()
                )
            )
            raise InvalidBoardException(f"{os.linesep}".join(message))
        valid_values_with_placeholder = cls._VALID_VALUES.union([0])
        invalid_values = {
            (i, j): value
            for i, row in enumerate(values)
            for j, value in enumerate(row)
            if value not in valid_values_with_placeholder
        }
        if invalid_values:
            message = ["Expect values between 0 and 9. Found invalid values:"]
            message.extend((f"{position}: {value}" for position, value in invalid_values.items()))
            raise InvalidBoardException(f"{os.linesep}".join(message))
        return cls([value for row in values for value in row], _is_direct=False)

    @classmethod
    def from_list(cls, values: List[int]) -> Board:
        if len(values) != cls._BOARD_DIM**2:
            raise InvalidBoardException(
                f"Cannot create board. Expected {cls._BOARD_DIM ** 2} rows but received {len(values)}."
            )
        valid_values_with_placeholder = cls._VALID_VALUES.union([0])
        invalid_values = {i: value for i, value in enumerate(values) if value not in valid_values_with_placeholder}
        if invalid_values:
            message = ["Expect values between 0 and 9. Found invalid values:"]
            message.extend((f"{index}: {value}" for index, value in invalid_values.items()))
            raise InvalidBoardException(f"{os.linesep}".join(message))
        return cls(values, _is_direct=False)

    @classmethod
    def from_string(cls, values: str) -> Board:
        if len(values) != cls._BOARD_DIM**2:
            raise InvalidBoardException(
                f"Cannot create board. Expected {cls._BOARD_DIM ** 2} values but received {len(values)}."
            )
        invalid_positions = {}
        valid_values = []
        for i, value in enumerate(values):
            try:
                converted_value = int(value)
                valid_values.append(converted_value)
            except ValueError:
                invalid_positions[i] = f'Value "{value}" is not an integer'

        if invalid_positions:
            message = ["Error creating board. Found invalid values:"]
            message.extend((f"{index}: {message}" for index, message in invalid_positions.items()))
            raise InvalidBoardException(f"{os.linesep}".join(message))
        else:
            return cls(valid_values, _is_direct=False)

    def available_col_values(self, column_index: int) -> Set[int]:
        if column_index < 0 or column_index >= self._BOARD_DIM:
            raise InvalidIndexException(f"Expecting a column index betwenn 0 and 8, but {column_index} was given")
        values_in_column = set(self._values[column_index : self._BOARD_DIM**2 : self._BOARD_DIM])
        return Board._VALID_VALUES.difference(values_in_column)

    def available_row_values(self, row_index: int) -> Set[int]:
        if row_index < 0 or row_index >= self._BOARD_DIM:
            raise InvalidIndexException(f"Expecting a row index betwenn 0 and 8, but {row_index} was given")
        values_in_row = set(self._values[self._BOARD_DIM * row_index : self._BOARD_DIM * (row_index + 1)])
        return Board._VALID_VALUES.difference(values_in_row)

    def available_square_values(self, coordinate: Coordinate) -> Set[int]:
        top_left = Coordinate(
            coordinate.row - coordinate.row % self._SQUARE_SIZE,
            coordinate.col - coordinate.col % self._SQUARE_SIZE,
        )
        values_in_square = set()
        for i in range(0, Board._SQUARE_SIZE):
            start_index = (top_left.row + i) * self._BOARD_DIM + top_left.col
            values_in_square.update(self._values[start_index : start_index + 3])
        return Board._VALID_VALUES.difference(values_in_square)

    def is_valid(self, coordinate: Coordinate, value: int) -> bool:
        if value <= 0 or value > 9:
            return False
        if (
            value in self.available_row_values(coordinate.row)
            and value in self.available_col_values(coordinate.col)
            and value in self.available_square_values(coordinate)
        ):
            return True
        return False

    def __iter__(self) -> Iterator[Tuple[Coordinate, int]]:
        for i in range(0, self._BOARD_DIM**2):
            row = i // self._BOARD_DIM
            column = i % self._BOARD_DIM
            yield (Coordinate(row, column), self._values[i])

    def _calculate_index(self, coordinate: Coordinate) -> int:
        return coordinate.row * self._BOARD_DIM + coordinate.col

    def __getitem__(self, coordinate: Coordinate) -> int:
        index = self._calculate_index(coordinate)
        return self._values[index]

    def __setitem__(self, coordinate: Coordinate, value: int) -> None:
        # Allow to set an initial empty cell to empty again
        valid_for_empty_cell = coordinate in self._initial_empty_cells and value == 0
        valid_for_cell = self.is_valid(coordinate, value)
        if valid_for_empty_cell or valid_for_cell:
            index = self._calculate_index(coordinate)
            self._values[index] = value
        else:
            raise InvalidCellValueException(f"Value {value} not valid for {coordinate}")

    def __str__(self) -> str:
        formated_rows = []
        for i in range(0, self._BOARD_DIM**2, self._BOARD_DIM):
            row = self._values[i : i + self._BOARD_DIM]
            template_string = ("| " + "{} | " * self._BOARD_DIM).strip()
            formated_row = template_string.format(*row)
            formated_rows.append("-" * len(formated_row))
            formated_rows.append(formated_row)
        formated_rows.append("-" * len(formated_rows[-1]))
        return f"{os.linesep}".join(formated_rows)
