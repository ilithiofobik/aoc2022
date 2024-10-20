import copy
from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass
from enum import IntEnum
from math import gcd
from typing import Optional


class DirectionChange(IntEnum):
    L = 3
    R = 1


class Direction(IntEnum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3


Instruction = int | DirectionChange


def read_instructions(line: str) -> list[Instruction]:
    instructions = []
    curr = 0

    for c in line.strip():
        if c.isdigit():
            curr = curr * 10 + int(c)
        else:
            if curr:
                instructions.append(curr)
                curr = 0
            instructions.append(DirectionChange.L if c == "L" else DirectionChange.R)

    if curr:
        instructions.append(curr)
    return instructions


def false_square(n: int) -> list[list[bool]]:
    return [[False] * n for _ in range(n)]


@dataclass
class Coordinates:
    row: int
    col: int

    def __hash__(self) -> int:
        return hash((self.row, self.col))

    def __add__(self, other):
        return Coordinates(self.row + other.row, self.col + other.col)


@dataclass
class Position:
    outer: Coordinates
    inner: Coordinates

    def add_inner(self, inner_coords: Coordinates):
        new_face = self.inner + inner_coords
        return Position(outer=self.outer, inner=new_face)


class Board:
    def char_to_obstacle(self, c: str) -> Optional[bool]:
        match c:
            case "#":
                return True
            case ".":
                return False
            case _:
                return None

    def get_start_position(self) -> Position:
        cols_in_first_row = [key.col for key in self.faces.keys() if key.row == 0]
        board_col = min(cols_in_first_row)
        board = Coordinates(0, board_col)
        face = Coordinates(0, 0)
        return Position(outer=board, inner=face)

    def keys_with_row(self, row: int) -> list[Coordinates]:
        return [key for key in self.faces.keys() if key.row == row]

    def keys_with_col(self, col: int) -> list[Coordinates]:
        return [key for key in self.faces.keys() if key.col == col]

    def __init__(self, lines: list[str]):
        num_of_rows = len(lines)
        num_of_cols = max(len(line) for line in lines) - 1
        self.face_side = gcd(num_of_rows, num_of_cols)
        self.faces = defaultdict(lambda: false_square(self.face_side))
        for row, line in enumerate(lines):
            for col, c in enumerate(line[:-1]):
                if obstacle := self.char_to_obstacle(c):
                    face = Coordinates(row // self.face_side, col // self.face_side)
                    if face not in self.faces:
                        self.faces[face] = false_square(self.face_side)
                    self.faces[face][row % self.face_side][col % self.face_side] = (
                        obstacle
                    )


def change_direction(direction: Direction, instruction: DirectionChange) -> Direction:
    new_direction = (direction.value + instruction.value) % 4
    return Direction(new_direction)


def direction_to_move(direction: Direction) -> Coordinates:
    match direction:
        case Direction.LEFT:
            return Coordinates(0, -1)
        case Direction.RIGHT:
            return Coordinates(0, 1)
        case Direction.UP:
            return Coordinates(-1, 0)
        case Direction.DOWN:
            return Coordinates(1, 0)


def correct_position_modulo(position: Position, board_info: Board) -> Position:
    face = position.inner
    outer = position.outer

    if face.row < 0:
        face.row = board_info.face_side - 1
        outer.row = (
            outer.row - 1
            if Coordinates(outer.row - 1, outer.col) in board_info.faces.keys()
            else max(key.row for key in board_info.faces.keys() if key.col == outer.col)
        )
    elif face.row >= board_info.face_side:
        face.row = 0
        outer.row = (
            outer.row + 1
            if Coordinates(outer.row + 1, outer.col) in board_info.faces.keys()
            else min(key.row for key in board_info.faces.keys() if key.col == outer.col)
        )
    elif face.col < 0:
        face.col = board_info.face_side - 1
        outer.col = (
            outer.col - 1
            if Coordinates(outer.row, outer.col - 1) in board_info.faces.keys()
            else max(key.col for key in board_info.faces.keys() if key.row == outer.row)
        )
    elif face.col >= board_info.face_side:
        face.col = 0
        outer.col = (
            outer.col + 1
            if Coordinates(outer.row, outer.col + 1) in board_info.faces.keys()
            else min(key.col for key in board_info.faces.keys() if key.row == outer.row)
        )

    return Position(outer=outer, inner=face)


class PositionCorrector(ABC):
    @abstractmethod
    def correct_position(self, position: Position) -> Position: ...


def move_once(
    position: Position, direction: Direction, corrector: PositionCorrector
) -> Optional[Position]:
    face_change = direction_to_move(direction)
    old_position = copy.deepcopy(position)
    new_position = corrector.correct_position(old_position.add_inner(face_change))

    if corrector.board_info.faces[new_position.outer][new_position.inner.row][
        new_position.inner.col
    ]:
        return None

    return new_position


def move(position, direction, steps, corrector):
    while steps > 0 and (new_position := move_once(position, direction, corrector)):
        steps -= 1
        position = new_position
    return position


def final_password(position: Position, direction: Direction, face_side):
    row = position.outer.row * face_side + position.inner.row
    col = position.outer.col * face_side + position.inner.col
    return 1000 * (row + 1) + 4 * (col + 1) + direction.value


def position_to_side(position: Position, n: int) -> Optional[Direction]:
    if position.inner.row < 0:
        return Direction.UP
    if position.inner.row >= n:
        return Direction.DOWN
    if position.inner.col < 0:
        return Direction.LEFT
    if position.inner.col >= n:
        return Direction.RIGHT

    return None


class FallCorrector:
    def __init__(self, board_info: Board):
        self.n: int = board_info.face_side
        self.board_info = board_info
        self.neighbors: dict[(Coordinates, Direction), (Coordinates, Direction)] = {}
        keys = board_info.faces.keys()

        for face in keys:
            up_row = (
                face.row - 1
                if Coordinates(face.row - 1, face.col) in keys
                else max(key.row for key in keys if face.col == key.col)
            )
            down_row = (
                face.row + 1
                if Coordinates(face.row + 1, face.col) in keys
                else min(key.row for key in keys if face.col == key.col)
            )
            left_col = (
                face.col - 1
                if Coordinates(face.row, face.col - 1) in keys
                else max(key.col for key in keys if face.row == key.row)
            )
            right_col = (
                face.col + 1
                if Coordinates(face.row, face.col + 1) in keys
                else min(key.col for key in keys if face.row == key.row)
            )
            self.neighbors[(face, Direction.LEFT)] = (
                Coordinates(face.row, left_col),
                Direction.RIGHT,
            )
            self.neighbors[(face, Direction.RIGHT)] = (
                Coordinates(face.row, right_col),
                Direction.LEFT,
            )
            self.neighbors[(face, Direction.UP)] = (
                Coordinates(up_row, face.col),
                Direction.DOWN,
            )
            self.neighbors[(face, Direction.DOWN)] = (
                Coordinates(down_row, face.col),
                Direction.UP,
            )

    def correct_position(self, position: Position) -> Position:
        face = position.inner
        direction = position_to_side(position, self.n)

        if face.row < 0:
            face.row = self.n - 1
        elif face.row >= self.n:
            face.row = 0
        elif face.col < 0:
            face.col = self.n - 1
        elif face.col >= self.n:
            face.col = 0

        if direction is not None:
            position.outer = self.neighbors[(position.outer, direction)][0]

        return Position(outer=position.outer, inner=face)


def part1():
    with open("data/day22.txt", "r", encoding="utf-8") as data:
        lines = data.readlines()
        instructions = read_instructions(lines[-1])
        board = Board(lines[:-2])
        position = board.get_start_position()
        direction = Direction.RIGHT
        corrector = FallCorrector(board)

        for instruction in instructions:
            match instruction:
                case DirectionChange():
                    direction = change_direction(direction, instruction)
                case int():
                    position = move(position, direction, instruction, corrector)

        return final_password(position, direction, board.face_side)
