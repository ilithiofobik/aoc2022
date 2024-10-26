from functools import cache

flow_rate: dict[str, int] = {}
neighbors: dict[str, list[str]] = {}


def read_input(lines):
    for line in lines:
        words = line.split()
        valve = words[1]
        flow_rate[valve] = int((words[4]).strip("rate=;"))
        neighbors[valve] = [w.strip(",") for w in words[9:]]


def add_to_opened(pos, opened):
    opened_arr = opened.split(",")
    opened_arr.append(pos)
    return ",".join(sorted(opened_arr))


@cache
def score(pos, time, opened):
    if time == 0:
        return 0

    result = 0

    if flow_rate[pos] > 0 and pos not in opened:
        added_score = flow_rate[pos] * (time - 1)
        visited_score = score(pos, time - 1, add_to_opened(pos, opened))
        result = max(result, added_score + visited_score)
        return result

    moving_score = max(score(n, time - 1, opened) for n in neighbors[pos])

    return max(result, moving_score)


@cache
def score2(humn, eleph, time, opened, elephant):
    if time == 0:
        return 0

    result = 0

    # elephant
    if elephant:
        if flow_rate[eleph] > 0 and eleph not in opened:
            added_score = flow_rate[eleph] * (time - 1)
            visited_score = score2(
                humn, eleph, time - 1, add_to_opened(eleph, opened), False
            )
            result = max(result, added_score + visited_score)
            return result

        moving_score = max(
            score2(humn, n, time - 1, opened, False) for n in neighbors[eleph]
        )

        return max(result, moving_score)

    # human
    humn, eleph = max(humn, eleph), min(humn, eleph)

    if flow_rate[humn] > 0 and humn not in opened:
        added_score = flow_rate[humn] * (time - 1)
        visited_score = score2(humn, eleph, time, add_to_opened(humn, opened), True)
        result = max(result, added_score + visited_score)
        return result

    moving_score = max(score2(n, eleph, time, opened, True) for n in neighbors[humn])

    return max(result, moving_score)


def part1():
    with open("data/day16.txt", "r", encoding="utf-8") as data:
        lines = data.readlines()
        read_input(lines)

        return score("AA", 30, "")


def part2():
    with open("data/day16.txt", "r", encoding="utf-8") as data:
        lines = data.readlines()
        read_input(lines)

        return score2("AA", "AA", 26, "", False)
