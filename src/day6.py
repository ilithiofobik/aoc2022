def _all_different(string: str) -> bool:
    length = len(string)
    return all(
        string[i] != string[j] for i in range(length) for j in range(i + 1, length)
    )


def _general_solution(pattern_len):
    with open("data/day6.txt", "r", encoding="utf-8") as data:
        text = data.read()
        length = len(text)

        for i in range(length - pattern_len):
            if _all_different(text[i : i + pattern_len]):
                return i + pattern_len

        raise ValueError("No solution found")


def part1():
    return _general_solution(4)


def part2():
    return _general_solution(14)
