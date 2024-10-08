from typing import Union, Optional
from math import gcd
from collections import namedtuple, defaultdict
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


Position = namedtuple("Position", ["board", "face"])


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
        cols_in_first_row = [key[1] for key in self.faces.keys() if key[0] == 0]
        board_col = min(cols_in_first_row)
        return Position(Coordinates(0, board_col), Coordinates(0, 0))

    def __init__(self, lines: list[str]):
        num_of_rows = len(lines)
        num_of_cols = max(len(line) for line in lines) - 1
        self.face_side = gcd(num_of_rows, num_of_cols)
        self.faces = defaultdict(lambda: false_square(self.face_side))
        for row, line in enumerate(lines):
            for col, c in enumerate(line[:-1]):
                if obstacle := self.char_to_obstacle(c):
                    face = (row // self.face_side, col // self.face_side)
                    if face not in self.faces:
                        self.faces[face] = false_square(self.face_side)
                    self.faces[face][row % self.face_side][
                        col % self.face_side
                    ] = obstacle


def change_direction(direction: Direction, instruction: DirectionChange) -> Direction:
    new_direction = (direction.value + instruction.value) % 4
    return Direction(new_direction)


def move_left(position: Position, board: Board):
    face_row, face_col = position.face.row, position.face.col
    board_row, board_col = position.board.row, position.board.col
    new_face_col = face_col - 1 if face_col > 0 else board.face_side - 1

    if face_col == 0:
        if (board_row, board_col - 1) in board.faces.keys():
            new_board_col = board_col - 1
        else:
            new_board_col = max(
                key[1] for key in board.faces.keys() if key[0] == board_row
            )
    else:
        new_board_col = board_col

    if board.faces[(board_row, new_board_col)][face_row][new_face_col]:
        return None
    return Position(
        Coordinates(board_row, new_board_col), Coordinates(face_row, new_face_col)
    )


def move_right(position: Position, board: Board):
    face_row, face_col = position.face.row, position.face.col
    board_row, board_col = position.board.row, position.board.col
    new_face_col = face_col + 1 if face_col < board.face_side - 1 else 0

    if face_col == board.face_side - 1:
        if (board_row, board_col + 1) in board.faces.keys():
            new_board_col = board_col + 1
        else:
            new_board_col = min(
                key[1] for key in board.faces.keys() if key[0] == board_row
            )
    else:
        new_board_col = board_col

    if board.faces[(board_row, new_board_col)][face_row][new_face_col]:
        return None
    return Position(
        Coordinates(board_row, new_board_col), Coordinates(face_row, new_face_col)
    )


def move_up(position: Position, board: Board):
    face_row, face_col = position.face.row, position.face.col
    board_row, board_col = position.board.row, position.board.col
    new_face_row = face_row - 1 if face_row > 0 else board.face_side - 1

    if face_row == 0:
        if (board_row - 1, board_col) in board.faces.keys():
            new_board_row = board_row - 1
        else:
            new_board_row = max(
                key[0] for key in board.faces.keys() if key[1] == board_col
            )
    else:
        new_board_row = board_row

    if board.faces[(new_board_row, board_col)][new_face_row][face_col]:
        return None
    return Position(
        Coordinates(new_board_row, board_col), Coordinates(new_face_row, face_col)
    )


def move_down(position: Position, board: Board):
    face_row, face_col = position.face.row, position.face.col
    board_row, board_col = position.board.row, position.board.col
    new_face_row = face_row + 1 if face_row < board.face_side - 1 else 0

    if face_row == board.face_side - 1:
        if (board_row + 1, board_col) in board.faces.keys():
            new_board_row = board_row + 1
        else:
            new_board_row = min(
                key[0] for key in board.faces.keys() if key[1] == board_col
            )
    else:
        new_board_row = board_row

    if board.faces[(new_board_row, board_col)][new_face_row][face_col]:
        return None
    return Position(
        Coordinates(new_board_row, board_col), Coordinates(new_face_row, face_col)
    )


def move_once(
    position: Position, direction: Direction, board: Board
) -> Optional[Position]:
    match direction:
        case Direction.LEFT:
            return move_left(position, board)
        case Direction.RIGHT:
            return move_right(position, board)
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
