from dataclasses import dataclass
from enum import Enum

Direction = Enum("Direction", ["U", "D", "L", "R"])

direction_to_move = {
    Direction.U: (-1, 0),
    Direction.D: (1, 0),
    Direction.L: (0, -1),
    Direction.R: (0, 1),
}


def add_tuples(t1, t2):
    return tuple(x + y for x, y in zip(t1, t2))


@dataclass
class Blizzard:
    def __init__(self, direction, x, y):
        self.direction = direction
        self.pos = (x, y)


def move(blizzard, mod_x, mod_y):
    diff = direction_to_move[blizzard.direction]
    (new_x, new_y) = add_tuples(blizzard.pos, diff)
    blizzard.pos = (new_x % mod_x, new_y % mod_y)


class Basin:
    def __init__(self, blizzards, mod_x, mod_y):
        self.achievable = {(-1, 0)}
        self.blizzards = blizzards
        self.mod_x = mod_x
        self.mod_y = mod_y
        self.ending = (mod_x, mod_y - 1)

    def neighbors(self, pos):
        x, y = pos

        for dx, dy in [(-1, 0), (1, 0), (0, 0), (0, -1), (0, 1)]:
            new_x = x + dx
            new_y = y + dy

            if new_x < 0 and new_y != 0:
                continue

            if new_x == self.mod_x and new_y != self.mod_y - 1:
                continue

            if new_y < 0 or new_y == self.mod_y:
                continue

            yield (new_x, new_y)

    def perform_blizzard_move(self):
        for blizzard in self.blizzards:
            move(blizzard, self.mod_x, self.mod_y)

    def is_there_a_blizzard(self, pos):
        return any(blizzard.pos == pos for blizzard in self.blizzards)

    def run_simulation(self):
        counter = 0

        while True:
            counter += 1
            new_achievable = set()

            self.perform_blizzard_move()

            for pos in self.achievable:
                for neighbor in self.neighbors(pos):
                    if neighbor == self.ending:
                        return counter
                    if self.is_there_a_blizzard(neighbor):
                        continue
                    new_achievable.add(neighbor)

            self.achievable = new_achievable


def char_to_direction(char):
    match char:
        case "v":
            return Direction.D
        case "^":
            return Direction.U
        case "<":
            return Direction.L
        case ">":
            return Direction.R
        case _:
            return None


def read_input(lines):
    mod_x = len(lines) - 2
    mod_y = len(lines[0].strip()) - 2

    blizzards = []

    for x, line in enumerate(lines[1:]):
        for y, char in enumerate(line[1:].strip()):
            if direction := char_to_direction(char):
                blizzards.append(Blizzard(direction, x, y))

    return blizzards, mod_x, mod_y


def part1():
    with open("data/day24.txt", "r", encoding="utf-8") as data:
        lines = data.readlines()
        blizzards, mod_x, mod_y = read_input(lines)
        basin = Basin(blizzards, mod_x, mod_y)
        return basin.run_simulation()


def part2():
    with open("data/day24.txt", "r", encoding="utf-8") as data:
        lines = data.readlines()
        blizzards, mod_x, mod_y = read_input(lines)
        starting, ending = (-1, 0), (mod_x, mod_y - 1)

        result = 0

        basin = Basin(blizzards, mod_x, mod_y)
        result += basin.run_simulation()

        basin.achievable = {ending}
        basin.ending = starting
        result += basin.run_simulation()

        basin.achievable = {starting}
        basin.ending = ending
        result += basin.run_simulation()

        return result
