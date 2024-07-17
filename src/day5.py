def read_input(data):
    lines = data.readlines()
    indices_idx = lines.index("\n") - 1

    num_of_indices = len(lines[indices_idx]) // 4
    stacks = []
    for _ in range(num_of_indices):
        stacks.append([])

    for i in range(indices_idx - 1, -1, -1):
        for j in range(0, num_of_indices):
            c = lines[i][1 + 4 * j]
            if c == " ":
                continue
            stacks[j].append(c)

    instructions = []

    for line in lines[indices_idx + 2:]:
        words = line.split()
        num = int(words[1])
        from_stack = int(words[3])
        to_stack = int(words[5])
        instructions.append((num, from_stack, to_stack))

    return stacks, instructions

def part1():
    with open("data/day5.txt", "r", encoding="utf-8") as data:
        stacks, instructions = read_input(data)

        for instruction in instructions:
            num, from_stack, to_stack = instruction

            for _ in range(num):
                elem = stacks[from_stack - 1].pop()
                stacks[to_stack - 1].append(elem)

        result = ""

        for stack in stacks:
            result += stack[-1]

        return result

def part2():
    with open("data/day5.txt", "r", encoding="utf-8") as data:
        stacks, instructions = read_input(data)

        for instruction in instructions:
            num, from_stack, to_stack = instruction
            stacks[to_stack - 1].extend(stacks[from_stack - 1][-num:])
            stacks[from_stack - 1] = stacks[from_stack - 1][:-num]

        result = ""

        for stack in stacks:
            result += stack[-1]

        return result
