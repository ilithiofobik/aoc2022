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


class PositionCorrector(ABC):
    @abstractmethod
    def correct_position(self, position: Position) -> tuple[Position, Direction]: ...

    @abstractmethod
    def is_position_blocked(self, position: Position) -> bool: ...


def move_once(
    position: Position, direction: Direction, corrector: PositionCorrector
) -> Optional[Position]:
    face_change = direction_to_move(direction)
    new_position, new_direction = corrector.correct_position(
        position.add_inner(face_change), direction
    )

    if corrector.is_position_blocked(new_position):
        return None

    return new_position, new_direction


def move(position, direction, steps, corrector):
    while steps > 0 and (new_data := move_once(position, direction, corrector)):
        steps -= 1
        (new_position, new_direction) = new_data
        position = new_position
        direction = new_direction
    return position, direction


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


def calculate_new_inner_position(
    position: Position, old_side: Direction, new_side: Direction, n: int
) -> Coordinates:
    match old_side, new_side:
        case Direction.LEFT, Direction.RIGHT:
            return Coordinates(position.inner.row, n - 1)
        case Direction.RIGHT, Direction.LEFT:
            return Coordinates(position.inner.row, 0)
        case Direction.UP, Direction.DOWN:
            return Coordinates(n - 1, position.inner.col)
        case Direction.DOWN, Direction.UP:
            return Coordinates(0, position.inner.col)
        case a, b:
            raise ValueError(f"Invalid sides: {a}, {b}")


class FallCorrector:
    def __init__(self, board_info: Board):
        self.n: int = board_info.face_side
        self._board_info = board_info
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

    def is_position_blocked(self, pos: Position) -> bool:
        return self._board_info.faces[pos.outer][pos.inner.row][pos.inner.col]

    def correct_position(
        self, position: Position, direction: Direction
    ) -> tuple[Position, Direction]:
        old_side = position_to_side(position, self.n)

        if old_side is not None:
            new_outer, new_side = self.neighbors[(position.outer, old_side)]
            new_inner = calculate_new_inner_position(
                position, old_side, new_side, self.n
            )
            return Position(outer=new_outer, inner=new_inner), direction

        return position, direction


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
                    position, direction = move(
                        position, direction, instruction, corrector
                    )

        return final_password(position, direction, board.face_side)


class CubeCorrector:
    def __init__(self, board_info: Board):
        self.n: int = board_info.face_side
        self._board_info = board_info

    def is_position_blocked(self, pos: Position) -> bool:
        return self._board_info.faces[pos.outer][pos.inner.row][pos.inner.col]

    def correct_position(
        self, position: Position, direction: Direction
    ) -> tuple[Position, Direction]:
        old_side = position_to_side(position, self.n)

        if old_side is not None:
            match position.outer, old_side:
                case Coordinates(0, 1), Direction.RIGHT:
                    return Position(
                        outer=Coordinates(0, 2),
                        inner=Coordinates(position.inner.row, 0),
                    ), Direction.RIGHT
                case Coordinates(0, 2), Direction.LEFT:
                    return Position(
                        outer=Coordinates(0, 1),
                        inner=Coordinates(position.inner.row, self.n - 1),
                    ), Direction.LEFT
                case Coordinates(0, 1), Direction.DOWN:
                    return Position(
                        outer=Coordinates(1, 1),
                        inner=Coordinates(0, position.inner.col),
                    ), Direction.DOWN
                case Coordinates(1, 1), Direction.UP:
                    return Position(
                        outer=Coordinates(0, 1),
                        inner=Coordinates(self.n - 1, position.inner.col),
                    ), Direction.UP
                case Coordinates(0, 1), Direction.LEFT:
                    return Position(
                        outer=Coordinates(2, 0),
                        inner=Coordinates(self.n - 1 - position.inner.row, 0),
                    ), Direction.RIGHT
                case Coordinates(2, 0), Direction.LEFT:
                    return Position(
                        outer=Coordinates(0, 1),
                        inner=Coordinates(self.n - 1 - position.inner.row, 0),
                    ), Direction.RIGHT
                case Coordinates(0, 1), Direction.UP:
                    return Position(
                        outer=Coordinates(3, 0),
                        inner=Coordinates(position.inner.col, 0),
                    ), Direction.RIGHT
                case Coordinates(3, 0), Direction.LEFT:
                    return Position(
                        outer=Coordinates(0, 1),
                        inner=Coordinates(0, position.inner.row),
                    ), Direction.DOWN
                case Coordinates(0, 2), Direction.DOWN:
                    return Position(
                        outer=Coordinates(1, 1),
                        inner=Coordinates(position.inner.col, self.n - 1),
                    ), Direction.LEFT
                case Coordinates(1, 1), Direction.RIGHT:
                    return Position(
                        outer=Coordinates(0, 2),
                        inner=Coordinates(self.n - 1, position.inner.row),
                    ), Direction.UP
                case Coordinates(0, 2), Direction.RIGHT:
                    return Position(
                        outer=Coordinates(2, 1),
                        inner=Coordinates(self.n - 1 - position.inner.row, self.n - 1),
                    ), Direction.LEFT
                case Coordinates(2, 1), Direction.RIGHT:
                    return Position(
                        outer=Coordinates(0, 2),
                        inner=Coordinates(self.n - 1 - position.inner.row, self.n - 1),
                    ), Direction.LEFT
                case Coordinates(0, 2), Direction.UP:
                    return Position(
                        outer=Coordinates(3, 0),
                        inner=Coordinates(self.n - 1, position.inner.col),
                    ), Direction.UP
                case Coordinates(3, 0), Direction.DOWN:
                    return Position(
                        outer=Coordinates(0, 2),
                        inner=Coordinates(0, position.inner.col),
                    ), Direction.DOWN
                case Coordinates(1, 1), Direction.DOWN:
                    return Position(
                        outer=Coordinates(2, 1),
                        inner=Coordinates(0, position.inner.col),
                    ), Direction.DOWN
                case Coordinates(2, 1), Direction.UP:
                    return Position(
                        outer=Coordinates(1, 1),
                        inner=Coordinates(self.n - 1, position.inner.col),
                    ), Direction.UP
                case Coordinates(1, 1), Direction.LEFT:
                    return Position(
                        outer=Coordinates(2, 0),
                        inner=Coordinates(0, position.inner.row),
                    ), Direction.DOWN
                case Coordinates(2, 0), Direction.UP:
                    return Position(
                        outer=Coordinates(1, 1),
                        inner=Coordinates(position.inner.col, 0),
                    ), Direction.RIGHT
                case Coordinates(2, 1), Direction.DOWN:
                    return Position(
                        outer=Coordinates(3, 0),
                        inner=Coordinates(position.inner.col, self.n - 1),
                    ), Direction.LEFT
                case Coordinates(3, 0), Direction.RIGHT:
                    return Position(
                        outer=Coordinates(2, 1),
                        inner=Coordinates(self.n - 1, position.inner.row),
                    ), Direction.UP
                case Coordinates(2, 1), Direction.LEFT:
                    return Position(
                        outer=Coordinates(2, 0),
                        inner=Coordinates(position.inner.row, self.n - 1),
                    ), Direction.LEFT
                case Coordinates(2, 0), Direction.RIGHT:
                    return Position(
                        outer=Coordinates(2, 1),
                        inner=Coordinates(position.inner.row, 0),
                    ), Direction.RIGHT
                case Coordinates(2, 0), Direction.DOWN:
                    return Position(
                        outer=Coordinates(3, 0),
                        inner=Coordinates(0, position.inner.col),
                    ), Direction.DOWN
                case Coordinates(3, 0), Direction.UP:
                    return Position(
                        outer=Coordinates(2, 0),
                        inner=Coordinates(self.n - 1, position.inner.col),
                    ), Direction.UP
                case a, b:
                    raise ValueError(f"Invalid outer: {a}, {b}")

        return position, direction


def part2():
    with open("data/day22.txt", "r", encoding="utf-8") as data:
        lines = data.readlines()
        instructions = read_instructions(lines[-1])
        board = Board(lines[:-2])
        position = board.get_start_position()
        direction = Direction.RIGHT
        corrector = CubeCorrector(board)

        for instruction in instructions:
            match instruction:
                case DirectionChange():
                    direction = change_direction(direction, instruction)
                case int():
                    position, direction = move(
                        position, direction, instruction, corrector
                    )

        return final_password(position, direction, board.face_side)
