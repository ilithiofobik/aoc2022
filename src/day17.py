import itertools
import dataclasses

from typing import Literal


@dataclasses.dataclass
class Shape:
    cells: list[tuple[int, int]]
    position: tuple[int, int]

    def move_vertical(self):
        self.position = (self.position[0] - 1, self.position[1])

    def move_horizontal(self, jet: Literal["<", ">"]):
        diff = 1 if jet == ">" else -1
        self.position = (self.position[0], self.position[1] + diff)

    def height(self):
        return max(x for x, _ in self.cells) + self.position[0]

    def absolute_cells(self) -> set[tuple[int, int]]:
        return {(self.position[0] + x, self.position[1] + y) for x, y in self.cells}


def get_minus(position: tuple[int, int]) -> Shape:
    return Shape(cells=[(0, 0), (0, 1), (0, 2), (0, 3)], position=position)


def get_plus(position: tuple[int, int]) -> Shape:
    return Shape(cells=[(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)], position=position)


def get_lshape(position: tuple[int, int]) -> Shape:
    return Shape(cells=[(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)], position=position)


def get_ishape(position: tuple[int, int]) -> Shape:
    return Shape(cells=[(0, 0), (1, 0), (2, 0), (3, 0)], position=position)


def get_square(position: tuple[int, int]) -> Shape:
    return Shape(cells=[(0, 0), (0, 1), (1, 0), (1, 1)], position=position)


shape_getters = [get_minus, get_plus, get_lshape, get_ishape, get_square]


def is_solid(board: set[tuple[int, int]], position: tuple[int, int]) -> bool:
    x, y = position
    return x <= 0 or y < 0 or y >= 7 or (x, y) in board


def can_move_horizontal(
    board: set[tuple[int, int]], shape: Shape, jet: Literal["<", ">"]
) -> bool:
    diff = 1 if jet == ">" else -1
    abs_x, abs_y = shape.position
    return all(
        not is_solid(board, (abs_x + x, abs_y + y + diff)) for x, y in shape.cells
    )


def can_move_vertical(board: set[tuple[int, int]], shape: Shape) -> bool:
    abs_x, abs_y = shape.position
    return all(not is_solid(board, (abs_x + x - 1, abs_y + y)) for x, y in shape.cells)


def get_height(n: int):
    with open("data/day17.txt", "r", encoding="utf-8") as data:
        line = data.readline()
        jets = itertools.cycle(list(line.strip()))
        shape_getter = itertools.cycle(shape_getters)
        board = set()
        height = 0

        for _ in range(n):
            shape = next(shape_getter)(position=(height + 4, 2))
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
            board.update(shape.absolute_cells())

        return height


def part1():
    return get_height(2022)


def part2():
    return get_height(1)
