def read_the_forest(lines):
    forest = []

    for line in lines:
        row = []
        for tree in line.strip():
            row.append(int(tree))
        forest.append(row)

    num_of_rows = len(forest)
    num_of_cols = len(forest[0])

    return forest, num_of_rows, num_of_cols


def part1():
    with open("data/day8.txt", "r", encoding="utf-8") as data:
        # read the forest
        lines = data.readlines()
        forest, num_of_rows, num_of_cols = read_the_forest(lines)

        # is tree visible
        is_visible = []
        for _ in range(num_of_rows):
            is_visible.append([False] * num_of_cols)

        # left to right
        for row in range(num_of_rows):
            curr_max = -1
            for col in range(num_of_cols):
                if forest[row][col] > curr_max:
                    is_visible[row][col] = True
                    curr_max = forest[row][col]

        # right to left
        for row in range(num_of_rows):
            curr_max = -1
            for col in range(num_of_cols - 1, -1, -1):
                if forest[row][col] > curr_max:
                    is_visible[row][col] = True
                    curr_max = forest[row][col]

        # top to bottom
        for col in range(num_of_cols):
            curr_max = -1
            for row in range(num_of_rows):
                if forest[row][col] > curr_max:
                    is_visible[row][col] = True
                    curr_max = forest[row][col]

        # bottom to top
        for col in range(num_of_cols):
            curr_max = -1
            for row in range(num_of_rows - 1, -1, -1):
                if forest[row][col] > curr_max:
                    is_visible[row][col] = True
                    curr_max = forest[row][col]

        # count the trees
        count = 0
        for row in range(num_of_rows):
            for col in range(num_of_cols):
                if is_visible[row][col]:
                    count += 1

        return count


def scenic_score(forest, row, col, num_of_rows, num_of_cols):
    left, right, up, down = 0, 0, 0, 0
    tree_height = forest[row][col]

    # left
    for ncol in range(col - 1, -1, -1):
        left += 1
        if forest[row][ncol] >= tree_height:
            break

    # right
    for ncol in range(col + 1, num_of_cols):
        right += 1
        if forest[row][ncol] >= tree_height:
            break

    # up
    for nrow in range(row - 1, -1, -1):
        up += 1
        if forest[nrow][col] >= tree_height:
            break

    # down
    for nrow in range(row + 1, num_of_rows):
        down += 1
        if forest[nrow][col] >= tree_height:
            break

    return left * right * up * down


def part2():
    with open("data/day8.txt", "r", encoding="utf-8") as data:
        # read the forest
        lines = data.readlines()
        forest, num_of_rows, num_of_cols = read_the_forest(lines)
        max_scenic_score = 0

        for row in range(num_of_rows):
            for col in range(num_of_cols):
                max_scenic_score = max(
                    max_scenic_score,
                    scenic_score(forest, row, col, num_of_rows, num_of_cols),
                )

        return max_scenic_score
