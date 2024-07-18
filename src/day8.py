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


def create_boolean_array(num_of_rows, num_of_cols):
    is_visible = []
    for _ in range(num_of_rows):
        is_visible.append([False] * num_of_cols)

    return is_visible


def row_col_check(xs, ys, forest, is_visible, x_is_row):
    row, col = 0, 0
    for x in xs:
        if x_is_row:
            row = x
        else:
            col = x

        curr_max = -1
        for y in ys:
            if x_is_row:
                col = y
            else:
                row = y

            if forest[row][col] > curr_max:
                is_visible[row][col] = True
                curr_max = forest[row][col]


def part1():
    with open("data/day8.txt", "r", encoding="utf-8") as data:
        # read the forest
        lines = data.readlines()
        forest, num_of_rows, num_of_cols = read_the_forest(lines)

        # is tree visible
        is_visible = create_boolean_array(num_of_rows, num_of_cols)

        # left to right
        row_col_check(range(num_of_rows), range(num_of_cols), forest, is_visible, True)
        # right to left
        row_col_check(
            range(num_of_rows), range(num_of_cols - 1, -1, -1), forest, is_visible, True
        )
        # top to bottom
        row_col_check(range(num_of_cols), range(num_of_rows), forest, is_visible, False)
        # bottom to top
        row_col_check(
            range(num_of_cols),
            range(num_of_rows - 1, -1, -1),
            forest,
            is_visible,
            False,
        )

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
