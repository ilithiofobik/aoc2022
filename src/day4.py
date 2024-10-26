from typing import Callable


class Pair:
    def __init__(self, line: str):
        def pair_to_range(pair: str) -> tuple[int, int]:
            span = pair.split("-")
            first, last = span[0], span[1]
            return (int(first), int(last))

        splitted = line.split(",")
        self.first = pair_to_range(splitted[0])
        self.second = pair_to_range(splitted[1])

    def either_is_contained(self) -> bool:
        def is_contained(inner, outer) -> bool:
            inn_first, inn_last = inner
            out_first, out_last = outer
            return out_first <= inn_first and inn_last <= out_last

        return is_contained(self.first, self.second) or is_contained(
            self.second, self.first
        )

    def are_overlapping(self) -> bool:
        x_first, x_last = self.first
        y_first, y_last = self.second
        return not (x_last < y_first or y_last < x_first)


def _general_solution(condition: Callable[[Pair], bool]) -> int:
    with open("data/day4.txt", "r", encoding="utf-8") as data:
        lines = data.readlines()
        pairs = [Pair(line) for line in lines]
        return sum(1 for p in pairs if condition(p))


def part1() -> int:
    return _general_solution(Pair.either_is_contained)


def part2() -> int:
    return _general_solution(Pair.are_overlapping)
