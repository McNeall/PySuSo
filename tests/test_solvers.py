"""Contains the tests for the Sudoku solver implementation."""

import re

import pytest
from pysuso.boards import Board
from pysuso.exceptions import BoardNotSolvableException
from pysuso.solvers import BasicSolver


@pytest.fixture(name="easy_board")
def easy_board() -> Board:
    """Provide a board rated with a easy difficulty."""
    return Board.from_nested_lists(
        [
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
    )


@pytest.fixture(name="solution_easy_board")
def fixture_solution_easy_board() -> list[list[int]]:
    """Solution for board provided by fixture `easy_board`."""
    return [
        [1, 5, 8, 7, 2, 3, 4, 6, 9],
        [3, 6, 7, 9, 5, 4, 8, 2, 1],
        [2, 9, 4, 8, 1, 6, 3, 7, 5],
        [6, 1, 9, 2, 3, 8, 5, 4, 7],
        [4, 8, 5, 6, 9, 7, 1, 3, 2],
        [7, 3, 2, 1, 4, 5, 9, 8, 6],
        [9, 7, 6, 3, 8, 1, 2, 5, 4],
        [8, 4, 1, 5, 7, 2, 6, 9, 3],
        [5, 2, 3, 4, 6, 9, 7, 1, 8],
    ]


@pytest.fixture(name="medium_board")
def fixture_medium_board() -> Board:
    """Provide a board rated with a medium difficulty."""
    return Board.from_nested_lists(
        [
            [0, 0, 2, 0, 0, 0, 8, 0, 0],
            [0, 0, 5, 0, 2, 0, 1, 0, 0],
            [4, 6, 0, 0, 0, 0, 0, 2, 9],
            [1, 3, 0, 0, 6, 0, 0, 5, 2],
            [0, 0, 9, 0, 8, 0, 4, 0, 0],
            [0, 0, 0, 3, 0, 2, 0, 0, 0],
            [0, 0, 6, 0, 7, 0, 2, 0, 0],
            [7, 0, 0, 0, 0, 0, 0, 0, 8],
            [0, 2, 0, 5, 1, 9, 0, 7, 0],
        ]
    )


@pytest.fixture(name="solution_medium_board")
def fixture_solution_medium_board() -> list[list[int]]:
    """Solution for board provided by fixture `medium_board`."""
    return [
        [3, 1, 2, 9, 4, 7, 8, 6, 5],
        [9, 8, 5, 6, 2, 3, 1, 4, 7],
        [4, 6, 7, 8, 5, 1, 3, 2, 9],
        [1, 3, 8, 7, 6, 4, 9, 5, 2],
        [2, 7, 9, 1, 8, 5, 4, 3, 6],
        [6, 5, 4, 3, 9, 2, 7, 8, 1],
        [5, 9, 6, 4, 7, 8, 2, 1, 3],
        [7, 4, 1, 2, 3, 6, 5, 9, 8],
        [8, 2, 3, 5, 1, 9, 6, 7, 4],
    ]


@pytest.fixture(name="hard_board")
def fixture_hard_board() -> Board:
    """Provide a board rated with a hard difficulty."""
    return Board.from_nested_lists(
        [
            [0, 0, 0, 0, 0, 8, 4, 0, 0],
            [0, 0, 5, 0, 0, 0, 0, 2, 6],
            [0, 0, 3, 4, 0, 0, 9, 0, 8],
            [6, 0, 0, 2, 4, 0, 0, 3, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 8, 0, 0, 6, 9, 0, 0, 2],
            [2, 0, 8, 0, 0, 4, 6, 0, 0],
            [3, 7, 0, 0, 0, 0, 5, 0, 0],
            [0, 0, 6, 9, 0, 0, 0, 0, 0],
        ]
    )


@pytest.fixture(name="solution_hard_board")
def fixture_solution_hard_board() -> list[list[int]]:
    """Solution for board provided by fixture `hard_board`."""
    return [
        [9, 2, 1, 6, 3, 8, 4, 5, 7],
        [8, 4, 5, 7, 9, 1, 3, 2, 6],
        [7, 6, 3, 4, 5, 2, 9, 1, 8],
        [6, 1, 9, 2, 4, 7, 8, 3, 5],
        [4, 3, 2, 1, 8, 5, 7, 6, 9],
        [5, 8, 7, 3, 6, 9, 1, 4, 2],
        [2, 9, 8, 5, 1, 4, 6, 7, 3],
        [3, 7, 4, 8, 2, 6, 5, 9, 1],
        [1, 5, 6, 9, 7, 3, 2, 8, 4],
    ]


@pytest.fixture(name="diabolical_board")
def fixture_diabolical_board() -> Board:
    """Provide a board rated with a diabolical difficulty."""
    return Board.from_nested_lists(
        [
            [0, 5, 0, 9, 0, 8, 6, 0, 0],
            [8, 0, 0, 0, 0, 6, 0, 0, 7],
            [0, 0, 6, 0, 2, 0, 0, 0, 0],
            [0, 0, 9, 0, 0, 0, 0, 7, 0],
            [2, 0, 3, 0, 0, 0, 8, 0, 9],
            [0, 1, 0, 0, 0, 0, 4, 0, 0],
            [0, 0, 0, 0, 3, 0, 7, 0, 0],
            [9, 0, 0, 8, 0, 0, 0, 0, 4],
            [0, 0, 5, 6, 0, 4, 0, 3, 0],
        ]
    )


@pytest.fixture(name="solution_diabolical_board")
def fixture_solution_diabolical_board() -> list[list[int]]:
    """Solution for board provided by fixture `diabolical_board`."""
    return [
        [3, 5, 7, 9, 4, 8, 6, 2, 1],
        [8, 2, 1, 3, 5, 6, 9, 4, 7],
        [4, 9, 6, 7, 2, 1, 3, 8, 5],
        [5, 4, 9, 1, 8, 3, 2, 7, 6],
        [2, 7, 3, 4, 6, 5, 8, 1, 9],
        [6, 1, 8, 2, 7, 9, 4, 5, 3],
        [1, 6, 4, 5, 3, 2, 7, 9, 8],
        [9, 3, 2, 8, 1, 7, 5, 6, 4],
        [7, 8, 5, 6, 9, 4, 1, 3, 2],
    ]


@pytest.fixture(name="unsolvable_board")
def fixture_unsolvable_board() -> Board:
    """Provide an unsolvable board."""
    return Board.from_nested_lists(
        [
            [1, 5, 0, 7, 2, 3, 4, 0, 9],
            [3, 6, 7, 9, 5, 4, 8, 2, 1],
            [2, 9, 4, 8, 1, 6, 3, 7, 5],
            [6, 1, 9, 2, 3, 8, 5, 4, 7],
            [4, 8, 5, 6, 9, 7, 1, 3, 2],
            [7, 3, 2, 1, 4, 5, 9, 6, 6],
            [9, 7, 6, 3, 8, 1, 2, 5, 4],
            [8, 4, 1, 5, 7, 2, 6, 9, 3],
            [5, 2, 3, 4, 6, 9, 7, 1, 8],
        ]
    )


class TestBasicSolver:
    """Groups tests for the BasicSolver class."""

    @pytest.mark.parametrize(
        ("board_fixture", "solution_fixture"),
        [
            ("easy_board", "solution_easy_board"),
            ("medium_board", "solution_medium_board"),
            ("hard_board", "solution_hard_board"),
            ("diabolical_board", "solution_diabolical_board"),
        ],
    )
    def test_solver(self, board_fixture: str, solution_fixture: str, request: pytest.FixtureRequest) -> None:
        """Test solver againt boards of varying difficulity."""
        board: Board = request.getfixturevalue(board_fixture)
        solution: list[list[int]] = request.getfixturevalue(solution_fixture)
        solver = BasicSolver(board)
        solved_board = solver.solve()
        for position, value in solved_board:
            assert solution[position.row][position.col] == value, (
                f"Found value {value} but expected value "
                "{solution[position.row][position.col]} at position ({position.row}, {position.col})"
            )

    def test_unsolvable_board(self, unsolvable_board: Board) -> None:
        """Test solver with unsolvable board."""
        solver = BasicSolver(unsolvable_board)
        with pytest.raises(BoardNotSolvableException, match=re.escape("No valid solution found.")):
            solver.solve()
