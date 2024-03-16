"""PySuSo boards tests."""

import os
import re

import pytest
from pysuso.boards import Board, Coordinate
from pysuso.exceptions import (
    InvalidBoardError,
    InvalidCellValueError,
    InvalidIndexError,
)


@pytest.fixture(name="nested_list_raw_values")
def fixture_nested_list_raw_values() -> list[list[int]]:
    """Provide a valid Sudoku values as nested list."""
    return [
        [0, 5, 0, 7, 0, 3, 0, 6, 0],
        [0, 0, 7, 0, 0, 0, 8, 0, 0],
        [0, 0, 0, 8, 1, 6, 0, 0, 0],
        [0, 0, 0, 0, 3, 0, 0, 0, 0],
        [0, 0, 5, 0, 0, 0, 1, 0, 0],
        [7, 3, 0, 0, 4, 0, 0, 8, 6],
        [9, 0, 6, 0, 0, 0, 2, 0, 4],
        [8, 4, 0, 5, 7, 2, 0, 9, 3],
        [0, 0, 0, 4, 0, 9, 0, 0, 0],
    ]


@pytest.fixture(name="invalid_symbol_raw_values")
def fixture_invalid_symbol_raw_values() -> list[list[int | str]]:
    """Provide invalid Sudoku values as nested list."""
    return [
        ["?", 5, 0, 7, 0, 3, 0, 6, 0],
        [0, 0, 7, 0, 0, 0, 8, 0, 0],
        [0, 0, 0, 8, 1, 6, 0, 0, 0],
        [0, 0, 0, 0, 3, 0, 0, 0, 0],
        [0, 0, 5, 0, "?", 0, 1, 0, 0],
        [7, 3, 0, 0, 4, 0, 0, 8, 6],
        [9, 0, 6, 0, 0, 0, 2, 0, 4],
        [8, 4, 0, 5, 7, 2, 0, 9, 3],
        [0, 0, 0, 4, 0, 9, 0, 0, "?"],
    ]


@pytest.fixture(name="flat_list_raw_values")
def fixture_flat_list_raw_values() -> list[int]:
    """Provide valid Sudoku values as flat list."""
    # Swith off otherwise list will be formatted to one item per line
    # fmt: off
    return [
        0, 5, 0, 7, 0, 3, 0, 6, 0,
        0, 0, 7, 0, 0, 0, 8, 0, 0,
        0, 0, 0, 8, 1, 6, 0, 0, 0,
        0, 0, 0, 0, 3, 0, 0, 0, 0,
        0, 0, 5, 0, 0, 0, 1, 0, 0,
        7, 3, 0, 0, 4, 0, 0, 8, 6,
        9, 0, 6, 0, 0, 0, 2, 0, 4,
        8, 4, 0, 5, 7, 2, 0, 9, 3,
        0, 0, 0, 4, 0, 9, 0, 0, 0,
    ]
    # fmt: on


@pytest.fixture(name="flat_list_raw_values_invalid_length", scope="module")
def fixture_flat_list_raw_values_invalid_length() -> list[int]:
    """Provide a flat list with 78 instead of 81 values. Module scoped, do not change."""
    # Swith off otherwise list will be formatted to one item per line
    # fmt: off
    return [
        0, 5, 0, 7, 0, 3, 0, 6, 0,
        0, 0, 7, 0, 0, 0, 8, 0, 0,
        0, 0, 0, 8, 1, 6, 0, 0, 0,
        0, 0, 0, 0, 3, 0, 0, 0, 0,
        0, 0, 5, 0, 0, 0, 1, 0, 0,
        7, 3, 0, 0, 4, 0, 0, 8, 6,
        9, 0, 6, 0, 0, 0, 2, 0, 4,
        8, 4, 0, 5, 7, 2, 0, 9, 3,
        0, 0, 0, 4, 0, 9,
    ]
    # fmt: on


@pytest.fixture(name="flat_list_raw_values_invalid_values", scope="module")
def fixture_flat_list_raw_values_invalid_values() -> list[int | str]:
    """Provide a flat list with valid and invalid Sudoku values. Module scoped, do not change."""
    # Swith off otherwise list will be formatted to one item per line
    # fmt: off
    return [
        0, 5, 0, 7, 0, 3, 0, 6, 0,
        0, 0, 7, 0, -1, 0, 8, 0, 0,
        0, 0, 0, 8, 1, 6, 0, 0, 0,
        0, 0, 0, 0, 3, 0, 0, 0, 0,
        0, 0, 5, 0, 0, 0, 1, 0, 0,
        7, 3, 0, 0, 4, 0, 0, 10, 6,
        9, 0, 6, "😀", 0, 0, 2, 0,
        4, 8, 4, 0, 5, 7, 2, 0, 9,
        3, 0, 0, 0, 4, 0, 9, 0, 0,
        99,
    ]
    # fmt: on


@pytest.fixture(name="string_raw_values_valid", scope="module")
def fixture_string_raw_values_valid() -> str:
    """Provide valid values as a string."""
    return "050703060007000800000816000000030000005000100730040086906000204840572093000409000"


@pytest.fixture(name="string_raw_values_invalid_length", scope="module")
def fixture_string_raw_values_invalid_length() -> str:
    """Provide invalid number of elements as string."""
    return "050703060007000800000816000000030000005000100730040086906000204840572093000409"


@pytest.fixture(name="string_raw_values_invalid_chars", scope="module")
def fixture_string_raw_values_invalid_chars() -> str:
    """Provide invalid values as string."""
    return "050703060007000800000816000000030000?05000100730040086906😀002048405720930-04090亯0"


@pytest.fixture(name="invalid_number_of_rows")
def fixture_invalid_number_of_rows() -> list[list[int]]:
    """Provide a nested list with invalid number of rows."""
    return [
        [0, 5, 0, 7, 0, 3, 0, 6, 0],
        [0, 0, 7, 0, 0, 0, 8, 0, 0],
    ]


@pytest.fixture(name="invalid_number_of_columns")
def fixture_invalid_number_of_columns() -> list[list[int]]:
    """Provide a nested list with invalid number of columns."""
    return [
        [0, 5, 0, 7, 0, 3, 0, 6],
        [0, 0, 7, 0, 0, 0, 8, 0, 0],
        [0, 0, 0, 1, 6, 0, 0, 0],
        [0, 0, 0, 0, 3, 0, 0, 0, 0],
        [0, 0, 5, 0, 0, 0, 1, 0, 0],
        [7, 3, 0, 0, 4, 0, 0, 8, 6],
        [9, 0, 6, 0, 0, 0, 2, 0, 4],
        [8, 4, 0, 5, 7, 2, 0, 9, 3],
        [0, 0, 0, 4, 0, 0, 0, 0],
    ]


@pytest.fixture(name="valid_test_board")
def fixture_valid_test_board(nested_list_raw_values: list[list[int]]) -> Board:
    """Provide a Sudoku Board. Function scoped, can be change during tests."""
    return Board.from_nested_lists(nested_list_raw_values)


@pytest.fixture(name="allowed_values", scope="module")
def fixture_allowed_values() -> frozenset[int]:
    """Provide the valid values for a Sudoku board. Does not include the placeholder zero."""
    return frozenset(range(1, 10))


@pytest.fixture(name="square_top_left_edges", scope="module")
def fixture_square_top_left_edges() -> list[Coordinate]:
    """Provide the a list of coordinates describing the top left corners of the 3x3 squares of a Sudoku board."""
    return [Coordinate(row, col) for row in range(0, 9, 3) for col in range(0, 9, 3)]


@pytest.fixture(name="example_board_representation", scope="module")
def fixture_example_board_representation() -> str:
    """Provide the string representation of a Sudou board.

    Representation belonging to board created by fixture `nested_list_raw_values`.
    """
    return (
        f"-------------------------------------{os.linesep}| 0 | 5 | 0 | 7 | 0 | 3 | 0 | 6 | 0 |{os.linesep}"
        f"-------------------------------------{os.linesep}| 0 | 0 | 7 | 0 | 0 | 0 | 8 | 0 | 0 |{os.linesep}"
        f"-------------------------------------{os.linesep}| 0 | 0 | 0 | 8 | 1 | 6 | 0 | 0 | 0 |{os.linesep}"
        f"-------------------------------------{os.linesep}| 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 |{os.linesep}"
        f"-------------------------------------{os.linesep}| 0 | 0 | 5 | 0 | 0 | 0 | 1 | 0 | 0 |{os.linesep}"
        f"-------------------------------------{os.linesep}| 7 | 3 | 0 | 0 | 4 | 0 | 0 | 8 | 6 |{os.linesep}"
        f"-------------------------------------{os.linesep}| 9 | 0 | 6 | 0 | 0 | 0 | 2 | 0 | 4 |{os.linesep}"
        f"-------------------------------------{os.linesep}| 8 | 4 | 0 | 5 | 7 | 2 | 0 | 9 | 3 |{os.linesep}"
        f"-------------------------------------{os.linesep}| 0 | 0 | 0 | 4 | 0 | 9 | 0 | 0 | 0 |{os.linesep}"
        "-------------------------------------"
    ).strip()


class TestBoard:
    """Groups tests for the Board class."""

    def test_available_col_values(
        self,
        allowed_values: set[int],
        nested_list_raw_values: list[list[int]],
        valid_test_board: Board,
    ) -> None:
        """Test that the `available_col_values` method returns the correct values."""
        for col in range(9):
            used_column_values: set[int] = set()
            for row in range(9):
                used_column_values.add(nested_list_raw_values[row][col])
            unused_values = allowed_values.difference(used_column_values)
            board_available_column_values = valid_test_board.available_col_values(col)
            sym_diff = unused_values.symmetric_difference(board_available_column_values)
            assert sym_diff == set()

    @pytest.mark.parametrize(
        "invalid_index",
        [-1, 9],
    )
    def test_available_col_values_invalid_index(self, valid_test_board: Board, invalid_index: int) -> None:
        """Test behaviour of `available_col_values` method for an invalid index."""
        with pytest.raises(
            InvalidIndexError,
            match=re.escape(f"Expecting a column index betwenn 0 and 8, but {invalid_index} was given"),
        ):
            valid_test_board.available_col_values(invalid_index)

    def test_available_row_values(
        self,
        allowed_values: set[int],
        nested_list_raw_values: list[list[int]],
        valid_test_board: Board,
    ) -> None:
        """Test that the `available_row_values` method returns the correct values."""
        for row_num, row in enumerate(nested_list_raw_values):
            used_row_values = set(row)
            unused_values = allowed_values.difference(used_row_values)
            board_available_column_values = valid_test_board.available_row_values(row_num)
            sym_diff = unused_values.symmetric_difference(board_available_column_values)
            assert sym_diff == set()

    @pytest.mark.parametrize(
        "invalid_index",
        [-1, 9],
    )
    def test_available_row_values_invalid_index(self, valid_test_board: Board, invalid_index: int) -> None:
        """Test behaviour of `available_row_values` method for an invalid index."""
        with pytest.raises(
            InvalidIndexError, match=re.escape(f"Expecting a row index betwenn 0 and 8, but {invalid_index} was given")
        ):
            valid_test_board.available_row_values(invalid_index)

    def test_available_square_values(
        self,
        square_top_left_edges: list[Coordinate],
        allowed_values: set[int],
        nested_list_raw_values: list[list[int]],
        valid_test_board: Board,
    ) -> None:
        """Test that the `available_square_values` method returns the correct values."""
        for position in square_top_left_edges:
            used_square_values: set[int] = set()
            for row in range(position.row, position.row + 3):
                for col in range(position.col, position.col + 3):
                    used_square_values.add(nested_list_raw_values[row][col])
            unused_values = allowed_values.difference(used_square_values)
            board_available_column_values = valid_test_board.available_square_values(position)
            sym_diff = unused_values.symmetric_difference(board_available_column_values)
            assert sym_diff == set()

    def test_is_valid_with_valid_value(self, valid_test_board: Board) -> None:
        """Test that the `is_valid` method returns `True` for valid coordinates and values."""
        coordinate: Coordinate = Coordinate(0, 0)
        assert valid_test_board.is_valid(coordinate, 1)

    def test_is_valid_with_invalid_value(self, valid_test_board: Board) -> None:
        """Test that the `is_valid` method returns `False` for an invalid value."""
        position: Coordinate = Coordinate(0, 0)
        assert not valid_test_board.is_valid(position, 7)

    def test_board_iterator(self, nested_list_raw_values: list[list[int]], valid_test_board: Board) -> None:
        """Test that the board is iterated correctly."""
        for position, value in valid_test_board:
            assert value == nested_list_raw_values[position.row][position.col]

    def test_board_get_index(self, valid_test_board: Board, nested_list_raw_values: list[list[int]]) -> None:
        """Test that the indexing the board works correctly."""
        position = Coordinate(0, 1)
        board_value = valid_test_board[position]
        raw_value = nested_list_raw_values[position.row][position.col]
        assert board_value == raw_value

    def test_board_set_index_valid_value(self, valid_test_board: Board) -> None:
        """Test that setting a coordinate on the board works for a valid value."""
        coordinate = Coordinate(8, 8)
        valid_test_board[coordinate] = 1
        assert valid_test_board[coordinate] == 1

    def test_board_set_index_invalid_value(self, valid_test_board: Board) -> None:
        """Test that setting a coordinate on the board works for an invalid value raises an exception."""
        coordinate = Coordinate(0, 0)
        with pytest.raises(InvalidCellValueError, match=re.escape("Value 5 not valid for Coordinate(row=0, col=0)")):
            valid_test_board[coordinate] = 5

    def test_board_representation(self, valid_test_board: Board, example_board_representation: str) -> None:
        """Test that the board is printed in a human readable way."""
        board_representation = str(valid_test_board)
        assert example_board_representation == board_representation

    def test_create_board_from_nested_list_with_invalid_values(
        self, invalid_symbol_raw_values: list[list[int | str]]
    ) -> None:
        """Test creation of board from nested list with invald symbols."""
        exception_message = re.escape(
            f"Expect values between 0 and 9. Found invalid values:{os.linesep}"
            f"(0, 0): ?{os.linesep}(4, 4): ?{os.linesep}(8, 8): ?"
        )
        with pytest.raises(InvalidBoardError, match=exception_message):
            # Passing a list containing invalid types is part of the test hence ignore error.
            Board.from_nested_lists(invalid_symbol_raw_values)  # pyright: ignore reportArgumentType

    def test_create_board_from_nested_list_invalid_number_of_rows(
        self, invalid_number_of_rows: list[list[int]]
    ) -> None:
        """Test creation of board from nested list with invald number of rows."""
        with pytest.raises(InvalidBoardError, match=re.escape("Cannot create board. Expected 9 rows but received 2.")):
            Board.from_nested_lists(invalid_number_of_rows)

    def test_create_board_from_nested_list_invalid_number_of_columns(
        self, invalid_number_of_columns: list[list[int]]
    ) -> None:
        """Test creation of board from nested list with invald number of columns."""
        exception_message = re.escape(
            f"Cannot create board. Rows found with invalid length{os.linesep}"
            f"0: Expectec length 9, actual length 8{os.linesep}"
            f"2: Expectec length 9, actual length 8{os.linesep}"
            "8: Expectec length 9, actual length 8"
        )
        with pytest.raises(InvalidBoardError, match=exception_message):
            Board.from_nested_lists(invalid_number_of_columns)

    def test_create_board_from_flat_list_with_valid_values(self, flat_list_raw_values: list[int]) -> None:
        """Test creation of board from flat list with valid values."""
        board = Board.from_list(flat_list_raw_values)
        for coordinate, value in board:
            index = coordinate.row * 9 + coordinate.col
            assert value == flat_list_raw_values[index]

    def test_create_board_from_flat_list_invalid_length(
        self, flat_list_raw_values_invalid_length: list[int | str]
    ) -> None:
        """Test creation of board from flat list with invalid length."""
        with pytest.raises(
            InvalidBoardError,
            match=re.escape("Cannot create board. Expected 81 rows but received 78."),
        ):
            # Passing a list containing invalid types is part of the test hence ignore error.
            Board.from_list(flat_list_raw_values_invalid_length)  # pyright: ignore reportArgumentType

    def test_create_board_from_flat_list_invalid_values(
        self, flat_list_raw_values_invalid_values: list[int | str]
    ) -> None:
        """Test creation of board from flat list with invalid values."""
        exception_message = re.escape(
            f"Expect values between 0 and 9. Found invalid values:{os.linesep}"
            f"13: -1{os.linesep}"
            f"52: 10{os.linesep}"
            f"57: 😀{os.linesep}"
            "80: 99"
        )
        with pytest.raises(InvalidBoardError, match=exception_message):
            # Passing a list containing invalid types is part of the test hence ignore error.
            Board.from_list(flat_list_raw_values_invalid_values)  # pyright: ignore reportArgumentType

    def test_do_raise_if_constructor_is_used(self, flat_list_raw_values: list[int]) -> None:
        """Test that direct board constructor call raises an error."""
        with pytest.raises(
            RuntimeError,
            match=re.escape(
                "Calling the Board constructure is not supported. Use one of the factory methods to create a board."
            ),
        ):
            Board(flat_list_raw_values)

    def test_create_board_from_valid_string(self, string_raw_values_valid: str) -> None:
        """Test that a board is correctly created from a string with valid values."""
        board = Board.from_string(string_raw_values_valid)
        for coordinate, value in board:
            expected = int(string_raw_values_valid[coordinate.row * 9 + coordinate.col])
            assert expected == value

    def test_create_board_from_invalid_length(self, string_raw_values_invalid_length: str) -> None:
        """Test behaviour in case a board is created with too short string."""
        with pytest.raises(
            InvalidBoardError, match=re.escape("Cannot create board. Expected 81 values but received 78.")
        ):
            Board.from_string(string_raw_values_invalid_length)

    def test_create_board_from_invalid_chars(self, string_raw_values_invalid_chars: str) -> None:
        """Test behaviour in case a board is created with a string containing invalid values."""
        exception_message = re.escape(
            f"Error creating board. Found invalid values:{os.linesep}"
            f'36: Value "?" is not an integer{os.linesep}'
            f'57: Value "😀" is not an integer{os.linesep}'
            f'73: Value "-" is not an integer{os.linesep}'
            '79: Value "亯" is not an integer'
        )
        with pytest.raises(InvalidBoardError, match=exception_message):
            Board.from_string(string_raw_values_invalid_chars)


class TestCoordinate:
    """Test cases for the coordinate dataclass."""

    @pytest.mark.parametrize(
        ("row", "column"),
        [
            (-1, 10),
            (9, 5),
        ],
    )
    def test_coordinate_invalid_row(self, row: int, column: int) -> None:
        """Test that a coordinate cannot be created with an invalid row index."""
        with pytest.raises(ValueError, match=f"Row index needs to be between zero and eight. Given {row}"):
            Coordinate(row, column)

    @pytest.mark.parametrize(
        ("row", "column"),
        [
            (2, -1),
            (3, 9),
        ],
    )
    def test_coordinate_invalid_column(self, row: int, column: int) -> None:
        """Test that a coordinate cannot be created with an invalid column index."""
        with pytest.raises(ValueError, match=f"Column index needs to be between zero and eight. Given {column}"):
            Coordinate(row, column)
