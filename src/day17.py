import itertools
import dataclasses
import math

from collections import namedtuple
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


State = namedtuple("State", ["top_row", "jet_num", "shape_num"])


def get_height(n: int):
    with open("data/day17.txt", "r", encoding="utf-8") as data:
        line = data.readline()
        jets_list = list(line.strip())
        jets = itertools.cycle(enumerate(jets_list))
        shape_getter = itertools.cycle(enumerate(shape_getters))
        board = get_new_board()
        height = 0
        cycle_steps = math.lcm(len(jets_list), len(shape_getters))
        states = dict()

        for step in range(n):
            last_shape, shape = next(shape_getter)
            shape = shape(position=height + 4)
            is_horizontal = True
            movable = True
            last_jet = 0

            while movable:
                if is_horizontal:
                    last_jet, jet = next(jets)
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

            curr_state = State(
                top_row=board[height], jet_num=last_jet, shape_num=last_shape
            )

            if curr_state in states:
                prev_height, prev_step = states[curr_state]
                cycle_len = step - prev_step
                height_diff = height - prev_height
                remaining_steps = n - step - 1

                cycles_left, remainder = divmod(remaining_steps, cycle_len)

                if remainder == 0:
                    return height + cycles_left * height_diff

            states[curr_state] = height, step

        return height


def part1():
    return get_height(2022)


def part2():
    return get_height(1000000000000)
