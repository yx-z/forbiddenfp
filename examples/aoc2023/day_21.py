from typing import Iterable, Tuple, Callable

import forbiddenfp

grid = """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........""".splitlines()
nrows = grid.len()
ncols = grid[0].len()
row_range = nrows.range()
col_range = ncols.range()
empty = lambda r, c: grid[r][c] in (".", "S")
S = grid.enumerate().next_unpack(lambda r, line: "S" in line).then_unpack(lambda r, line: (r, line.index("S")))
dirs = lambda r, c: {(-1, 0), (1, 0), (0, -1), (0, 1)}.map_unpack(lambda dr, dc: (dr + r, dc + c))


def step(count: int, neighbor_fun: Callable[[int, int], Iterable[Tuple[int, int]]]) -> None:
    queue = {S}
    for _ in range(count):
        queue = queue.map_unpack(neighbor_fun).flatten().set()
    queue.len().print()


# 1
neighbors = lambda r, c: dirs(r, c).filter_unpack(lambda nr, nc: nr in row_range and nc in col_range and empty(nr, nc))
step(64, neighbors)


# 2
def resolve(r: int, rng: range) -> int:
    if r in rng:
        return r
    l = rng.stop - rng.start
    if r < rng.start:
        return resolve(r + l, rng)
    return resolve(r - l, rng)


neighbors2 = lambda r, c: dirs(r, c).filter_unpack(lambda nr, nc: empty(resolve(nr, row_range), resolve(nc, col_range)))
for i in (65, 65 + 131, 65 + 262):
    step(i, neighbors2)
# quadratic fit above values at x=0,1,2. Then the answer is the parabola at x=202300
