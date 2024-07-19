def update_result(result, cycle, x, idxs):
    cycle += 1
    if cycle in idxs:
        result += cycle * x
    return cycle, result


def part1():
    with open("data/day10.txt", "r", encoding="utf-8") as data:
        x = 1
        cycle = 1
        idxs = list(i for i in range(20, 221, 40))
        result = 0

        for line in data.readlines():
            words = line.split()

            if words[0] == "noop":
                cycle, result = update_result(result, cycle, x, idxs)
            else:
                cycle, result = update_result(result, cycle, x, idxs)
                x += int(words[1])
                cycle, result = update_result(result, cycle, x, idxs)

        return result


def part2():
    with open("data/day10.txt", "r", encoding="utf-8") as data:
        x = 1
        x_arr = [1]
        cycle = 1
        result = 0

        for line in data.readlines():
            words = line.split()

            if words[0] == "noop":
                cycle += 1
                x_arr.append(x)
            else:
                cycle += 1
                x_arr.append(x)
                x += int(words[1])
                cycle += 1
                x_arr.append(x)

        rows = 6
        cols = 40
        result = ""

        for row in range(rows):
            for col in range(cols):
                x = x_arr[row * cols + col]
                c = "#" if abs(x - col) <= 1 else "."
                result += c
            result += "\n"

        return result
