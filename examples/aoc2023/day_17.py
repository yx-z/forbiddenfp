import heapq
import math
from collections import defaultdict
from typing import Tuple, Iterable

from forbiddenfp import use

grid = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533""".splitlines().map(lambda l: l.map(int).list()).list()
nrows = len(grid)
ncols = len(grid[0])
row_range = range(nrows)
col_range = range(ncols)
# coord_r, coord_c, (dir_r, dir_c), streak
Vertex = Tuple[int, int, Tuple[int, int], int]
DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def dijkstra(lo: int, hi: int) -> None:
    in_bound = lambda r, c, _, s: r in row_range and c in col_range and s in range(hi + 1)

    def get_neighbors(r: int, c: int, direct: Tuple[int, int], streak: int) -> Iterable[Vertex]:
        if streak < lo:
            return [(r + direct[0], c + direct[1], direct, streak + 1)].filter_unpack(in_bound)
        return DIRS.filter_unpack(lambda dr, dc: (-dr, -dc) != direct).map_unpack(
            lambda dr, dc: (r + dr, c + dc, (dr, dc), streak + 1 if (dr, dc) == direct else 1)
        ).filter_unpack(in_bound)

    def get_dist(src: Vertex, dst: Vertex) -> int:
        dist = defaultdict(use(math.inf)).apply(lambda d: d.setitem(src, 0))
        queue = [(0, src)]
        while queue:
            curr_dist, curr_node = heapq.heappop(queue)
            for n in get_neighbors(*curr_node):
                new_dist = curr_dist + grid[n[0]][n[1]]
                if new_dist < dist[n]:
                    dist[n] = new_dist
                    heapq.heappush(queue, (new_dist, n))
        return dist[dst]

    srcs = DIRS.map(lambda d: (0, 0, d, 0))
    dsts = (DIRS, range(lo, hi + 1)).product().map_unpack(lambda d, s: (nrows - 1, ncols - 1, d, s))
    (srcs, dsts).product().map_unpack(get_dist).min().print()


# 1
dijkstra(1, 3)
# 2
dijkstra(4, 10)
