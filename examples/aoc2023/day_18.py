from typing import Tuple, List

import forbiddenfp

plans = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)""".splitlines().map(lambda l: l.split().apply(lambda ls: ls.setitem(1, ls[1].int()))).list()
DIR = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}


def solve(ins: List[Tuple[str, int]]) -> None:
    crds = ins.reduce(lambda ls, pl: pl.then_unpack(lambda d, cnt: ls[-1].then_unpack(lambda r, c: DIR[d].then_unpack(
        lambda dr, dc: ls + [(r + dr * cnt, c + dc * cnt)]
    ))), [(0, 0)])
    # shoelace theorem for inner area
    interior_points = crds.zip(crds.islice(1)).sum_unpack(lambda p1, p2: p1[0] * p2[1] - p2[0] * p1[1]).abs() // 2
    # pricks theorem: inner area = #interior points + #boundary points/2 - 1
    boundary_points = ins.sum_unpack(lambda _, d: d)
    # based on above, we are looking for #interior points + #boundary points
    print(interior_points + boundary_points // 2 + 1)


# 1
solve(plans.map_unpack(lambda d, c, _: (d, c)).list())
# 2
solve(plans.map_unpack(lambda _, __, hex: ["R", "D", "L", "U"][hex[-2].int()].pair(hex[2:7].int(16))).list())
