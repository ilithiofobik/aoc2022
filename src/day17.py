import itertools
import dataclasses

from operator import lshift, rshift
from typing import Literal


@dataclasses.dataclass
class Shape:
    cells: list[int]
    position: int

    def move_vertical(self) -> None:
        self.position -= 1

    def move_horizontal(self, jet: Literal["<", ">"]) -> None:
        op = lshift if jet == "<" else rshift
        self.cells = [op(c, 1) for c in self.cells]

    def height(self) -> int:
        return self.position + len(self.cells) - 1


def get_minus(position: int) -> Shape:
    return Shape(cells=[0b0011110], position=position)


def get_plus(position: int) -> Shape:
    return Shape(cells=[0b0001000, 0b0011100, 0b0001000], position=position)


def get_lshape(position: int) -> Shape:
    return Shape(cells=[0b0011100, 0b0000100, 0b0000100], position=position)


def get_ishape(position: int) -> Shape:
    return Shape(cells=[0b0010000, 0b0010000, 0b0010000, 0b0010000], position=position)


def get_square(position: int) -> Shape:
    return Shape(cells=[0b0011000, 0b0011000], position=position)


shape_getters = [get_minus, get_plus, get_lshape, get_ishape, get_square]


def can_move_horizontal(
    board: set[tuple[int, int]], shape: Shape, jet: Literal["<", ">"]
) -> bool:
    blocker = 0b1000000 if jet == "<" else 0b0000001

    if any(cell & blocker for cell in shape.cells):
        return False

    op = lshift if jet == "<" else rshift
    new_cells = [op(cell, 1) for cell in shape.cells]
    pos = shape.position

    return all(board[pos + i] & cell == 0 for i, cell in enumerate(new_cells))


def can_move_vertical(board: list[int], shape: Shape) -> bool:
    pos = shape.position - 1
    return all(board[pos + i] & cell == 0 for i, cell in enumerate(shape.cells))


def get_new_board() -> list[int]:
    board = 10_000 * [0b0000000]
    board[0] = 0b1111111
    return board


def get_height(n: int):
    with open("data/day17.txt", "r", encoding="utf-8") as data:
        line = data.readline()
        jets = itertools.cycle(list(line.strip()))
        shape_getter = itertools.cycle(shape_getters)
        board = get_new_board()
        height = 0

        for _ in range(n):
            shape = next(shape_getter)(position=height + 4)
            is_horizontal = True
            movable = True

            while movable:
                if is_horizontal:
                    jet = next(jets)
                    if can_move_horizontal(board, shape, jet):
                        shape.move_horizontal(jet)

                else:
                    movable = can_move_vertical(board, shape)
                    if movable:
                        shape.move_vertical()

                is_horizontal = not is_horizontal

            height = max(height, shape.height())

            for i, cell in enumerate(shape.cells):
                board[shape.position + i] |= cell

        return height


def part1():
    return get_height(2022)


def part2():
    return get_height(1)
