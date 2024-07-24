from dataclasses import dataclass


@dataclass
class MonkeyValue:
    def __init__(self, value, left, op, right):
        self.value = value
        self.left = left
        self.op = op
        self.right = right


def read_input(lines):
    monkeys = {}

    for line in lines:
        words = line.strip().split()
        key = words[0][:-1]

        if len(words) == 2:
            value = int(words[1])
            monkeys[key] = MonkeyValue(value, None, None, None)
        else:
            left = words[1]
            op = words[2]
            right = words[3]

            monkeys[key] = MonkeyValue(None, left, op, right)

    return monkeys


operations = {
    "+": lambda x, y: x + y,
    "-": lambda x, y: x - y,
    "*": lambda x, y: x * y,
    "/": lambda x, y: x // y,
}


def eval_monkey(monkeys, key):
    monkey = monkeys[key]

    if monkey.value is not None:
        return monkey.value

    left = eval_monkey(monkeys, monkey.left)
    right = eval_monkey(monkeys, monkey.right)
    operation = operations[monkey.op]

    return operation(left, right)


def contains_key(monkeys, start_key, key):
    if start_key == key:
        return True

    if monkeys[start_key].left is None:
        return False

    left_contains = contains_key(monkeys, monkeys[start_key].left, key)
    right_contains = contains_key(monkeys, monkeys[start_key].right, key)

    return left_contains or right_contains


ROOT = "root"
HUMAN = "humn"


def part1():
    with open("data/day21.txt", "r", encoding="utf-8") as data:
        lines = data.readlines()
        monkeys = read_input(lines)
        return eval_monkey(monkeys, ROOT)


def starter_parameters(monkeys):
    left = monkeys[ROOT].left
    right = monkeys[ROOT].right

    if contains_key(monkeys, left, HUMAN):
        return left, eval_monkey(monkeys, right)
    if contains_key(monkeys, right, HUMAN):
        return right, eval_monkey(monkeys, left)

    raise ValueError("No starter parameters found")


reverse_with_right = {
    "+": lambda v, r: v - r,
    "-": lambda v, r: v + r,
    "*": lambda v, r: v // r,
    "/": lambda v, r: v * r,
}

reverse_with_left = {
    "+": lambda l, v: v - l,
    "-": lambda l, v: l - v,
    "*": lambda l, v: v // l,
    "/": lambda l, v: l // v,
}


def find_human(monkeys, key, v):
    if key == HUMAN:
        return v

    left = monkeys[key].left
    right = monkeys[key].right

    if contains_key(monkeys, left, HUMAN):
        r = eval_monkey(monkeys, right)
        reverse_fun = reverse_with_right[monkeys[key].op]
        return find_human(monkeys, left, reverse_fun(v, r))

    if contains_key(monkeys, right, HUMAN):
        l = eval_monkey(monkeys, left)
        reverse_fun = reverse_with_left[monkeys[key].op]
        return find_human(monkeys, right, reverse_fun(l, v))

    raise ValueError("No human found")


def part2():
    with open("data/day21.txt", "r", encoding="utf-8") as data:
        lines = data.readlines()
        monkeys = read_input(lines)
        subtree, value = starter_parameters(monkeys)
        return find_human(monkeys, subtree, value)
