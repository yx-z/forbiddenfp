from sys import setrecursionlimit
from typing import Tuple, Set

from forbiddenfp import use, not_equals

grid = """#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#""".splitlines()
nrows = len(grid)
ncols = len(grid[0])
row_range = range(nrows)
col_range = range(ncols)
start = (0, grid[0].index("."))
end = (nrows - 1, grid[-1].index("."))
DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
gen_neighbor = lambda dirs: lambda r, c, seen: dirs(r, c).map_unpack(lambda dr, dc: (r + dr, c + dc)).filter_unpack(
    lambda nr, nc: nr in row_range and nc in col_range and grid[nr][nc] != "#" and (nr, nc) not in seen
).tuple()
# 1
get_neighbors = gen_neighbor(
    lambda r, c: {"v": [(1, 0)], "^": [(-1, 0)], "<": [(0, -1)], ">": [(0, 1)]}.get(grid[r][c], DIRS)
)
longest = lambda crd, seen: 0 if crd == end else get_neighbors(*crd, seen).map(
    lambda n: longest(n, seen | {n})
).max().or_else(0) + 1
setrecursionlimit(2147483647)
longest(start, {start}).print()

# 2
vertices = (row_range, col_range).product().filter_unpack(lambda r, c: grid[r][c] != "#").list()
get_neighbors2 = gen_neighbor(use(DIRS))
edges = vertices.zip(vertices.map(lambda crd: get_neighbors2(*crd, set())).list()).dict()


def collapse(vertex: Tuple[int, int], neighbor: Tuple[int, int], dist: int = 1) -> Tuple[Tuple[int, int], int]:
    while len(edges[neighbor]) == 2:
        vertex, neighbor, dist = neighbor, edges[neighbor].next(not_equals(vertex)), dist + 1
    return neighbor, dist


edges = vertices.zip(vertices.map(lambda v: edges[v].map(lambda n: collapse(v, n)).list())).dict()


def search(node: Tuple[int, int], dist: int, stop: Tuple[int, int] = vertices[-1],
           seen: Set[Tuple[int, int]] = set()) -> int:
    if node == stop:
        return dist
    seen.add(node)
    longest = edges[node].filter_unpack(lambda n, _: n not in seen).map_unpack(
        lambda n, d: search(n, d + dist)
    ).max().or_else(0)
    seen.remove(node)
    return longest


search(vertices[0], 0).print()
