"""Contains expections specific to PySuSo."""


class InvalidBoardError(ValueError):
    """Raise in case the board cannot be created from the provided values."""


class InvalidCellValueError(ValueError):
    """Raise in case a value is not allowed in a cell."""


class InvalidIndexError(ValueError):
    """Raise in case an index is not valid."""


class BoardNotSolvableException(BaseException):
    """Raise in case the board does not have a solution."""
