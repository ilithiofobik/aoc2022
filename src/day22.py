from enum import Enum
from dataclasses import dataclass
from typing import Literal, Union
from math import gcd


DirectionChange = Literal["L", "R"]
Direction = Literal["LEFT", "RIGHT", "UP", "DOWN"]
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
            instructions.append(c)

    if curr:
        instructions.append(curr)
    return instructions


def char_to_int(c: str) -> int:
    match c:
        case "#":
            return 1
        case ".":
            return 2
        case _:
            return 0


def read_board(lines):
    board = []

    for line in lines:
        row = [char_to_int(c) for c in line[:-1]]
        board.append(row)

    return board


def row_to_min_max(row):
    idxs = [i for i, x in enumerate(row) if x != 0]
    return min(idxs), max(idxs)


def cols_min_maxes(row_mins, row_maxs):
    num_of_cols = max(row_maxs)
    num_of_rows = len(row_mins)

    col_mins = []
    col_maxs = []

    for c in range(num_of_cols):
        col_min = min(i for i in range(num_of_rows) if row_mins[i] <= c <= row_maxs[i])
        col_max = max(i for i in range(num_of_rows) if row_mins[i] <= c <= row_maxs[i])
        col_mins.append(col_min)
        col_maxs.append(col_max)

    return col_mins, col_maxs


def mins_maxs(board):
    row_mins = []
    row_maxs = []

    for row in board:
        min_r, max_r = row_to_min_max(row)
        row_mins.append(min_r)
        row_maxs.append(max_r)

    col_mins, col_maxs = cols_min_maxes(row_mins, row_maxs)

    return row_mins, row_maxs, col_mins, col_maxs


@dataclass
class Board:
    def __init__(self, lines):
        self.board = read_board(lines)
        self.row_mins, self.row_maxs, self.col_mins, self.col_maxs = mins_maxs(
            self.board
        )


def change_direction(direction: Direction, instruction) -> Direction:
    match (direction, instruction):
        case ("LEFT", "L") | ("RIGHT", "R"):
            return "DOWN"
        case ("LEFT", "R") | ("RIGHT", "L"):
            return "UP"
        case ("UP", "R") | ("DOWN", "L"):
            return "RIGHT"
        case ("DOWN", "R") | ("UP", "L"):
            return "LEFT"


def move_left(position, board):
    row, col = position
    l_col = col - 1 if col > board.row_mins[row] else board.row_maxs[row]
    new_col = l_col if board.board[row][l_col] == 2 else col
    return (row, new_col)


def move_right(position, board):
    row, col = position
    r_col = col + 1 if col < board.row_maxs[row] else board.row_mins[row]
    new_col = r_col if board.board[row][r_col] == 2 else col
    return (row, new_col)


def move_up(position, board):
    row, col = position
    u_row = row - 1 if row > board.col_mins[col] else board.col_maxs[col]
    new_row = u_row if board.board[u_row][col] == 2 else row
    return (new_row, col)


def move_down(position, board):
    row, col = position
    d_row = row + 1 if row < board.col_maxs[col] else board.col_mins[col]
    new_row = d_row if board.board[d_row][col] == 2 else row
    return (new_row, col)


pos_diff = {
    "LEFT": (0, -1),
    "RIGHT": (0, 1),
    "UP": (-1, 0),
    "DOWN": (1, 0),
}


def add_vectors(v1, v2):
    v11, v12 = v1
    v21, v22 = v2
    return (v11 + v21, v12 + v22)


def correct_position(position, board):
    row, col = position

    if row < len(board.row_mins):
        k = board.row_mins[row]
        n = board.row_maxs[row] - k + 1
        col = (col - k) % n + k

    if col < len(board.col_mins):
        k = board.col_mins[col]
        n = board.col_maxs[col] - k + 1
        row = (row - k) % n + k

    return row, col


def move_once(position, direction: Direction, board):
    if direction == "LEFT":
        return move_left(position, board)
    if direction == "RIGHT":
        return move_right(position, board)
    if direction == "UP":
        return move_up(position, board)
    if direction == "DOWN":
        return move_down(position, board)

    raise ValueError("Invalid direction")


def move(position, direction, board, steps):
    for _ in range(steps):
        position = move_once(position, direction, board)

    return position


def part1():
    with open("data/day22.txt", "r", encoding="utf-8") as data:
        lines = data.readlines()
        instructions = read_instructions(lines[-1])
        board = Board(lines[:-2])

        position = 0, board.row_mins[0]
        direction = "RIGHT"

        for instruction in instructions:
            if isinstance(instruction, int):
                position = move(position, direction, board, instruction)
            else:
                direction = change_direction(direction, instruction)

        row, col = position
        facing_point = {
            "RIGHT": 0,
            "DOWN": 1,
            "LEFT": 2,
            "UP": 3,
        }

        return 1000 * (row + 1) + 4 * (col + 1) + facing_point[direction]
