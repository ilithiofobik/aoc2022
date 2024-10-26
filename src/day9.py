from typing import Set, Tuple


def max_dist(x0: int, y0: int, x1: int, y1: int) -> int:
    return max(abs(x1 - x0), abs(y1 - y0))


def move(x: int, y: int, direction: str) -> Tuple[int, int]:
    if direction == "U":
        return x, y + 1
    if direction == "D":
        return x, y - 1
    if direction == "L":
        return x - 1, y
    if direction == "R":
        return x + 1, y
    raise ValueError("Invalid direction")


def move_tail(h_x: int, h_y: int, t_x: int, t_y: int) -> Tuple[int, int]:
    if abs(h_x - t_x) <= 1:
        t_x = h_x
    else:
        t_x = (t_x + h_x) // 2

    if abs(h_y - t_y) <= 1:
        t_y = h_y
    else:
        t_y = (t_y + h_y) // 2

    return t_x, t_y


def part1() -> int:
    with open("data/day9.txt", "r", encoding="utf-8") as data:
        h_x, h_y = 0, 0
        t_x, t_y = 0, 0
        visited: Set[Tuple[int, int]] = {(0, 0)}

        lines = data.readlines()
        for line in lines:
            words = line.split()
            direction = words[0]
            distance = int(words[1])

            for _ in range(distance):
                h_x, h_y = move(h_x, h_y, direction)
                if max_dist(h_x, h_y, t_x, t_y) >= 2:
                    t_x, t_y = move_tail(h_x, h_y, t_x, t_y)
                visited.add((t_x, t_y))

        return len(visited)


K = 10


def part2() -> int:
    with open("data/day9.txt", "r", encoding="utf-8") as data:
        x = [0] * K
        y = [0] * K
        visited: Set[Tuple[int, int]] = {(0, 0)}

        lines = data.readlines()
        for line in lines:
            words = line.split()
            direction = words[0]
            distance = int(words[1])

            for _ in range(distance):
                x[0], y[0] = move(x[0], y[0], direction)

                for i in range(K - 1):
                    if max_dist(x[i], y[i], x[i + 1], y[i + 1]) >= 2:
                        x[i + 1], y[i + 1] = move_tail(x[i], y[i], x[i + 1], y[i + 1])
                    else:
                        break

                visited.add((x[K - 1], y[K - 1]))

        return len(visited)
