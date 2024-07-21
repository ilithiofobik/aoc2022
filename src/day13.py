from dataclasses import dataclass


@dataclass
class Node:
    value: int
    children: list


def pack_node(node):
    return Node(None, [node])


def signum(x):
    if x < 0:
        return -1
    if x > 0:
        return 1
    return 0


def compare_integers(x, y):
    return signum(x - y)


def compare_arr_nodes(node1, node2):
    if len(node1.children) == 0:
        if len(node2.children) == 0:
            return 0
        return -1
    if len(node2.children) == 0:
        return 1

    inner1 = node1.children[0]
    inner2 = node2.children[0]
    first_compare = compare_nodes(inner1, inner2)

    if first_compare != 0:
        return first_compare

    new_arr1 = Node(None, node1.children[1:])
    new_arr2 = Node(None, node2.children[1:])

    return compare_nodes(new_arr1, new_arr2)


def compare_nodes(node1, node2):
    is_array1 = node1.value is None
    is_array2 = node2.value is None

    if is_array1 and is_array2:
        return compare_arr_nodes(node1, node2)

    if not is_array1 and is_array2:
        return compare_arr_nodes(pack_node(node1), node2)

    if is_array1 and not is_array2:
        return compare_arr_nodes(node1, pack_node(node2))

    return compare_integers(node1.value, node2.value)


def read_commas(text):
    commas = []
    depth = 0

    for i, c in enumerate(text):
        if c == "[":
            depth += 1
        elif c == "]":
            depth -= 1

        if depth == 1 and c == ",":
            commas.append(i)

    return commas


def read_node(text):
    # array case
    if text[0] == "[":
        if text[1] == "]":
            return Node(None, [])

        children = []
        commas = read_commas(text)
        starts = [0] + commas
        ends = commas + [len(text) - 1]

        for start, end in zip(starts, ends):
            children.append(read_node(text[start + 1 : end]))

        return Node(None, children)

    # value case
    value = int(text)
    return Node(value, None)


def part1():
    with open("data/day13.txt", "r", encoding="utf-8") as data:
        lines = data.readlines()
        num_of_instances = (len(lines) + 1) // 3
        result = 0

        for i in range(num_of_instances):
            node1 = read_node(lines[i * 3].strip())
            node2 = read_node(lines[i * 3 + 1].strip())

            if compare_nodes(node1, node2) == -1:
                result += i + 1

        return result


def double_packed(value):
    node = Node(value, None)
    return pack_node(pack_node(node))


def part2():
    with open("data/day13.txt", "r", encoding="utf-8") as data:
        lines = data.readlines()
        num_of_instances = (len(lines) + 1) // 3
        nodes = []

        for i in range(num_of_instances):
            node1 = read_node(lines[i * 3].strip())
            node2 = read_node(lines[i * 3 + 1].strip())
            nodes.append(node1)
            nodes.append(node2)

        double_two = double_packed(2)
        double_six = double_packed(6)

        count_two = 1
        count_six = 2

        for node in nodes:
            if compare_nodes(node, double_two) == -1:
                count_two += 1
            if compare_nodes(node, double_six) == -1:
                count_six += 1

        return count_two * count_six
