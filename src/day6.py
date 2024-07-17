def all_different(string):
    length = len(string)
    for i in range(length):
        for j in range(i + 1, length):
            if string[i] == string[j]:
                return False
    return True

def general_solution(pattern_len):
    with open("data/day6.txt", "r", encoding="utf-8") as data:
        text = data.read()
        length = len(text)

        for i in range(length - pattern_len):
            if all_different(text[i:i + pattern_len]):
                return i + pattern_len

        raise Exception("No solution found")

def part1():
    return general_solution(4)

def part2():
    return general_solution(14)
