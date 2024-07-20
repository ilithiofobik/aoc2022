import dataclasses
from math import prod


@dataclasses.dataclass
class ThrowTest:
    number: int
    t_throw: int
    f_throw: int


class Monkey:
    def __init__(self, starting_tems, operation, throw_test):
        self.__items = starting_tems
        self.__operation = operation
        self.__throw_test = throw_test
        self.__inspected_items = 0

    def test_number(self):
        return self.__throw_test.number

    def inspected(self):
        return self.__inspected_items

    def append_item(self, item):
        self.__items.append(item)

    def throw_test(self, worry_level):
        if worry_level % self.__throw_test.number == 0:
            return self.__throw_test.t_throw

        return self.__throw_test.f_throw

    def do_turn(self, second_op):
        result = []

        for item in self.__items:
            worry_level = self.__operation(item)
            worry_level = second_op(worry_level)
            new_monkey = self.throw_test(worry_level)
            result.append((new_monkey, worry_level))
            self.__inspected_items += 1

        self.__items = []

        return result


def read_starting_items(line):
    parts = line.split(":")
    numbers = parts[1].split(",")
    return [int(num.strip()) for num in numbers]


def read_operation(line):
    parts = line.split()
    op = parts[-2]

    if parts[-1].isdigit():
        num = int(parts[-1])

        if op == "+":
            return lambda x: x + num

        return lambda x: x * num

    return lambda x: x**2


def read_throw_test(lines):
    num = int(lines[0].split()[-1])
    t_throw = int(lines[1].split()[-1])
    f_throw = int(lines[2].split()[-1])

    return ThrowTest(num, t_throw, f_throw)


def read_monkeys(lines):
    num_of_monkeys = (len(lines) + 1) // 7
    monkeys = []

    for i in range(num_of_monkeys):
        starting_items = read_starting_items(lines[i * 7 + 1])
        operation = read_operation(lines[i * 7 + 2])
        throw_test = read_throw_test(lines[i * 7 + 3 : i * 7 + 6])
        monkey = Monkey(starting_items, operation, throw_test)
        monkeys.append(monkey)

    return monkeys


def monkey_business(monkeys):
    max_inspected = 0
    second_max_inspected = 0

    for monkey in monkeys:
        inspected = monkey.inspected()

        if inspected > second_max_inspected:
            second_max_inspected = inspected

            if second_max_inspected > max_inspected:
                max_inspected, second_max_inspected = (
                    second_max_inspected,
                    max_inspected,
                )

    return max_inspected * second_max_inspected


ROUNDS1 = 20


def part1():
    with open("data/day11.txt", "r", encoding="utf-8") as data:
        lines = data.readlines()
        monkeys = read_monkeys(lines)

        for _ in range(ROUNDS1):
            for monkey in monkeys:
                result = monkey.do_turn(lambda x: x // 3)
                for new_monkey, worry_level in result:
                    (monkeys[new_monkey]).append_item(worry_level)

        return monkey_business(monkeys)


ROUNDS2 = 10_000


def part2():
    with open("data/day11.txt", "r", encoding="utf-8") as data:
        lines = data.readlines()
        monkeys = read_monkeys(lines)
        common_multiple = prod(monkey.test_number() for monkey in monkeys)

        for _ in range(ROUNDS2):
            for monkey in monkeys:
                result = monkey.do_turn(lambda x: x % common_multiple)
                for new_monkey, worry_level in result:
                    (monkeys[new_monkey]).append_item(worry_level)

        return monkey_business(monkeys)
