"""Contains an implementation of a Sudoku board and related objects."""

from __future__ import annotations

import os
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING

from pysuso.exceptions import (
    InvalidBoardError,
    InvalidCellValueError,
    InvalidIndexError,
)

# Required to avoid circular imports. Skips import at runtime.
if TYPE_CHECKING:
    from collections.abc import Iterator


@dataclass(frozen=True)
class Coordinate:
    """Represents a coordinate on a board.

    The indices passed to the dataclass are validate. A coordinate is immutable.

    Args:
        row: Row index of the coordinate. Needs to be between 0 and 8, both included.
        col: Col index of the coordinate. Needs to be between 0 and 8, both included.

    Raises:
        ValueError: If row or column index are invalid. Indizes are invalid in case they are not
            between zero and 8, both included.

    """

    _INDEX_LOWER_BOUND = 0
    _INDEX_UPPER_BOUND = 8
    row: int
    col: int

    def __post_init__(self) -> None:
        """Validate rules for coordiante."""
        if self.row < self._INDEX_LOWER_BOUND or self.row > self._INDEX_UPPER_BOUND:
            message = f"Row index needs to be between zero and eight. Given {self.row}"
            raise ValueError(message)
        if self.col < self._INDEX_LOWER_BOUND or self.col > self.row > self._INDEX_UPPER_BOUND:
            message = f"Column index needs to be between zero and eight. Given {self.col}"
            raise ValueError(message)


class CallType(Enum):
    """Used to specify the allowed call types of the Board constructor."""

    PRIVATE = 1
    NON_PRIVATE = 2


class Board:
    """Presenting a possibly unfinished Sudoku board."""

    _BOARD_DIM = 9
    _SQUARE_SIZE = 3
    _VALID_VALUES = frozenset(range(1, _BOARD_DIM + 1))

    def __init__(self, values: list[int], _call_type: CallType = CallType.NON_PRIVATE) -> None:
        """Initialize the Board. Should not be called from outside the class.

        The constructure initializes the class but assumes a valid input. Do not not directly
        instantiate this class. Use one of the factory methods:

        - from_nested_lists
        - from_string
        - from_list

        Args:
            values: Values to initialize the Board. Values are not checked.
            _call_type: Indicates if the constructor was called from outside the class.
                Defaults to 'True'.

        Raises:
            RuntimeError: If constructor is called directly, that is not using one of the listed
                factory methods

        """
        if _call_type != CallType.PRIVATE:
            message = (
                "Calling the Board constructure is not supported. Use one of the factory methods to create a board."
            )
            raise RuntimeError(message)
        self._values: list[int] = values
        self._initial_empty_cells: set[Coordinate] = {
            Coordinate(i // self._BOARD_DIM, i % self._BOARD_DIM) for i, value in enumerate(values) if value == 0
        }

    @classmethod
    def from_nested_lists(cls, values: list[list[int]]) -> Board:
        """Return a new Board based on the passed values.

        The passed argument needs to have exactly nine elements. Each of them has to be a list
        with nine integers between zero and nine, both included. A value of zero marks an empty field.

        Args:
            values: The values used to create the board

        Returns:
            Board: Board holding the values given by `values`.

        Raises:
            InvalidBoardException: Raised in the following cases:

                - If the outter list has less than nine inner lists.
                - If an inner list has less than nine elements.
                - If the values are not between zero and nine.

        """
        if len(values) != cls._BOARD_DIM:
            message = f"Cannot create board. Expected {cls._BOARD_DIM} rows but received {len(values)}."
            raise InvalidBoardError(message)

        invalid_row_length = {i: len(row) for i, row in enumerate(values) if len(row) != cls._BOARD_DIM}
        if invalid_row_length:
            message = ["Cannot create board. Rows found with invalid length"]
            message.extend(
                (
                    f"{row_index}: Expectec length {cls._BOARD_DIM}, actual length {row_length}"
                    for row_index, row_length in invalid_row_length.items()
                )
            )
            raise InvalidBoardError(f"{os.linesep}".join(message))
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
            raise InvalidBoardError(f"{os.linesep}".join(message))
        return cls([value for row in values for value in row], _call_type=CallType.PRIVATE)

    @classmethod
    def from_list(cls, values: list[int]) -> Board:
        """Return a new Board based on the passed values.

        The passed argument needs to have exactly 81 integers between 0 and 9, both included.
        A value of zero marks an empty field.

        Args:
            values: The values used to create the board.

        Returns:
            Board: Board holding the values given by `values`.

        Raises:
            InvalidBoardException: Raised in the following cases:

                - If `values` does not have exactly 81 elements
                - If elements of `values` are not between 0 and 9, both included.

        """
        if len(values) != cls._BOARD_DIM**2:
            message = f"Cannot create board. Expected {cls._BOARD_DIM ** 2} rows but received {len(values)}."
            raise InvalidBoardError(message)
        valid_values_with_placeholder = cls._VALID_VALUES.union([0])
        invalid_values = {i: value for i, value in enumerate(values) if value not in valid_values_with_placeholder}
        if invalid_values:
            message = ["Expect values between 0 and 9. Found invalid values:"]
            message.extend((f"{index}: {value}" for index, value in invalid_values.items()))
            raise InvalidBoardError(f"{os.linesep}".join(message))
        return cls(values, _call_type=CallType.PRIVATE)

    @classmethod
    def from_string(cls, values: str) -> Board:
        """Return a new Board based on the passed values.

        The passed string needs to have exactly 81 characters. Each character being an integer

        Args:
            values: The values used to create the board

        Returns:
            Board holding the values given by `values` after converting to integer

        Raises:
            InvalidBoardException: Raised in the following cases:

                - If the passed string does not have exactly 81 characters
                - If there is a character that is not convertible to an integer
                - If the converted characters are not integers between zero and nine

        """
        if len(values) != cls._BOARD_DIM**2:
            message = f"Cannot create board. Expected {cls._BOARD_DIM ** 2} values but received {len(values)}."
            raise InvalidBoardError(message)
        invalid_positions: dict[int, str] = {}
        valid_values: list[int] = []
        for i, value in enumerate(values):
            try:
                converted_value = int(value)
                valid_values.append(converted_value)
            except ValueError:
                invalid_positions[i] = f'Value "{value}" is not an integer'

        if invalid_positions:
            message = ["Error creating board. Found invalid values:"]
            message.extend((f"{index}: {message}" for index, message in invalid_positions.items()))
            raise InvalidBoardError(f"{os.linesep}".join(message))
        return cls(valid_values, _call_type=CallType.PRIVATE)

    def available_col_values(self, column_index: int) -> frozenset[int]:
        """Return the allowed but unused values for the column given by column_index.

        Args:
            column_index: The column index starting at 0.

        Returns:
            Values available for the row indentified by the passed row_index

        Raises:
            InvalidIndexException: If `column_index` is less than 0 or greater or equal 9.

        """
        if column_index < 0 or column_index >= self._BOARD_DIM:
            message = f"Expecting a column index betwenn 0 and 8, but {column_index} was given"
            raise InvalidIndexError(message)
        values_in_column = set(self._values[column_index : self._BOARD_DIM**2 : self._BOARD_DIM])
        return Board._VALID_VALUES.difference(values_in_column)

    def available_row_values(self, row_index: int) -> frozenset[int]:
        """Return the allowed but unused values for the row given by row_index.

        Args:
            row_index: The row index starting at 0. Values has to be between 0 and 8.

        Returns:
            Values available for the row indentified by the passed row_index

        Raises:
            InvalidIndexException: If `row_index` is less than 0 or greater or equal 9.

        """
        if row_index < 0 or row_index >= self._BOARD_DIM:
            message = f"Expecting a row index betwenn 0 and 8, but {row_index} was given"
            raise InvalidIndexError(message)
        values_in_row = set(self._values[self._BOARD_DIM * row_index : self._BOARD_DIM * (row_index + 1)])
        return Board._VALID_VALUES.difference(values_in_row)

    def available_square_values(self, coordinate: Coordinate) -> frozenset[int]:
        """Return the allowed but unused values of the 3x3 square that contains the coordinate.

        Args:
            coordinate: coordinate used to determine the square for which the values should be returned.

        Returns:
            Values available for the 3x3 square the given coordinate is located in.

        """
        top_left = Coordinate(
            coordinate.row - coordinate.row % self._SQUARE_SIZE,
            coordinate.col - coordinate.col % self._SQUARE_SIZE,
        )
        values_in_square: set[int] = set()
        for i in range(Board._SQUARE_SIZE):
            start_index = (top_left.row + i) * self._BOARD_DIM + top_left.col
            values_in_square.update(self._values[start_index : start_index + 3])
        return Board._VALID_VALUES.difference(values_in_square)

    def is_valid(self, coordinate: Coordinate, value: int) -> bool:
        """Check that `value` is valid for `coordinate` based on the current state of the board.

        A value is seen as valid if all of the following cases hold:

        - Value is between 1 and 9 both included.
        - Value is not yet present in the row the cell belongs to.
        - Value is not yet present in the column the cell belongs to.
        - Value is not yet present in the 3x3 square the cell is in.

        Args:
            coordinate: Position on the board.
            value: Value for position given by `coordinate`.

        Returns:
            `True` if value is valid for `coordinate` otherwise `False`.

        """
        if value not in self._VALID_VALUES:
            return False
        if (
            value in self.available_row_values(coordinate.row)
            and value in self.available_col_values(coordinate.col)
            and value in self.available_square_values(coordinate)
        ):
            return True
        return False

    def __iter__(self) -> Iterator[tuple[Coordinate, int]]:
        """Iterate through the board left to right, top to bottom.

        Return an iterator which allows to walk the board from left to right and top to bottom. The
        iterator returns a tuple that has a Coordinate as first entry and the current value of the
        board at the coordinate as the second entry.

        Returns:
            Tuple with first element Coordinate and second element integer value at the given
                coordinate.

        """
        for i in range(self._BOARD_DIM**2):
            row = i // self._BOARD_DIM
            column = i % self._BOARD_DIM
            yield (Coordinate(row, column), self._values[i])

    def _calculate_index(self, coordinate: Coordinate) -> int:
        """Calcuate the index of the given coordinate in the internal value storage.

        Args:
            coordinate: Coordinate for which the index should be calculated.

        Returns:
            Index that corresponds to the `coordinate`.

        """
        return coordinate.row * self._BOARD_DIM + coordinate.col

    def __getitem__(self, coordinate: Coordinate) -> int:
        """Return the value at `coordinate`.

        Args:
            coordinate: Coordinate of the cell for which to return the value.

        Returns:
            Value of the cell given by `coordinate`.

        """
        index = self._calculate_index(coordinate)
        return self._values[index]

    def __setitem__(self, coordinate: Coordinate, value: int) -> None:
        """Set `value` at `coordinate` in case the value is valid for this position.

        Args:
            coordinate: Position on the board that should be updated.
            value: New value.

        Raises:
            InvalidCellValueException: If `value` is not valid for position given by `coordinate`.
                A value is valid if one of the following cases holds:
                - The coordinate was initially empty and the value is 0.
                - The value fulfills the conditions of a valid sudoku board. See `is_valid` method.

        """
        # Allow to set an initial empty cell to empty again
        valid_for_empty_cell = coordinate in self._initial_empty_cells and value == 0
        valid_for_cell = self.is_valid(coordinate, value)
        if valid_for_empty_cell or valid_for_cell:
            index = self._calculate_index(coordinate)
            self._values[index] = value
        else:
            message = f"Value {value} not valid for {coordinate}"
            raise InvalidCellValueError(message)

    def __str__(self) -> str:
        """Return a string representation of the board."""
        formated_rows: list[str] = []
        for i in range(0, self._BOARD_DIM**2, self._BOARD_DIM):
            row = self._values[i : i + self._BOARD_DIM]
            template_string = ("| " + "{} | " * self._BOARD_DIM).strip()
            formated_row = template_string.format(*row)
            formated_rows.append("-" * len(formated_row))
            formated_rows.append(formated_row)
        formated_rows.append("-" * len(formated_rows[-1]))
        return f"{os.linesep}".join(formated_rows)
