import itertools
import copy
from enum import Enum


class State(Enum, str):
    AIR = "."
    SAND = "@"
    ROCK = "#"


MINUS = [
    [State.AIR, State.AIR, State.SAND, State.SAND, State.SAND, State.SAND, State.AIR]
]

PLUS = [
    [State.AIR, State.AIR, State.AIR, State.SAND, State.AIR, State.AIR, State.AIR],
    [State.AIR, State.AIR, State.SAND, State.SAND, State.SAND, State.AIR, State.AIR],
    [State.AIR, State.AIR, State.AIR, State.SAND, State.AIR, State.AIR, State.AIR],
]

LSHAPE = [
    [State.AIR, State.AIR, State.SAND, State.SAND, State.SAND, State.AIR, State.AIR],
    [State.AIR, State.AIR, State.AIR, State.AIR, State.SAND, State.AIR, State.AIR],
    [State.AIR, State.AIR, State.AIR, State.AIR, State.SAND, State.AIR, State.AIR],
]

ISHAPE = [
    [State.AIR, State.AIR, State.SAND, State.AIR, State.AIR, State.AIR, State.AIR],
    [State.AIR, State.AIR, State.SAND, State.AIR, State.AIR, State.AIR, State.AIR],
    [State.AIR, State.AIR, State.SAND, State.AIR, State.AIR, State.AIR, State.AIR],
    [State.AIR, State.AIR, State.SAND, State.AIR, State.AIR, State.AIR, State.AIR],
]

SQUARE = [
    [State.AIR, State.AIR, State.SAND, State.SAND, State.AIR, State.AIR, State.AIR],
    [State.AIR, State.AIR, State.SAND, State.SAND, State.AIR, State.AIR, State.AIR],
]

SHAPES = [MINUS, PLUS, LSHAPE, ISHAPE, SQUARE]

FLOOR = [State.ROCK] * 7
EMPTY = [State.AIR] * 7


def fill_up_with_air(board):
    for _ in range(3):
        board.append(copy.deepcopy(EMPTY))


def get_shape(i):
    return copy.deepcopy(SHAPES[i % len(SHAPES)])


def put_shape(board, shape):
    lowest = len(board)
    board.extend(shape)
    highest = len(board) - 1

    return lowest, highest


def part1():
    with open("data/day17.txt", "r", encoding="utf-8") as data:
        line = data.readline()
        jets = itertools.cycle(list(line.strip()))
        board = [FLOOR]

        for i in range(2022):
            fill_up_with_air(board)
            shape = get_shape(i)
            lowest, highest = put_shape(board, shape)

        return 0
