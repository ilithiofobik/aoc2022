def pair_to_range(pair):
    span = pair.split("-")
    first, last = span[0], span[1]
    return (int(first), int(last))

def to_pairs(line):
    pairs = line.split(",")
    first, second = pairs[0], pairs[1]
    return (pair_to_range(first), pair_to_range(second))

def is_contained(inner, outer):
    inn_first, inn_last = inner
    out_first, out_last = outer
    return out_first <= inn_first and inn_last <= out_last

def either_is_contained(pair):
    first, second = pair
    return is_contained(first, second) or is_contained(second, first)

def part1():
    with open("data/day4.txt", "r", encoding="utf-8") as data:
        lines = data.readlines()
        pairs = [to_pairs(l) for l in lines]
        contained = [ p for p in pairs if either_is_contained(p)]
        return len(contained)

def are_overlapping(pair):
    x, y = pair
    x_first, x_last = x
    y_first, y_last = y
    return not (x_last < y_first or y_last < x_first)

def part2():
    with open("data/day4.txt", "r", encoding="utf-8") as data:
        lines = data.readlines()
        pairs = [to_pairs(l) for l in lines]
        contained = [ p for p in pairs if are_overlapping(p)]
        return len(contained)
