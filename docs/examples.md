The solver provided by PySuSo expects an instance of `pysuso.boards.Board`. A `Board` instance should be created
by one of the factory methods.

## The `from_nested_lists` factory method

To create a board with the the  `from_neste_lists` factory method requires a list with nine elements,
each a list with nine integers between from zero to nine. The following code shows an example:

```py
from pysuso.boards import Board
from pysuso.solvers import BasicSolver

board = Board.from_nested_lists(
    [
        [0, 5, 0, 7, 0, 3, 0, 6, 0],
        [0, 0, 7, 0, 0, 0, 8, 0, 0],
        [0, 0, 0, 8, 1, 6, 0, 0, 0],
        [0, 0, 0, 0, 3, 0, 0, 0, 0],
        [0, 0, 5, 0, 0, 0, 1, 0, 0],
        [7, 3, 0, 0, 4, 0, 0, 8, 6],
        [9, 0, 6, 0, 0, 0, 2, 0, 4],
        [8, 4, 0, 5, 7, 2, 0, 9, 3],
        [0, 0, 0, 4, 0, 9, 0, 0, 0]
    ]
)
solver = BasicSolver(board)
solution = solver.solve()
print(solution)
# ┌───┬───┬───┬───┬───┬───┬───┬───┬───┐
# │ 1 │ 5 │ 8 │ 7 │ 2 │ 3 │ 4 │ 6 │ 9 │
# ├───┼───┼───┼───┼───┼───┼───┼───┼───┤
# │ 3 │ 6 │ 7 │ 9 │ 5 │ 4 │ 8 │ 2 │ 1 │
# ├───┼───┼───┼───┼───┼───┼───┼───┼───┤
# │ 2 │ 9 │ 4 │ 8 │ 1 │ 6 │ 3 │ 7 │ 5 │
# ├───┼───┼───┼───┼───┼───┼───┼───┼───┤
# │ 6 │ 1 │ 9 │ 2 │ 3 │ 8 │ 5 │ 4 │ 7 │
# ├───┼───┼───┼───┼───┼───┼───┼───┼───┤
# │ 4 │ 8 │ 5 │ 6 │ 9 │ 7 │ 1 │ 3 │ 2 │
# ├───┼───┼───┼───┼───┼───┼───┼───┼───┤
# │ 7 │ 3 │ 2 │ 1 │ 4 │ 5 │ 9 │ 8 │ 6 │
# ├───┼───┼───┼───┼───┼───┼───┼───┼───┤
# │ 9 │ 7 │ 6 │ 3 │ 8 │ 1 │ 2 │ 5 │ 4 │
# ├───┼───┼───┼───┼───┼───┼───┼───┼───┤
# │ 8 │ 4 │ 1 │ 5 │ 7 │ 2 │ 6 │ 9 │ 3 │
# ├───┼───┼───┼───┼───┼───┼───┼───┼───┤
# │ 5 │ 2 │ 3 │ 4 │ 6 │ 9 │ 7 │ 1 │ 8 │
# └───┴───┴───┴───┴───┴───┴───┴───┴───┘
```

## The `from_list` factory method

To create a board with the the  `from_list` factory method requires a list with 81 elements,
each an integer between zero to nine. The following code shows an example:

```py
from pysuso.boards import Board
from pysuso.solvers import BasicSolver

board = Board.from_list(
    [
        0, 5, 0, 7, 0, 3, 0, 6, 0,
        0, 0, 7, 0, 0, 0, 8, 0, 0,
        0, 0, 0, 8, 1, 6, 0, 0, 0,
        0, 0, 0, 0, 3, 0, 0, 0, 0,
        0, 0, 5, 0, 0, 0, 1, 0, 0,
        7, 3, 0, 0, 4, 0, 0, 8, 6,
        9, 0, 6, 0, 0, 0, 2, 0, 4,
        8, 4, 0, 5, 7, 2, 0, 9, 3,
        0, 0, 0, 4, 0, 9, 0, 0, 0
    ]
)
solver = BasicSolver(board)
solution = solver.solve()
print(solution)
# ┌───┬───┬───┬───┬───┬───┬───┬───┬───┐
# │ 1 │ 5 │ 8 │ 7 │ 2 │ 3 │ 4 │ 6 │ 9 │
# ├───┼───┼───┼───┼───┼───┼───┼───┼───┤
# │ 3 │ 6 │ 7 │ 9 │ 5 │ 4 │ 8 │ 2 │ 1 │
# ├───┼───┼───┼───┼───┼───┼───┼───┼───┤
# │ 2 │ 9 │ 4 │ 8 │ 1 │ 6 │ 3 │ 7 │ 5 │
# ├───┼───┼───┼───┼───┼───┼───┼───┼───┤
# │ 6 │ 1 │ 9 │ 2 │ 3 │ 8 │ 5 │ 4 │ 7 │
# ├───┼───┼───┼───┼───┼───┼───┼───┼───┤
# │ 4 │ 8 │ 5 │ 6 │ 9 │ 7 │ 1 │ 3 │ 2 │
# ├───┼───┼───┼───┼───┼───┼───┼───┼───┤
# │ 7 │ 3 │ 2 │ 1 │ 4 │ 5 │ 9 │ 8 │ 6 │
# ├───┼───┼───┼───┼───┼───┼───┼───┼───┤
# │ 9 │ 7 │ 6 │ 3 │ 8 │ 1 │ 2 │ 5 │ 4 │
# ├───┼───┼───┼───┼───┼───┼───┼───┼───┤
# │ 8 │ 4 │ 1 │ 5 │ 7 │ 2 │ 6 │ 9 │ 3 │
# ├───┼───┼───┼───┼───┼───┼───┼───┼───┤
# │ 5 │ 2 │ 3 │ 4 │ 6 │ 9 │ 7 │ 1 │ 8 │
# └───┴───┴───┴───┴───┴───┴───┴───┴───┘
```

## The `from_string` factory method

To create a board with the the  `from_string` factory method requires a string with 81 elements,
each an integer between zero to nine. The examples above can be modified as follows:

```py
from pysuso.boards import Board
from pysuso.solvers import BasicSolver

board = Board.from_string((
    "050703060"
    "007000800"
    "000816000"
    "000030000"
    "005000100"
    "730040086"
    "906000204"
    "840572093"
    "000409000"
))
solver = BasicSolver(board)
solution = solver.solve()
print(solution)
# ┌───┬───┬───┬───┬───┬───┬───┬───┬───┐
# │ 1 │ 5 │ 8 │ 7 │ 2 │ 3 │ 4 │ 6 │ 9 │
# ├───┼───┼───┼───┼───┼───┼───┼───┼───┤
# │ 3 │ 6 │ 7 │ 9 │ 5 │ 4 │ 8 │ 2 │ 1 │
# ├───┼───┼───┼───┼───┼───┼───┼───┼───┤
# │ 2 │ 9 │ 4 │ 8 │ 1 │ 6 │ 3 │ 7 │ 5 │
# ├───┼───┼───┼───┼───┼───┼───┼───┼───┤
# │ 6 │ 1 │ 9 │ 2 │ 3 │ 8 │ 5 │ 4 │ 7 │
# ├───┼───┼───┼───┼───┼───┼───┼───┼───┤
# │ 4 │ 8 │ 5 │ 6 │ 9 │ 7 │ 1 │ 3 │ 2 │
# ├───┼───┼───┼───┼───┼───┼───┼───┼───┤
# │ 7 │ 3 │ 2 │ 1 │ 4 │ 5 │ 9 │ 8 │ 6 │
# ├───┼───┼───┼───┼───┼───┼───┼───┼───┤
# │ 9 │ 7 │ 6 │ 3 │ 8 │ 1 │ 2 │ 5 │ 4 │
# ├───┼───┼───┼───┼───┼───┼───┼───┼───┤
# │ 8 │ 4 │ 1 │ 5 │ 7 │ 2 │ 6 │ 9 │ 3 │
# ├───┼───┼───┼───┼───┼───┼───┼───┼───┤
# │ 5 │ 2 │ 3 │ 4 │ 6 │ 9 │ 7 │ 1 │ 8 │
# └───┴───┴───┴───┴───┴───┴───┴───┴───┘
```