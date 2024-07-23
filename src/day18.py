def read_cube(line):
    words = line.strip().split(",")
    x, y, z = map(int, words)
    return (x, y, z)


def are_overlapping(cube1, cube2):
    x1, y1, z1 = cube1
    x2, y2, z2 = cube2

    differences = sum([abs(x1 - x2), abs(y1 - y2), abs(z1 - z2)])

    return differences == 1


def read_input(lines):
    return set(read_cube(line) for line in lines)


def count_common_sides(cubes):
    common_sides = 0

    for cube in cubes:
        for other in cubes:
            if cube == other:
                continue
            if are_overlapping(cube, other):
                common_sides += 1

    return common_sides


def exterior_surface(cubes):
    common_sides = count_common_sides(cubes)

    return 6 * len(cubes) - common_sides


def part1():
    with open("data/day18.txt", "r", encoding="utf-8") as data:
        lines = data.readlines()
        cubes = read_input(lines)

        return exterior_surface(cubes)


def dict_add_zero_or_inc(d, key):
    if key in d:
        d[key] += 1
    else:
        d[key] = 1


def all_neighbors(cube):
    x, y, z = cube
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            for dz in [-1, 0, 1]:
                if abs(dx) + abs(dy) + abs(dz) == 1:
                    yield (x + dx, y + dy, z + dz)


def find_max_coords(cubes):
    max_x, max_y, max_z = 0, 0, 0

    for cube in cubes:
        x, y, z = cube
        max_x = max(max_x, x)
        max_y = max(max_y, y)
        max_z = max(max_z, z)

    return max_x, max_y, max_z


def find_min_coords(cubes, max_x, max_y, max_z):
    min_x, min_y, min_z = max_x, max_y, max_z

    for cube in cubes:
        x, y, z = cube
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        min_z = min(min_z, z)

    return min_x, min_y, min_z


def whole_space(min_all, max_all):
    min_x, min_y, min_z = min_all
    max_x, max_y, max_z = max_all

    space = set()

    for x in range(min_x - 1, max_x + 2):
        for y in range(min_y - 1, max_y + 2):
            for z in range(min_z - 1, max_z + 2):
                space.add((x, y, z))

    return space


def air_neighbors(air_cube, cubes, min_all, max_all):
    x, y, z = air_cube

    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            for dz in [-1, 0, 1]:
                if abs(dx) + abs(dy) + abs(dz) != 1:
                    continue
                (xn, yn, zn) = (x + dx, y + dy, z + dz)

                if xn < min_all[0] - 1 or xn > max_all[0] + 1:
                    continue

                if yn < min_all[1] - 1 or yn > max_all[1] + 1:
                    continue

                if zn < min_all[2] - 1 or zn > max_all[2] + 1:
                    continue

                if (xn, yn, zn) in cubes:
                    continue

                yield (xn, yn, zn)


def fill_air_pockets(cubes):
    max_all = find_max_coords(cubes)
    max_x, max_y, max_z = max_all
    min_all = find_min_coords(cubes, max_x, max_y, max_z)
    min_x, min_y, min_z = min_all

    space = whole_space(min_all, max_all)

    queue = [(min_x - 1, min_y - 1, min_z - 1)]
    visited = set()

    while queue:
        air_cube = queue.pop()
        visited.add(air_cube)

        for neighbor in air_neighbors(air_cube, cubes, min_all, max_all):
            if neighbor in visited:
                continue
            queue.append(neighbor)

    return space.difference(visited)


def part2():
    with open("data/day18.txt", "r", encoding="utf-8") as data:
        lines = data.readlines()
        cubes = read_input(lines)
        filled = fill_air_pockets(cubes)

        return exterior_surface(filled)
