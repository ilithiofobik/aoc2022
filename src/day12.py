import heapq
from typing import Callable, Generator, List, Set, Tuple


def read_heights(
    lines: List[str],
) -> Tuple[List[List[int]], Tuple[int, int], Tuple[int, int]]:
    board = []
    start = (0, 0)
    end = (0, 0)

    for r_idx, line in enumerate(lines):
        row = []
        for c_idx, elem in enumerate(line.strip()):
            if elem == "S":
                start = (r_idx, c_idx)
                row.append(0)
            elif elem == "E":
                end = (r_idx, c_idx)
                row.append(ord("z") - ord("a"))
            else:
                row.append(ord(elem) - ord("a"))
        board.append(row)

    return board, start, end


def board_size(board: List[List[int]]) -> Tuple[int, int]:
    return len(board), len(board[0])


def initialize_distances(n: int, m: int, start: Tuple[int, int]) -> List[List[int]]:
    infinity = n * m + 1
    distances = [[infinity for _ in range(m)] for _ in range(n)]
    distances[start[0]][start[1]] = 0

    return distances


def neighbors(
    heights: List[List[int]], pos: Tuple[int, int], cond: Callable[[int, int], bool]
) -> Generator[Tuple[int, int], None, None]:
    row, col = pos
    num_rows, num_cols = len(heights), len(heights[0])

    for r, c in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        new_row, new_col = row + r, col + c

        if new_row < 0 or new_row >= num_rows or new_col < 0 or new_col >= num_cols:
            continue

        new_height = heights[new_row][new_col]
        height = heights[row][col]

        if cond(new_height, height):
            yield new_row, new_col


def calculate_distances(
    start: Tuple[int, int], heights: List[List[int]], cond: Callable[[int, int], bool]
) -> List[List[int]]:
    r_num, c_num = board_size(heights)
    distances = initialize_distances(r_num, c_num, start)
    pq: List[Tuple[int, Tuple[int, int]]] = [(0, start)]
    heapq.heapify(pq)
    visited: Set[Tuple[int, int]] = set()

    while pq:
        dist, pos = heapq.heappop(pq)

        if pos in visited:
            continue

        visited.add(pos)

        for neigh_r, neigh_c in neighbors(heights, pos, cond):
            distance = dist + 1

            if distance < distances[neigh_r][neigh_c]:
                distances[neigh_r][neigh_c] = distance
                heapq.heappush(pq, (distance, (neigh_r, neigh_c)))

    return distances


def part1() -> int:
    with open("data/day12.txt", "r", encoding="utf-8") as data:
        heights, start, end = read_heights(data.readlines())
        distances = calculate_distances(start, heights, lambda x, y: x - y <= 1)

        return distances[end[0]][end[1]]


def find_minimum(
    r_num: int, c_num: int, heights: List[List[int]], distances: List[List[int]]
) -> int:
    minimum = r_num * c_num

    for r in range(r_num):
        for c in range(c_num):
            if heights[r][c] == 0:
                minimum = min(minimum, distances[r][c])

    return minimum


def part2() -> int:
    with open("data/day12.txt", "r", encoding="utf-8") as data:
        heights, _, end = read_heights(data.readlines())
        r_num, c_num = board_size(heights)
        distances = calculate_distances(end, heights, lambda x, y: y - x <= 1)

        return find_minimum(r_num, c_num, heights, distances)
