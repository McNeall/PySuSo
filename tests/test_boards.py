import os
from typing import List, Set

import pytest

from pysuso.boards import Board, Coordinate
from pysuso.exceptions import (
    InvalidBoardException,
    InvalidCellValueException,
    InvalidIndexException,
)


@pytest.fixture(name="nested_list_raw_values", scope="module")
def fixture_nested_list_raw_values() -> List[List[int]]:
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


@pytest.fixture(name="invalid_symbol_raw_values", scope="module")
def fixture_invalid_symbol_raw_values() -> List[List[int | str]]:
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


@pytest.fixture(name="flat_list_raw_values", scope="module")
def fixture_flat_list_raw_values() -> List[int]:
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
def fixture_flat_list_raw_values_invalid_length() -> List[int]:
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
def fixture_flat_list_raw_values_invalid_values() -> List[int | str]:
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
    return "050703060007000800000816000000030000005000100730040086906000204840572093000409000"


@pytest.fixture(name="string_raw_values_invalid_length", scope="module")
def fixture_string_raw_values_invalid_length() -> str:
    return "050703060007000800000816000000030000005000100730040086906000204840572093000409"


@pytest.fixture(name="string_raw_values_invalid_chars", scope="module")
def fixture_string_raw_values_invalid_chars() -> str:
    return "050703060007000800000816000000030000?05000100730040086906😀002048405720930-04090亯0"


@pytest.fixture(name="invalid_number_of_rows", scope="module")
def fixture_invalid_number_of_rows() -> List[List[int]]:
    return [
        [0, 5, 0, 7, 0, 3, 0, 6, 0],
        [0, 0, 7, 0, 0, 0, 8, 0, 0],
    ]


@pytest.fixture(name="invalid_number_of_columns", scope="module")
def fixture_invalid_number_of_columns() -> List[List[int]]:
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


@pytest.fixture(name="function_scope_test_board", scope="function")
def fixture_function_scope_test_board(nested_list_raw_values: List[List[int]]) -> Board:
    return Board.from_nested_lists(nested_list_raw_values)


@pytest.fixture(name="module_scope_test_board", scope="module")
def fixture_module_scope_test_board(nested_list_raw_values: List[List[int]]) -> Board:
    return Board.from_nested_lists(nested_list_raw_values)


@pytest.fixture(name="allowed_values", scope="module")
def fixture_allowed_values() -> Set[int]:
    return set(range(1, 10))


@pytest.fixture(name="square_top_left_edges", scope="module")
def fixture_square_top_left_edges() -> List[Coordinate]:
    return [Coordinate(row, col) for row in range(0, 9, 3) for col in range(0, 9, 3)]


@pytest.fixture(name="example_board_representation", scope="module")
def fixture_example_board_representation() -> str:
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

    def test_available_col_values(
        self,
        allowed_values: Set[int],
        nested_list_raw_values: List[List[int]],
        module_scope_test_board: Board,
    ) -> None:
        for col in range(0, 9):
            used_column_values = set()
            for row in range(0, 9):
                used_column_values.add(nested_list_raw_values[row][col])
            unused_values = allowed_values.difference(used_column_values)
            board_available_column_values = module_scope_test_board.available_col_values(col)
            sym_diff = unused_values.symmetric_difference(board_available_column_values)
            assert sym_diff == set()

    def test_available_col_values_invalid_index(self, module_scope_test_board: Board) -> None:
        with pytest.raises(InvalidIndexException) as excinfo:
            module_scope_test_board.available_col_values(9)
        assert str(excinfo.value) == "Expecting a column index betwenn 0 and 8, but 9 was given"

    def test_available_row_values(
        self,
        allowed_values: Set[int],
        nested_list_raw_values: List[List[int]],
        module_scope_test_board: Board,
    ) -> None:
        for row_num, row in enumerate(nested_list_raw_values):
            used_row_values = set(row)
            unused_values = allowed_values.difference(used_row_values)
            board_available_column_values = module_scope_test_board.available_row_values(row_num)
            sym_diff = unused_values.symmetric_difference(board_available_column_values)
            assert sym_diff == set()

    def test_available_row_values_invalid_index(self, module_scope_test_board: Board) -> None:
        with pytest.raises(InvalidIndexException) as excinfo:
            module_scope_test_board.available_row_values(9)
        assert str(excinfo.value) == "Expecting a row index betwenn 0 and 8, but 9 was given"

    def test_available_square_values(
        self,
        square_top_left_edges: List[Coordinate],
        allowed_values: Set[int],
        nested_list_raw_values: List[List[int]],
        module_scope_test_board: Board,
    ) -> None:
        for position in square_top_left_edges:
            used_square_values = set()
            for row in range(position.row, position.row + 3):
                for col in range(position.col, position.col + 3):
                    used_square_values.add(nested_list_raw_values[row][col])
            unused_values = allowed_values.difference(used_square_values)
            board_available_column_values = module_scope_test_board.available_square_values(position)
            sym_diff = unused_values.symmetric_difference(board_available_column_values)
            assert sym_diff == set()

    def test_is_valid_with_valid_value(self, module_scope_test_board: Board) -> None:
        coordinate: Coordinate = Coordinate(0, 0)
        assert module_scope_test_board.is_valid(coordinate, 1)

    def test_is_valid_with_invalid_value(self, module_scope_test_board: Board) -> None:
        position: Coordinate = Coordinate(0, 0)
        assert not module_scope_test_board.is_valid(position, 7)

    def test_board_iterator(self, nested_list_raw_values: List[List[int]], module_scope_test_board: Board) -> None:
        for position, value in module_scope_test_board:
            assert value == nested_list_raw_values[position.row][position.col]

    def test_board_get_index(self, module_scope_test_board: Board, nested_list_raw_values: List[List[int]]) -> None:
        position = Coordinate(0, 1)
        board_value = module_scope_test_board[position]
        raw_value = nested_list_raw_values[position.row][position.col]
        assert board_value == raw_value

    def test_board_set_index_valid_value(self, function_scope_test_board: Board) -> None:
        coordinate = Coordinate(8, 8)
        function_scope_test_board[coordinate] = 1
        assert function_scope_test_board[coordinate] == 1

    def test_board_set_index_invalid_value(self, function_scope_test_board: Board) -> None:
        coordinate = Coordinate(0, 0)
        with pytest.raises(InvalidCellValueException) as excinfo:
            function_scope_test_board[coordinate] = 5
        assert str(excinfo.value) == "Value 5 not valid for Coordinate(row=0, col=0)"

    def test_board_representation(self, module_scope_test_board: Board, example_board_representation: str) -> None:
        board_representation = str(module_scope_test_board)
        assert example_board_representation == board_representation

    def test_create_board_from_nested_list_with_invalid_values(
        self, invalid_symbol_raw_values: List[List[int | str]]
    ) -> None:
        with pytest.raises(InvalidBoardException) as excinfo:
            # Passing a list containing invalid types is part of the test hence ignore error.
            Board.from_nested_lists(invalid_symbol_raw_values)  # type: ignore
        assert str(excinfo.value) == (
            f"Expect values between 0 and 9. Found invalid values:{os.linesep}"
            f"(0, 0): ?{os.linesep}(4, 4): ?{os.linesep}(8, 8): ?"
        )

    def test_create_board_from_nested_list_invalid_number_of_rows(
        self, invalid_number_of_rows: List[List[int]]
    ) -> None:
        with pytest.raises(InvalidBoardException) as excinfo:
            Board.from_nested_lists(invalid_number_of_rows)
        assert str(excinfo.value) == "Cannot create board. Expected 9 rows but received 2."

    def test_create_board_from_nested_list_invalid_number_of_columns(
        self, invalid_number_of_columns: List[List[int]]
    ) -> None:
        with pytest.raises(InvalidBoardException) as excinfo:
            Board.from_nested_lists(invalid_number_of_columns)
        assert str(excinfo.value) == (
            f"Cannot create board. Rows found with invalid length{os.linesep}"
            f"0: Expectec length 9, actual length 8{os.linesep}"
            f"2: Expectec length 9, actual length 8{os.linesep}"
            "8: Expectec length 9, actual length 8"
        )

    def test_create_board_from_flat_list_with_valid_values(self, flat_list_raw_values: List[int]) -> None:
        board = Board.from_list(flat_list_raw_values)
        for coordinate, value in board:
            index = coordinate.row * 9 + coordinate.col
            assert value == flat_list_raw_values[index]

    def test_create_board_from_flat_list_invalid_length(
        self, flat_list_raw_values_invalid_length: List[int | str]
    ) -> None:
        with pytest.raises(InvalidBoardException) as excinfo:
            # Passing a list containing invalid types is part of the test hence ignore error.
            Board.from_list(flat_list_raw_values_invalid_length)  # type: ignore
        assert str(excinfo.value) == "Cannot create board. Expected 81 rows but received 78."

    def test_create_board_from_flat_list_invalid_values(
        self, flat_list_raw_values_invalid_values: List[int | str]
    ) -> None:
        with pytest.raises(InvalidBoardException) as excinfo:
            # Passing a list containing invalid types is part of the test hence ignore error.
            Board.from_list(flat_list_raw_values_invalid_values)  # type: ignore
        assert str(excinfo.value) == (
            f"Expect values between 0 and 9. Found invalid values:{os.linesep}"
            f"13: -1{os.linesep}"
            f"52: 10{os.linesep}"
            f"57: 😀{os.linesep}"
            "80: 99"
        )

    def test_do_raise_if_constructor_is_used(self, flat_list_raw_values: List[int]) -> None:
        with pytest.raises(RuntimeError) as excinfo:
            Board(flat_list_raw_values)
        assert (
            str(excinfo.value)
            == "Calling the Board constructure is not supported. Use one of the factory methods to create a board."
        )

    def test_create_board_from_valid_string(self, string_raw_values_valid: str) -> None:
        board = Board.from_string(string_raw_values_valid)
        for coordinate, value in board:
            expected = int(string_raw_values_valid[coordinate.row * 9 + coordinate.col])
            assert expected == value

    def test_create_board_from_invalid_length(self, string_raw_values_invalid_length: str) -> None:
        with pytest.raises(InvalidBoardException) as excinfo:
            Board.from_string(string_raw_values_invalid_length)
        assert str(excinfo.value) == "Cannot create board. Expected 81 values but received 78."

    def test_create_board_from_invalid_chars(self, string_raw_values_invalid_chars: str) -> None:
        with pytest.raises(InvalidBoardException) as excinfo:
            Board.from_string(string_raw_values_invalid_chars)
        assert str(excinfo.value) == (
            f"Error creating board. Found invalid values:{os.linesep}"
            f'36: Value "?" is not an integer{os.linesep}'
            f'57: Value "😀" is not an integer{os.linesep}'
            f'73: Value "-" is not an integer{os.linesep}'
            '79: Value "亯" is not an integer'
        )


class TestCoordinate:

    def test_coordinate_invalid_row(self) -> None:
        """Test that a coordinate cannot be created with an invalid row index."""
        with pytest.raises(ValueError) as excinfo:
            Coordinate(-1, 10)
        assert str(excinfo.value) == "Row index needs to be between zero and eight. Given -1"

    def test_coordinate_invalid_column(self) -> None:
        """Test that a coordinate cannot be created with an invalid column index."""
        with pytest.raises(ValueError) as excinfo:
            Coordinate(0, 10)
        assert str(excinfo.value) == "Column index needs to be between zero and eight. Given 10"
