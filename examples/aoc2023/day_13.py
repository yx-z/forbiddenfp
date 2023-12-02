from typing import List

from forbiddenfp import join

patterns = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#""".split("\n\n").map(str.splitlines).list()


def reflect(grid: List[str], required_diff: int) -> int:
    num_rows = grid.len()
    row_range = num_rows.range()
    col_range = grid.next().range()
    # reflect by rows
    for mid_row_up, mid_row_down in row_range.groupwise(2):
        if range(mid_row_up, -1, -1).zip(range(mid_row_down, num_rows)).sum_unpack(
                lambda idx_up, idx_down: grid[idx_up].zip(grid[idx_down]).count_if_unpack(lambda x, y: x != y)
        ) == required_diff:
            return (1 + mid_row_up) * 100
    # reflect by cols
    rot = [[None for _ in row_range] for _ in col_range]
    for r, c in row_range.pair(col_range).product():
        rot[c][num_rows - 1 - r] = grid[r][c]
    return reflect(rot.map(join()).list(), required_diff) / 100


# 1
patterns.sum(lambda g: reflect(g, 0)).print()
# 2
patterns.sum(lambda g: reflect(g, 1)).print()
