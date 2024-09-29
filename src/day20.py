import copy
from collections import namedtuple

Node = namedtuple("Node", ["orig_idx", "value"])


def read_input(factor: int = 1) -> tuple[int, list[Node]]:
    with open("data/day20.txt", "r", encoding="utf-8") as data:
        number_arr = [factor * int(l.strip()) for l in data.readlines()]
        return [Node(i, v) for i, v in enumerate(number_arr)]


def calculate_grove_coords(nodes: list[Node]) -> int:
    zero_idx = [i for i, node in enumerate(nodes) if node.value == 0][0]
    n = len(nodes)
    return sum((nodes[(zero_idx + s) % n]).value for s in [1000, 2000, 3000])


def perform_shuffle(nodes: list[Node], times: int = 1) -> None:
    original_arr = copy.deepcopy(nodes)
    n = len(nodes)

    for _ in range(times):
        for node in original_arr:
            curr_idx = nodes.index(node)
            nodes.pop(curr_idx)
            new_idx = (curr_idx + node.value) % (n - 1)
            nodes.insert(new_idx, node)


def part1():
    nodes = read_input()
    perform_shuffle(nodes)
    return calculate_grove_coords(nodes)


DECRYPTION_KEY = 811589153


def part2():
    nodes = read_input(factor=DECRYPTION_KEY)
    perform_shuffle(nodes, times=10)
    return calculate_grove_coords(nodes)
