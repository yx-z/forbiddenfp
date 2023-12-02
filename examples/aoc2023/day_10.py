import math
from typing import Set, Tuple

from forbiddenfp import equals, not_in, deepcopying

grid = """.....
.S-7.
.|.|.
.L-J.
.....""".splitlines().map(list).list()
row_range = grid.len().range()
col_range = grid.next().len().range()


def connected_neighbors(r: int, c: int) -> Set[Tuple[int, int]]:
    def get_neighbors(x: int, y: int) -> Set[Tuple[int, int]]:
        return grid[x][y].map_val({
            "|": [(x - 1, y), (x + 1, y)],
            "-": [(x, y - 1), (x, y + 1)],
            "L": [(x - 1, y), (x, y + 1)],
            "J": [(x - 1, y), (x, y - 1)],
            "7": [(x, y - 1), (x + 1, y)],
            "F": [(x, y + 1), (x + 1, y)],
            ".": []
        }).filter_unpack(lambda nr, nc: nr in row_range and nc in col_range)

    return get_neighbors(r, c).filter_unpack(lambda nr, nc: (r, c) in get_neighbors(nr, nc)).set()


s_row, s_col = grid.enumerate().map_unpack(
    lambda i, row: (i, row.index_if(equals("S")))
).next_unpack(lambda _, j: j is not None)
gen_start = deepcopying({(s_row, s_col)})


def has_cycle() -> bool:
    start_neighbors = connected_neighbors(s_row, s_col)
    if len(start_neighbors) != 2:
        return False
    one, other = start_neighbors
    seen = gen_start()

    def dfs(r: int, c: int) -> bool:
        if (r, c) == other:
            return True
        neighbors = connected_neighbors(r, c)
        if not neighbors:
            return False
        seen.add((r, c))
        return neighbors.filter(not_in(seen)).any_unpack(dfs)

    return dfs(*one)


for pipe in ("|", "F", "J", "7", "L", "-"):
    grid[s_row][s_col] = pipe
    if has_cycle():
        break
dist = [[math.inf for _ in grid.next()] for _ in grid].apply(lambda d: d[s_row].setitem(s_col, 0))


def step(r: int, c: int, step_seen: Set[Tuple[int, int]], curr: int = 1) -> None:
    dist[r][c] = min(dist[r][c], curr)
    step_seen.add((r, c))
    connected_neighbors(r, c).filter(not_in(step_seen)).each_unpack(lambda nr, nc: step(nr, nc, step_seen, curr + 1))


connected_neighbors(s_row, s_col).each_unpack(lambda r, c: step(r, c, gen_start()))
walls = (row_range, col_range).product().filter_unpack(lambda r, c: not math.isinf(dist[r][c])).set()
walls.map_unpack(lambda r, c: dist[r][c]).max().print()

# 2
count = 0
for r, row in grid.enumerate():
    in_maze = False
    for c, col in row.enumerate():
        if (r, c) not in walls:
            # add 0 or 1 based on the boolean
            count += in_maze.int()
            continue
        # We flip `in_maze` upon entering or exiting the maze.
        # "|" of course crosses the wall and we need to flip.
        # "L--J" and "F--7" stays at the same side of the maze. Think of it as walking along the edge of a U shape.
        # The cases are covered by not flipping at all ("L--J") and by flipping `in_maze` twice ("F--7").
        # "L--7" and "F--J" still mark entering/exiting the maze. But only once. Think of them as zigzagged walls ("|").
        # Hence, we only need to flip `in_maze` once (on one character).
        if col in ("|", "F", "7"):
            in_maze = not in_maze
print(count)
