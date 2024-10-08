from typing import Union, Optional
from math import gcd
from collections import defaultdict
from enum import IntEnum
from dataclasses import dataclass


class DirectionChange(IntEnum):
    L = 3
    R = 1


class Direction(IntEnum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3


Instruction = Union[int, DirectionChange]


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

    def add_modulo(self, other, n):
        return Coordinates((self.row + other.row) % n, (self.col + other.col) % n)


@dataclass
class Position:
    board: Coordinates
    face: Coordinates


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
        return Position(board=board, face=face)

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
                    self.faces[face][row % self.face_side][
                        col % self.face_side
                    ] = obstacle


def change_direction(direction: Direction, instruction: DirectionChange) -> Direction:
    new_direction = (direction.value + instruction.value) % 4
    return Direction(new_direction)


def move_left(position: Position, board: Board, face_change: Coordinates):
    new_face = position.face.add_modulo(face_change, board.face_side)
    new_board = position.board
    attrs_pairs = [("col", "row")]

    for attr1, attr2 in attrs_pairs:
        if (
            getattr(new_face, attr1) == board.face_side - 1
            and getattr(face_change, attr1) == -1
        ):
            if (
                Coordinates(
                    getattr(position.board, attr2), getattr(position.board, attr1) - 1
                )
                in board.faces.keys()
            ):
                setattr(new_board, attr1, getattr(position.board, attr1) - 1)
            else:
                setattr(
                    new_board,
                    attr1,
                    max(
                        getattr(key, attr1)
                        for key in board.faces.keys()
                        if getattr(key, attr2) == getattr(position.board, attr2)
                    ),
                )
        elif getattr(new_face, attr1) == 0 and getattr(face_change, attr1) == 1:
            if (
                Coordinates(
                    getattr(position.board, attr2), getattr(position.board, attr1) + 1
                )
                in board.faces.keys()
            ):
                setattr(new_board, attr1, getattr(position.board, attr1) + 1)
            else:
                setattr(
                    new_board,
                    attr1,
                    min(
                        getattr(key, attr1)
                        for key in board.faces.keys()
                        if getattr(key, attr2) == getattr(position.board, attr2)
                    ),
                )

    if board.faces[new_board][new_face.row][new_face.col]:
        return None

    board = Coordinates(new_board.row, new_board.col)
    return Position(board=board, face=new_face)


def move_up(position: Position, board: Board):
    face_row, face_col = position.face.row, position.face.col
    board_row, board_col = position.board.row, position.board.col
    new_face_row = face_row - 1 if face_row > 0 else board.face_side - 1

    if face_row == 0:
        if Coordinates(board_row - 1, board_col) in board.faces.keys():
            new_board_row = board_row - 1
        else:
            new_board_row = max(
                key.row for key in board.faces.keys() if key.col == board_col
            )
    else:
        new_board_row = board_row

    if board.faces[Coordinates(new_board_row, board_col)][new_face_row][face_col]:
        return None

    board = Coordinates(new_board_row, board_col)
    face = Coordinates(new_face_row, face_col)
    return Position(board=board, face=face)


def move_down(position: Position, board: Board):
    face_row, face_col = position.face.row, position.face.col
    board_row, board_col = position.board.row, position.board.col
    new_face_row = face_row + 1 if face_row < board.face_side - 1 else 0

    if face_row == board.face_side - 1:
        if Coordinates(board_row + 1, board_col) in board.faces.keys():
            new_board_row = board_row + 1
        else:
            new_board_row = min(
                key.row for key in board.faces.keys() if key.col == board_col
            )
    else:
        new_board_row = board_row

    if board.faces[Coordinates(new_board_row, board_col)][new_face_row][face_col]:
        return None

    board = Coordinates(new_board_row, board_col)
    face = Coordinates(new_face_row, face_col)
    return Position(board=board, face=face)


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


def move_once(
    position: Position, direction: Direction, board: Board
) -> Optional[Position]:
    face_change = direction_to_move(direction)

    match direction:
        case Direction.LEFT:
            return move_left(position, board, face_change)
        case Direction.RIGHT:
            return move_left(position, board, face_change)
        case Direction.UP:
            return move_up(position, board)
        case Direction.DOWN:
            return move_down(position, board)


def move(position, direction, board, steps):
    if steps > 0 and (new_position := move_once(position, direction, board)):
        return move(new_position, direction, board, steps - 1)
    return position


def final_password(position: Position, direction: Direction, face_side):
    row = position.board.row * face_side + position.face.row
    col = position.board.col * face_side + position.face.col
    return 1000 * (row + 1) + 4 * (col + 1) + direction.value


def part1():
    with open("data/day22.txt", "r", encoding="utf-8") as data:
        lines = data.readlines()
        instructions = read_instructions(lines[-1])
        board = Board(lines[:-2])
        position = board.get_start_position()
        direction = Direction.RIGHT

        for instruction in instructions:
            match instruction:
                case DirectionChange():
                    direction = change_direction(direction, instruction)
                case int():
                    position = move(position, direction, board, instruction)

        return final_password(position, direction, board.face_side)
