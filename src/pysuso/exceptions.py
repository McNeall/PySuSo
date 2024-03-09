"""This module contains expections specific to PySuSo"""


class InvalidBoardException(ValueError):
    """Raise in case the board cannot be created from the provided values"""


class InvalidCellValueException(ValueError):
    """Raise in case a value is not allowed in a cell"""


class InvalidIndexException(ValueError):
    "Raise in case an index is not valid"


class BoardNotSolvableException(BaseException):
    """Raise in case the board does not have a solution."""
