import itertools


def _general_solution(n: int) -> int:
    with open("data/day1.txt", "r", encoding="utf-8") as data:
        words = [line.strip() for line in data.readlines()]
        splitted = [list(group) for k, group in itertools.groupby(words, bool) if k]
        sums = [sum(map(int, group)) for group in splitted]
        return sum(sorted(sums, reverse=True)[:n])


def part1() -> int:
    return _general_solution(1)


def part2() -> int:
    return _general_solution(3)
