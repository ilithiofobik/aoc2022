from enum import Enum

Cardinal = Enum("Cardinal", ["NORTH", "EAST", "SOUTH", "WEST"])

neighbors = {
    Cardinal.NORTH: [(-1, -1), (-1, 0), (-1, 1)],
    Cardinal.EAST: [(-1, 1), (0, 1), (1, 1)],
    Cardinal.SOUTH: [(1, -1), (1, 0), (1, 1)],
    Cardinal.WEST: [(-1, -1), (0, -1), (1, -1)],
}

moves = {
    Cardinal.NORTH: (-1, 0),
    Cardinal.EAST: (0, 1),
    Cardinal.SOUTH: (1, 0),
    Cardinal.WEST: (0, -1),
}


def add_tuples(t1, t2):
    return tuple(x + y for x, y in zip(t1, t2))


class Elf:
    def __init__(self, x, y):
        self.pos = (x, y)
        self.orders = [Cardinal.NORTH, Cardinal.SOUTH, Cardinal.WEST, Cardinal.EAST]
        self.new_order = None
        self.new_pos = None

    def is_order_legal(self, board, order):
        return all(add_tuples(self.pos, move) not in board for move in neighbors[order])

    def find_move(self, board):
        legal_orders = [
            order for order in self.orders if self.is_order_legal(board, order)
        ]

        if len(legal_orders) in [0, 4]:
            return

        self.new_order = legal_orders[0]
        new_move = moves[self.new_order]
        self.new_pos = add_tuples(self.pos, new_move)

        return

    def reset_new_move(self):
        self.new_pos = None
        self.new_order = None

    def perform_move(self, new_pos):
        self.pos = new_pos

    def rotate_orders(self):
        order = self.orders[0]
        self.orders = [x for x in self.orders if x != order] + [order]


def one_round(elves):
    board = board_from_elves(elves)
    counters = {}
    moved = False

    for elf in elves:
        elf.find_move(board)

        if new_pos := elf.new_pos:
            counters[new_pos] = counters.get(new_pos, 0) + 1

    for elf in elves:
        if new_pos := elf.new_pos:
            if counters[new_pos] == 1:
                elf.perform_move(new_pos)
                moved = True
        elf.reset_new_move()
        elf.rotate_orders()

    return moved


def board_from_elves(elves):
    return set(elf.pos for elf in elves)


def find_empty_spaces(elves):
    board = board_from_elves(elves)

    max_x = max(x for x, _ in board)
    max_y = max(y for _, y in board)
    min_x = min(x for x, _ in board)
    min_y = min(y for _, y in board)

    return (max_x - min_x + 1) * (max_y - min_y + 1) - len(board)


ROUNDS = 10


def read_elves(lines):
    elves = []

    for x, line in enumerate(lines):
        for y, char in enumerate(line):
            if char == "#":
                elves.append(Elf(x, y))

    return elves


def part1():
    with open("data/day23.txt", "r", encoding="utf-8") as data:
        lines = data.readlines()
        elves = read_elves(lines)

        for _ in range(ROUNDS):
            one_round(elves)

        return find_empty_spaces(elves)


def part2():
    with open("data/day23.txt", "r", encoding="utf-8") as data:
        lines = data.readlines()
        elves = read_elves(lines)

        counter = 1

        while one_round(elves):
            counter += 1

        return counter
