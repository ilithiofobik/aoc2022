def char_to_idx(c):
    if ord('a') <= ord(c):
        return ord(c) - ord('a')
    return ord(c) - ord('A') + 26

def line_to_points(line):
    length = len(line)
    half = length // 2
    used = [False] * 52

    for i in range(half):
        idx = char_to_idx(line[i])
        used[idx] = True

    for i in range(half, length):
        idx = char_to_idx(line[i])
        if used[idx]:
            return idx + 1

    return 0

def part1():
    with open("data/day3.txt", "r", encoding="utf-8") as data:
        lines = data.readlines()
        return sum(line_to_points(l) for l in lines)

def part2():
    with open("data/day3.txt", "r", encoding="utf-8") as data:
        lines = data.readlines()
        length = len(lines)
        result = 0

        for i in range(0, length, 3):
            symbols = [set((lines[j]).strip()) for j in range(i, i + 3)]

            final = (symbols[0].intersection(symbols[1])).intersection(symbols[2])

            for c in final:
                result += char_to_idx(c) + 1

        return result
