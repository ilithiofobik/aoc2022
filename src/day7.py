from abc import ABC, abstractmethod


class Node(ABC):
    @abstractmethod
    def memory(self):
        pass

    @abstractmethod
    def children(self):
        pass


class FileNode(Node):
    def __init__(self, parent, name, memory):
        self.memory_value = memory
        self.parent = parent
        self.name = name

    def memory(self):
        return self.memory_value

    def children(self):
        return {}


class DirectoryNode(Node):
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name
        self.children_dict = {}

    def memory(self):
        return sum(child.memory() for child in self.children_dict.values())

    def children(self):
        return self.children_dict

    def add_child(self, child):
        self.children_dict[child.name] = child


def read_the_tree(lines):
    root = DirectoryNode(None, "root")
    current_node = root

    # building the tree
    for line in lines[1:]:
        words = line.split()

        # ls case
        if words[1] == "ls":
            continue

        # cd case
        if words[1] == "cd":
            folder = words[2]
            if folder == "..":
                current_node = current_node.parent
            else:
                current_node = (current_node.children())[folder]

        # new directory case
        elif words[0] == "dir":
            folder = words[1]
            current_node.add_child(DirectoryNode(current_node, folder))

        # new file case
        else:
            memory = int(words[0])
            name = words[1]
            current_node.add_child(FileNode(current_node, name, memory))

    return root


def sum_tree_with_limit(node, limit, result):
    if isinstance(node, DirectoryNode):
        memory = node.memory()
        if memory <= limit:
            result += memory

        for child in node.children().values():
            result = sum_tree_with_limit(child, limit, result)

    return result


def part1():
    with open("data/day7.txt", "r", encoding="utf-8") as data:
        lines = data.readlines()
        root = read_the_tree(lines)

        return sum_tree_with_limit(root, 100000, 0)


def search_for_minimum_bigger_than(node, limit, result):
    if isinstance(node, DirectoryNode):
        memory = node.memory()
        if memory >= limit:
            result = min(result, memory)

        for child in node.children().values():
            result = search_for_minimum_bigger_than(child, limit, result)

    return result


def part2():
    with open("data/day7.txt", "r", encoding="utf-8") as data:
        lines = data.readlines()
        root = read_the_tree(lines)

        total_memory = 70000000
        required_memory = 30000000
        used_memory = root.memory()
        memory_to_free = used_memory - (total_memory - required_memory)

        return search_for_minimum_bigger_than(root, memory_to_free, used_memory)
