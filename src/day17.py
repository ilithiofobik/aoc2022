import itertools

from collections import namedtuple
from operator import lshift, rshift
from typing import Literal, Optional


State = namedtuple("State", ["top_row", "jet_num", "shape_num"])


class Shape:
    cells: list[int]
    position: int

    def __init__(self, cells: list[int], position: int):
        self.cells = cells
        self.position = position

    def can_move_horizontal(
        self, board: set[tuple[int, int]], jet: Literal["<", ">"]
    ) -> bool:
        blocker = 0b1000000 if jet == "<" else 0b0000001

        if any(cell & blocker for cell in self.cells):
            return False

        op = lshift if jet == "<" else rshift
        new_cells = [op(cell, 1) for cell in self.cells]
        pos = self.position

        return all(board[pos + i] & cell == 0 for i, cell in enumerate(new_cells))

    def can_move_vertical(self, board: list[int]) -> bool:
        pos = self.position - 1
        return all(board[pos + i] & cell == 0 for i, cell in enumerate(self.cells))

    def move_vertical(self) -> None:
        self.position -= 1

    def move_horizontal(self, jet: Literal["<", ">"]) -> None:
        op = lshift if jet == "<" else rshift
        self.cells = [op(c, 1) for c in self.cells]

    def height(self) -> int:
        return self.position + len(self.cells) - 1

    def perform_full_fall(self, board: list[int], jets) -> None:
        is_horizontal = True
        movable = True
        last_jet = 0

        while movable:
            if is_horizontal:
                last_jet, jet = next(jets)
                if self.can_move_horizontal(board, jet):
                    self.move_horizontal(jet)

            else:
                movable = self.can_move_vertical(board)
                if movable:
                    self.move_vertical()

            is_horizontal = not is_horizontal

        return last_jet


class BoardData:
    def __init__(self):
        self.board = 10_000 * [0b0000000]
        self.board[0] = 0b1111111
        self.height = 0

    def add_shape(self, shape: Shape) -> None:
        self.height = max(self.height, shape.height())

        for i, cell in enumerate(shape.cells):
            self.board[shape.position + i] |= cell

    def current_state(self, last_jet: int, last_shape: int) -> State:
        return State(
            top_row=self.board[self.height],
            jet_num=last_jet,
            shape_num=last_shape,
        )


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


def get_jets():
    with open("data/day17.txt", "r", encoding="utf-8") as data:
        line = data.readline()
        jets_list = list(line.strip())
        return itertools.cycle(enumerate(jets_list))


def get_shape_getters():
    getters_list = [get_minus, get_plus, get_lshape, get_ishape, get_square]
    return itertools.cycle(enumerate(getters_list))


def try_to_simulate_cycle(curr_state, states, step, board_data, n) -> Optional[int]:
    if curr_state in states:
        prev_height, prev_step = states[curr_state]
        cycle_len = step - prev_step
        height_diff = board_data.height - prev_height
        remaining_steps = n - step

        cycles_left, remainder = divmod(remaining_steps, cycle_len)

        if remainder == 0:
            return board_data.height + cycles_left * height_diff

    states[curr_state] = board_data.height, step

    return None


def get_height(n: int) -> int:
    jets = get_jets()
    shape_getter = get_shape_getters()
    board_data = BoardData()
    states = {}

    for step in range(1, n + 1):
        last_shape, shape = next(shape_getter)
        shape = shape(position=board_data.height + 4)

        last_jet = shape.perform_full_fall(board_data.board, jets)
        board_data.add_shape(shape)
        curr_state = board_data.current_state(last_jet, last_shape)

        if result := try_to_simulate_cycle(curr_state, states, step, board_data, n):
            return result

    return board_data.height


def part1():
    return get_height(2022)


def part2():
    return get_height(1_000_000_000_000)
