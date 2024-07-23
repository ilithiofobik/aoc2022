def part1():
    with open("data/day1.txt", "r", encoding="utf-8") as data:
        lines = data.readlines()
        curr_sum = 0
        max_sum = 0

        for line in lines:
            if line == "\n":
                max_sum = max(max_sum, curr_sum)
                curr_sum = 0
            else:
                curr_sum += int(line)

        return max_sum


def part2():
    with open("data/day1.txt", "r", encoding="utf-8") as data:
        lines = data.readlines()
        curr_sum = 0
        max_sums = [0, 0, 0]

        for line in lines:
            if line == "\n":
                max_sums[0] = max(max_sums[0], curr_sum)
                max_sums.sort()
                curr_sum = 0
            else:
                curr_sum += int(line)

        return sum(max_sums)
