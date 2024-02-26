from dataclasses import dataclass


@dataclass
class Coordinate:
    row: int
    col: int

    def __post_init__(self) -> None:
        if self.row < 0 or self.row >= 9:
            raise ValueError(f"Row index needs to be between zero and eight. Given {self.row}")
        if self.col < 0 or self.col >= 9:
            raise ValueError(f"Column index needs to be between zero and eight. Given {self.col}")


class Board:
    pass
