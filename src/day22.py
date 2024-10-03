from dataclasses import dataclass
from typing import Literal, Union, Optional
from math import gcd
from collections import namedtuple, defaultdict

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


def false_square(n: int) -> list[list[bool]]:
    return [[False] * n for _ in range(n)]


AltPosition = namedtuple(
    "AltPosition", ["board_row", "board_col", "face_row", "face_col"]
)


class AltBoard:
    def char_to_obstacle(self, c: str) -> Optional[bool]:
        match c:
            case "#":
                return True
            case ".":
                return False
            case _:
                return None

    def get_start_position(self) -> AltPosition:
        cols_in_first_row = [key[1] for key in self.faces.keys() if key[0] == 0]
        board_col = min(cols_in_first_row)
        return AltPosition(0, board_col, 0, 0)

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


def read_board(lines):
    def line_to_ints(line):
        return [char_to_int(c) for c in line[:-1]]

    return list(map(line_to_ints, lines))


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


def alt_move_left(position: AltPosition, board: AltBoard):
    face_row, face_col = position.face_row, position.face_col
    board_row, board_col = position.board_row, position.board_col
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
        return position
    return AltPosition(board_row, new_board_col, face_row, new_face_col)


def alt_move_right(position: AltPosition, board: AltBoard):
    face_row, face_col = position.face_row, position.face_col
    board_row, board_col = position.board_row, position.board_col
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
        return position
    return AltPosition(board_row, new_board_col, face_row, new_face_col)


def alt_move_up(position: AltPosition, board: AltBoard):
    face_row, face_col = position.face_row, position.face_col
    board_row, board_col = position.board_row, position.board_col
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
        return position
    return AltPosition(new_board_row, board_col, new_face_row, face_col)


def alt_move_down(position: AltPosition, board: AltBoard):
    face_row, face_col = position.face_row, position.face_col
    board_row, board_col = position.board_row, position.board_col
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
        return position
    return AltPosition(new_board_row, board_col, new_face_row, face_col)


def alt_move_once(position, direction: Direction, board):
    if direction == "LEFT":
        return alt_move_left(position, board)
    if direction == "RIGHT":
        return alt_move_right(position, board)
    if direction == "UP":
        return alt_move_up(position, board)
    if direction == "DOWN":
        return alt_move_down(position, board)

    raise ValueError("Invalid direction")


def move(position, direction, board, steps):
    for _ in range(steps):
        position = move_once(position, direction, board)

    return position


def alt_move(position: AltBoard, direction, board, steps):
    for _ in range(steps):
        position = alt_move_once(position, direction, board)

    return position


def final_password(position, direction, face_side):
    facing_point = {
        "RIGHT": 0,
        "DOWN": 1,
        "LEFT": 2,
        "UP": 3,
    }
    row = position.board_row * face_side + position.face_row
    col = position.board_col * face_side + position.face_col
    return 1000 * (row + 1) + 4 * (col + 1) + facing_point[direction]


def part1():
    with open("data/day22.txt", "r", encoding="utf-8") as data:
        lines = data.readlines()
        instructions = read_instructions(lines[-1])
        alt_board = AltBoard(lines[:-2])
        print("FAces:", len(alt_board.faces))
        alt_position = alt_board.get_start_position()
        board = Board(lines[:-2])

        position = 0, board.row_mins[0]
        direction = "RIGHT"

        for instruction in instructions:
            if isinstance(instruction, int):
                position = move(position, direction, board, instruction)
                alt_position = alt_move(alt_position, direction, alt_board, instruction)
            else:
                direction = change_direction(direction, instruction)

        return final_password(alt_position, direction, alt_board.face_side)
