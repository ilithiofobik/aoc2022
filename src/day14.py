def read_pair(text):
    t = text.strip().split(",")
    x = int(t[0])
    y = int(t[1])
    return (x, y)


def simulate_step1(max_y, rocks):
    xs, ys = 500, 0

    while ys <= max_y:
        if (xs, ys + 1) not in rocks:
            ys += 1

        elif (xs - 1, ys + 1) not in rocks:
            xs -= 1
            ys += 1

        elif (xs + 1, ys + 1) not in rocks:
            xs += 1
            ys += 1

        else:
            return True, xs, ys

    return False, xs, ys


def simulate_sand(max_y, rocks, simulate_step):
    sand_acceptable = True
    count = -1

    while sand_acceptable:
        sand_acceptable, xs, ys = simulate_step(max_y, rocks)
        rocks.add((xs, ys))
        count += 1

    return count


def generate_path(positions, idx):
    x1, y1 = positions[idx]
    x2, y2 = positions[idx + 1]

    x_min = min(x1, x2)
    x_max = max(x1, x2)
    y_min = min(y1, y2)
    y_max = max(y1, y2)

    for x in range(x_min, x_max + 1):
        for y in range(y_min, y_max + 1):
            yield (x, y)


def part1():
    with open("data/day14.txt", "r", encoding="utf-8") as data:
        lines = data.readlines()

        rocks = set()
        max_y = 0

        for line in lines:
            pairs = line.split(" -> ")
            positions = [read_pair(pair) for pair in pairs]
            local_max = max(y for _, y in positions)
            max_y = max(max_y, local_max)
            n = len(positions)

            for i in range(n - 1):
                for x, y in generate_path(positions, i):
                    rocks.add((x, y))

        return simulate_sand(max_y, rocks, simulate_step1)


def simulate_step2(max_y, rocks):
    xs, ys = 500, 0
    moved = False

    while ys <= max_y:
        if (xs, ys + 1) not in rocks:
            ys += 1
            moved = True

        elif (xs - 1, ys + 1) not in rocks:
            xs -= 1
            ys += 1
            moved = True

        elif (xs + 1, ys + 1) not in rocks:
            xs += 1
            ys += 1
            moved = True

        else:
            return moved, xs, ys

    return moved, xs, ys


def part2():
    with open("data/day14.txt", "r", encoding="utf-8") as data:
        lines = data.readlines()

        rocks = set()
        max_y = 0

        for line in lines:
            pairs = line.split(" -> ")
            positions = [read_pair(pair) for pair in pairs]
            local_max = max(y for _, y in positions)
            max_y = max(max_y, local_max)
            n = len(positions)

            for i in range(n - 1):
                for x, y in generate_path(positions, i):
                    rocks.add((x, y))

        return 1 + simulate_sand(max_y, rocks, simulate_step2)
